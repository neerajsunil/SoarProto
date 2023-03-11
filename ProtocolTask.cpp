/**
  ******************************************************************************
  * File Name          : ProtocolTask.cpp
  * Description        : Utilities for protocolging the flight board.
  ******************************************************************************
*/

/* Includes ------------------------------------------------------------------*/
#include "ProtocolTask.hpp"
#include "Command.hpp"
#include "Utils.hpp"
#include <cstring>

#include "FlightTask.hpp"
#include "UARTTask.hpp"
#include "stm32f4xx_hal.h"
#include "cobs.h"

#include "ControlMessage.hpp"
#include "WriteBufferFixedSize.h"
#include "_C++/ControlMessage.hpp"

/* Macros --------------------------------------------------------------------*/

/* Structs -------------------------------------------------------------------*/

/* Constants -----------------------------------------------------------------*/
constexpr uint8_t PROTOCOL_TASK_PERIOD = 100;

/* Variables -----------------------------------------------------------------*/

/* Prototypes ----------------------------------------------------------------*/

/* HAL Callbacks ----------------------------------------------------------------*/
//NOTE: This code MUST be added to wherever the HALRxCpltCallback is defined
//     else if (huart->Instance == SystemHandles::UART_Protocol->Instance)
//         <BOARD_ID>ProtocolTask::Inst().InterruptRxData();

/* Functions -----------------------------------------------------------------*/
/**
 * @brief Constructor, sets all member variables
 */
ProtocolTask::ProtocolTask(Proto::Node node) : Task(TASK_PROTOCOL_QUEUE_DEPTH_OBJS)
{
    // Setup Buffers
    protocolRxBuffer = soar_malloc(PROTOCOL_RX_BUFFER_SZ_BYTES+1);
    memset(protocolRxBuffer, 0, PROTOCOL_RX_BUFFER_SZ_BYTES+1);

    // Setup index and flags
    protocolMsgIdx = 0;
    isProtocolMsgReady = false;
    srcNode = node;
}

/**
 *    @brief Runcode for the ProtocolTask
 */
void ProtocolTask::Run(void * pvParams)
{
    // Arm the interrupt
    ReceiveData();

    while (1) {
        Command cm;

        //Wait forever for a command
        qEvtQueue->ReceiveWait(cm);

        //If this is a PROTOCOL_COMMAND, process it
        if (cm.GetCommand() == PROTOCOL_COMMAND) {
            switch (cm.GetTaskCommand()) {
            case EVENT_PROTOCOL_RX_COMPLETE: {                                              //Process the command -- RX Complete
                // Allocate a command for storing the decoded message
                Command protoRx(PROTOCOL_COMMAND, PROTOCOL_RX_DECODED_DATA);
                uint8_t* decodedDataPtr = protoRx.AllocateData(protocolMsgIdx);

                // Assert allocation was successful
                SOAR_ASSERT(decodedDataPtr);

                // When we get an Rx complete, we need to run the COBS decoder on the message
                cobs_decode_result cobsRes = cobs_decode(decodedDataPtr, protocolMsgIdx, protocolRxBuffer, protocolMsgIdx);

                // We can mark the rx buffer as safe to write to now
                protocolMsgIdx = 0;
                isProtocolMsgReady = false;

                // If the COBS decode result is not OK, then we need to send a NACK
                if (cobsRes.status != COBS_DECODE_OK) {
					SOAR_PRINT("PROTO-INFO: COBS Decode Failed: %d %d", cobsRes.status, cobsRes.out_len);
                    SendNACK();
                }
                else {
                    // Verify the checksum is correct, send a NACK if incorrect
                    //TODO: Implement this check, send NACK and don't handle if it fails

                    // Handle the protocol message using the inherited function
                    HandleProtocolMessage(protoRx);
                }

                protoRx.Reset();
            }
            case PROTOCOL_TX_REQUEST_DATA: {                                               //Process the command -- TX Request

				SOAR_PRINT("PROTO-INFO-Vs: TX Request Received [%d]", cm.GetDataSize());

                // Allocate a command for storing the encoded message
                Command protoTx(DATA_COMMAND, DEFAULT_PROTOCOL_UART_TX_TGT);

                // Allocate enough data for a COBS encoded message
                uint16_t msgSize = GET_COBS_MAX_LEN(cm.GetDataSize());
                protoTx.AllocateData(msgSize);

                // Encode in COBS
                cobs_encode_result cobsRes = cobs_encode(protoTx.GetDataPointer(), msgSize, cm.GetDataPointer(), cm.GetDataSize());

                if (cobsRes.status != COBS_ENCODE_OK) {
                    protoTx.Reset();
                    SOAR_PRINT("WARNING: COBS encode failed in ProtocolTask TX case\n");
                }

                // Send this off to the UART Task
                UARTTask::Inst().SendCommandReference(protoTx);
            }
            default:
                break;
            }
        }

        cm.Reset();
    }
}

/**
 * @brief Receive data, currently receives by arming interrupt
 */
bool ProtocolTask::ReceiveData()
{
    HAL_UART_Receive_IT(SystemHandles::UART_Protocol, &protocolRxChar, 1);
    return true;
}

/**
 * @brief Sends a message to UART Task directly after wrapping it inside the message ID and checksum, and encoding with COBS
 */
void ProtocolTask::SendData(uint8_t* data, uint16_t size, uint8_t msgId)
{
    uint16_t msgSize = GET_COBS_MAX_LEN(size + PROTOCOL_OVERHEAD_BYTES);

    // Temporary array to store the pre-COBS message
    const uint16_t preCobsSize = size + PROTOCOL_OVERHEAD_BYTES;
    uint8_t arr[preCobsSize];

    // Wrap in the message header and checksum
    uint16_t chkSum = Utils::getCRC32(data, size);
    arr[0] = msgId;
    *((uint32_t*)&arr[preCobsSize - 4]) = chkSum;

    // Send the data by wrapping in a COBS frame and sending direct to UART Task
    Command protoTx(DATA_COMMAND, DEFAULT_PROTOCOL_UART_TX_TGT);
    protoTx.AllocateData(msgSize);

    // Encode in COBS
    cobs_encode_result cobsEncRes = cobs_encode(protoTx.GetDataPointer(), msgSize, arr, preCobsSize);

    if (cobsEncRes.status != COBS_ENCODE_OK) {
        protoTx.Reset();
        SOAR_PRINT("WARNING: COBS encode failed in ProtocolTask NACK case\n");
    }

    SOAR_ASSERT(cobsEncRes.out_len == msgSize);
    protoTx.GetDataPointer()[msgSize] = 0x00;
    UARTTask::Inst().SendCommandReference(protoTx);
}

/*
 * @brief Send a NACK message to the UART Task
 */
void ProtocolTask::SendNACK()
{
    Proto::ControlMessage msg;
    msg.set_source(srcNode);
    msg.set_target(Proto::Node::NODE_RCU);
    msg.set_message_id(Proto::MessageID::MSG_CONTROL);
    Proto::AckNack nack;
    nack.set_acking_msg_source(Proto::Node::NODE_ANY);
    nack.set_acking_msg_id(Proto::MessageID::MSG_UNKNOWN);
    msg.set_nack(nack);

    EmbeddedProto::WriteBufferFixedSize<DEFAULT_PROTOCOL_WRITE_BUFFER_SIZE> writeBuffer;
    msg.serialize(writeBuffer);

    // Send the control message
    SendData(writeBuffer.get_data(), writeBuffer.get_size(), (uint8_t)Proto::MessageID::MSG_CONTROL);
}

/**
 * @brief Receive data to the buffer
 * @return Whether the protocolRxBuffer is ready or not
 */
void ProtocolTask::InterruptRxData()
{
    // If we already have an unprocessed protocol message, ignore this byte
    if (!isProtocolMsgReady) {
        // Check COBS byte for end of message
        if (protocolRxChar == '\0' || protocolMsgIdx == PROTOCOL_RX_BUFFER_SZ_BYTES) {
            // Null terminate and process
            protocolRxBuffer[protocolMsgIdx++] = '\0';
            isProtocolMsgReady = true;

            // Notify the protocol task
            Command cm(DATA_COMMAND, EVENT_PROTOCOL_RX_COMPLETE);
            bool res = qEvtQueue->SendFromISR(cm);

            // If we failed to send the event, we should reset the buffer, that way ProtocolTask doesn't stall
            if (res == false) {
                protocolMsgIdx = 0;
                isProtocolMsgReady = false;
            }
        }
        else {
            protocolRxBuffer[protocolMsgIdx++] = protocolRxChar;
        }
    }

    //Re-arm the interrupt
    ReceiveData();
}

/*
 * @brief Interface function to quickly send a protobuf message by providing the write buffer and the message ID
 * @param writeBuffer The write buffer containing the serialized protobuf message
 * @param msgId The message ID of the message
 */
void ProtocolTask::SendProtobufMessage(EmbeddedProto::WriteBufferFixedSize<DEFAULT_PROTOCOL_WRITE_BUFFER_SIZE>& writeBuffer, Proto::MessageID msgId)
{
    // Note: This function runs inside the calling task
    SendData(writeBuffer.get_data(), writeBuffer.get_size(), (uint8_t)msgId);
}

/* Helper Functions --------------------------------------------------------------*/
