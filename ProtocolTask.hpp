/**
 ******************************************************************************
 * File Name          : ProtocolTask.hpp
 * Description        :
 ******************************************************************************
*/
#ifndef SOAR_SYSTEM_PROTOCOL_TASK_HPP_
#define SOAR_SYSTEM_PROTOCOL_TASK_HPP_
/* Includes ------------------------------------------------------------------*/
#include "Task.hpp"
#include "SystemDefines.hpp"
#include "UARTTask.hpp"

/* Enums ------------------------------------------------------------------*/
enum PROTOCOL_TASK_COMMANDS {
    PROTOCOL_TASK_COMMAND_NONE = 0,
    EVENT_PROTOCOL_RX_COMPLETE,
    PROTOCOL_RX_DECODED_DATA,
    PROTOCOL_TX_REQUEST_DATA
};

/* Macros ------------------------------------------------------------------*/
constexpr uint16_t PROTOCOL_RX_BUFFER_SZ_BYTES = 255;
constexpr uint16_t DEFAULT_PROTOCOL_TASK_TX_TGT = UART_TASK_COMMAND_SEND_RADIO; // Must go in derived task
constexpr uint16_t DEFAULT_PROTOCOL_WRITE_BUFFER_SIZE = 256;

// Task Definition
constexpr uint8_t TASK_PROTOCOL_PRIORITY = 2;            // Priority of the protocol task
constexpr uint8_t TASK_PROTOCOL_QUEUE_DEPTH_OBJS = 10;        // Size of the protocol task queue
constexpr uint16_t TASK_PROTOCOL_STACK_DEPTH_WORDS = 256;        // Size of the protocol task stack

/* Class ------------------------------------------------------------------*/
class ProtocolTask : public Task
{
public:
// NOTE: This must be in the derived class
//    static ProtocolTask& Inst() {
//        static ProtocolTask inst;
//        return inst;
//    }
	ProtocolTask();

    void InitTask();

    //Functions exposed to HAL callbacks
    void InterruptRxData();

protected:
// NOTE: This must be in the derived class
//    static void RunTask(void* pvParams) { ProtocolTask::Inst().Run(pvParams); } // Static Task Interface, passes control to the instance Run();
    void Run(void* pvParams);    // Main run code

    void ConfigureUART();
    // This will receive a (PROTOCOL_COMMAND, PROTOCOL_RX_DECODED_DATA) with the data pointer allocated, COBS decoded (but in the SOAR Message Format)
    virtual void HandleProtocolMessage(Command& cmd) = 0;   // This MUST be implemented in the derived board-specific ProtocolTask object
    //void HandleCommand(Command& cm);

    bool ReceiveData();

    // Helper functions
    
    // Member variables
    uint8_t* protocolRxBuffer;
    uint16_t protocolMsgIdx;
    bool isProtocolMsgReady;

    uint8_t protocolRxChar; // Character received from UART Interrupt

private:
// NOTE: This must be in the derived class
//    ProtocolTask(); // Private constructor
//    ProtocolTask(const ProtocolTask&);                    // Prevent copy-construction
//    ProtocolTask& operator=(const ProtocolTask&);            // Prevent assignment
};

#endif    // SOAR_SYSTEM_PROTOCOL_TASK_HPP_
