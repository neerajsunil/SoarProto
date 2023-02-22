# Quick Protobuf Testing Script

import ControlMessage_pb2 as Proto

def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('World')

    # Generate an ACK_NACK message
    controlMsg = Proto.AckNack()
    controlMsg.acking_msg_source = Proto.NODE_DMB
    controlMsg.acking_msg_id = Proto.MSG_INVALID

    # You can either generate a wrapped message like this...
    msg = Proto.ControlMessage()
    msg.source = Proto.NODE_RCU
    msg.target = Proto.NODE_DMB
    msg.ack.acking_msg_id = Proto.NODE_DMB
    msg.ack.acking_msg_source = Proto.NODE_DMB

    # Or like this
    msg2 = Proto.ControlMessage()
    msg2.source = Proto.NODE_RCU
    msg2.target = Proto.NODE_DMB
    msg2.nack.CopyFrom(controlMsg)

    # Serialize
    msgOut = msg.SerializeToString()
    print(f'{msgOut}')

    # Deserialize
    msgParsed = Proto.ControlMessage()
    msgParsed.ParseFromString(msgOut)

    if(msgParsed.HasField("ack")):
        print("I got a ACK")
    elif(msgParsed.HasField("nack")):
        print("I got a NACK")

    # Serialize
    msgOut = msg2.SerializeToString()
    print(f'{msgOut}')

    # Deserialize
    msgParsed.ParseFromString(msg2.SerializeToString())

    if(msgParsed.HasField("ack")):
        print("I got a ACK")
    elif(msgParsed.HasField("nack")):
        print("I got a NACK")


