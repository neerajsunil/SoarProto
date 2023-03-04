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
#include "WriteBufferFixedSize.h"
#include "CoreProto.h"

/* Enums ------------------------------------------------------------------*/
enum PROTOCOL_TASK_COMMANDS {
    PROTOCOL_TASK_COMMAND_NONE = 0,
    EVENT_PROTOCOL_RX_COMPLETE,
    PROTOCOL_RX_DECODED_DATA,
    PROTOCOL_TX_REQUEST_DATA
};

/* Macros ------------------------------------------------------------------*/
constexpr uint16_t PROTOCOL_RX_BUFFER_SZ_BYTES = 255;
constexpr uint16_t DEFAULT_PROTOCOL_UART_TX_TGT = UART_TASK_COMMAND_SEND_RADIO; // Should go in systemdefines
constexpr uint16_t DEFAULT_PROTOCOL_WRITE_BUFFER_SIZE = 256;

// Task Definition
constexpr uint8_t TASK_PROTOCOL_PRIORITY = 2;            // Priority of the protocol task
constexpr uint8_t TASK_PROTOCOL_QUEUE_DEPTH_OBJS = 10;        // Size of the protocol task queue
constexpr uint16_t TASK_PROTOCOL_STACK_DEPTH_WORDS = 256;        // Size of the protocol task stack

// Protocol Definition
// The protocol is applied BEFORE COBS encoding, and contains a message ID and a checksum footer
constexpr uint8_t PROTOCOL_OVERHEAD_BYTES = 1 + 4;        // Size of the protocol overhead (message ID + 4 byte checksum)

/* Class ------------------------------------------------------------------*/
class ProtocolTask : public Task
{
public:
// NOTE: This must be in the derived class
//    static ProtocolTask& Inst() {
//        static ProtocolTask inst;
//        return inst;
//    }
    ProtocolTask(Proto::Node node);

    virtual void InitTask() = 0;

    //Functions exposed to HAL callbacks
    void InterruptRxData();

    //Main interface function for sending protobuf messages
    static void SendProtobufMessage(EmbeddedProto::WriteBufferFixedSize<DEFAULT_PROTOCOL_WRITE_BUFFER_SIZE>& writeBuffer, Proto::MessageID msgId);

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

    Proto::Node srcNode;

    static void SendData(uint8_t* data, uint16_t size, uint8_t msgId); // Send a protobuf encoded message over UART
    void SendNACK(); // Send a NACK message over UART

private:
// NOTE: This must be in the derived class
//    ProtocolTask(); // Private constructor
//    ProtocolTask(const ProtocolTask&);                    // Prevent copy-construction
//    ProtocolTask& operator=(const ProtocolTask&);            // Prevent assignment
};

#endif    // SOAR_SYSTEM_PROTOCOL_TASK_HPP_
