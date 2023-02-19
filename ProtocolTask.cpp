/**
  ******************************************************************************
  * File Name          : ProtocolTask.cpp
  * Description        : Utilities for protocolging the flight board.
  ******************************************************************************
*/

//TODO: Change the reception here directly to an array to receive to a large queue instead, that way we don't ever have to pause reception to process messages (if this runs into issues)

/* Includes ------------------------------------------------------------------*/
#include "ProtocolTask.hpp"
#include "Command.hpp"
#include "Utils.hpp"
#include <cstring>

#include "FlightTask.hpp"
#include "GPIO.hpp"
#include "stm32f4xx_hal.h"
#include "cobs.h"

/* Macros --------------------------------------------------------------------*/

/* Structs -------------------------------------------------------------------*/

/* Constants -----------------------------------------------------------------*/
constexpr uint8_t PROTOCOL_TASK_PERIOD = 100;

/* Variables -----------------------------------------------------------------*/

/* Prototypes ----------------------------------------------------------------*/

/* HAL Callbacks ----------------------------------------------------------------*/
//TODO: Add this code to wherever the global HAL_UART_RxCpltCallback is
/**
 * @brief HAL Callback for DMA/Interrupt Complete
 */
// void HAL_UART_RxCpltCallback(UART_HandleTypeDef* huart)
// {
//     if (huart->Instance == SystemHandles::UART_Protocol->Instance)
//         ProtocolTask::Inst().InterruptRxData();
// }

/* Functions -----------------------------------------------------------------*/
/**
 * @brief Constructor, sets all member variables
 */
ProtocolTask::ProtocolTask() : Task(TASK_PROTOCOL_QUEUE_DEPTH_OBJS)
{
    // Setup Buffers
    protocolRxBuffer = soar_malloc(PROTOCOL_RX_BUFFER_SZ_BYTES+1);
    memset(protocolRxBuffer, 0, PROTOCOL_RX_BUFFER_SZ_BYTES+1);

    // Setup index and flags
    protocolMsgIdx = 0;
    isProtocolMsgReady = false;
}

/**
 * @brief Init task for RTOS
 */
// NOTE: This must be in the derived class
//void ProtocolTask::InitTask()
//{
//    // Make sure the task is not already initialized
//    SOAR_ASSERT(rtTaskHandle == nullptr, "Cannot initialize Protocol task twice");
//
//    // Start the task
//    BaseType_t rtValue =
//        xTaskCreate((TaskFunction_t)ProtocolTask::RunTask,
//            (const char*)"ProtocolTask",
//            (uint16_t)TASK_PROTOCOL_STACK_DEPTH_WORDS,
//            (void*)this,
//            (UBaseType_t)TASK_PROTOCOL_PRIORITY,
//            (TaskHandle_t*)&rtTaskHandle);
//
//    //Ensure creation succeded
//    SOAR_ASSERT(rtValue == pdPASS, "ProtocolTask::InitTask - xTaskCreate() failed");
//}

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

        //Process the command -- RX Complete
        if(cm.GetCommand() == DATA_COMMAND && cm.GetTaskCommand() == EVENT_PROTOCOL_RX_COMPLETE) {
            // Allocate a command for storing the decoded message
            Command protoRx(DATA_COMMAND, PROTOCOL_RX_DECODED_DATA);
            uint8_t* decodedDataPtr = protoRx.AllocateData(protocolMsgIdx);

            // When we get an Rx complete, we need to run the COBS decoder on the message
            cobs_decode_result cobsRes = cobs_decode(decodedDataPtr, protocolMsgIdx, protocolRxBuffer, protocolMsgIdx);

            // We can mark the rx buffer as safe to write to now
            protocolMsgIdx = 0;
            isProtocolMsgReady = false;
            
            // If the COBS decode result is not OK, then we need to send a NACK
            if(cobsRes.status != COBS_DECODE_OK) {
                //TODO: Need to create and send a NACK
            }
            else
            {
                // Verify the initial byte is consistent, we keep the size with the message as that and the checksum will be parsed by HandleProtocolMessage
                //TODO: Implement this check

                // Handle the protocol message using the inherited function
                HandleProtocolMessage(protoRx);
            }
            
            protoRx.Reset();
        }
        // Process the command -- TX Request

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

/* Helper Functions --------------------------------------------------------------*/
