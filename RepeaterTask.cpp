/**
  ******************************************************************************
  * File Name          : RepeaterTask.cpp
  * Description        : The base RepeaterTask, includes basic logic for receiving until either
  *                      the buffer is full, or the end-frame byte for protocol is detected.
  ******************************************************************************
*/
#include "UARTTask.hpp"
#include "stm32f4xx_hal.h"
#include "RepeaterTask.hpp"

/**
 * @brief Constructor, sets all member variables
 */
RepeaterTask::RepeaterTask(UART_HandleTypeDef* huart, uint16_t uartTaskCmd) : Task(TASK_REPEATER_QUEUE_DEPTH_OBJS),
    uartTaskCommand(uartTaskCmd)
{
    // Setup Buffers
    protocolRxBuffer = soar_malloc(PROTOCOL_RX_BUFFER_SZ_BYTES + 1);
    memset(protocolRxBuffer, 0, PROTOCOL_RX_BUFFER_SZ_BYTES + 1);

    // Setup index and flags
    protocolMsgIdx = 0;
    isProtocolMsgReady = false;

    // Setup the internal variables
    uartHandle = huart;
}

/**
 * @brief Runcode for the RepeaterTask
 */
void RepeaterTask::Run(void* pvParams)
{
    // Arm the interrupt
    ReceiveData();

    while (1) {
        Command cm;

        // Wait forever for a command
        qEvtQueue->ReceiveWait(cm);

        // If this is a repeater Rx Complete event, process it
        if (cm.GetCommand() == PROTOCOL_COMMAND && cm.GetTaskCommand() == REPEATER_TASK_COMMANDS::EVENT_REPEATER_RX_COMPLETE) {
            SendData(protocolRxBuffer, protocolMsgIdx);

            // We can mark the rx buffer as safe to write to now
            protocolMsgIdx = 0;
            isProtocolMsgReady = false;
        }

        cm.Reset();
    }
}

/**
 * @brief Receive data, currently receives by arming interrupt
 */
bool RepeaterTask::ReceiveData()
{
    HAL_UART_Receive_IT((UART_HandleTypeDef*)uartHandle, &protocolRxChar, 1);
    return true;
}

/**
 * @brief Receive data to the buffer
 * @return Whether the protocolRxBuffer is ready or not
 */
void RepeaterTask::InterruptRxData()
{
    // If we already have an unprocessed protocol message, ignore this byte
    if (!isProtocolMsgReady) {
        // Check COBS byte for end of message
        if (protocolRxChar == '\0' || protocolMsgIdx == PROTOCOL_RX_BUFFER_SZ_BYTES) {
            // If the message is of insufficient length, reset the buffer
            if (protocolMsgIdx < PROTOCOL_MINIMUM_MESSAGE_LENGTH) {
                protocolMsgIdx = 0;
                isProtocolMsgReady = false;
            }
            else {
                // Null terminate and process
                protocolRxBuffer[protocolMsgIdx++] = '\0';
                isProtocolMsgReady = true;

                // Notify the protocol task
                Command cm(PROTOCOL_COMMAND, EVENT_PROTOCOL_RX_COMPLETE);
                bool res = qEvtQueue->SendFromISR(cm);

                // If we failed to send the event, we should reset the buffer, that way ProtocolTask doesn't stall
                if (res == false) {
                    protocolMsgIdx = 0;
                    isProtocolMsgReady = false;
                }
            }
        }
        else {
            protocolRxBuffer[protocolMsgIdx++] = protocolRxChar;
        }
    }

    //Re-arm the interrupt
    ReceiveData();
}
