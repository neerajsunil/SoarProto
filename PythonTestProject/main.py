#
# FILE: Main.py (Python Test Project)
# BRIEF: This file contains some example code for using protobuf and the codec
# AUTHOR: Christopher Chan (cjchanx)
#
# PIP PACKAGE LIST: pip install cobs; pip install pyserial; pip install protobuf
#

import ControlMessage_pb2 as Proto
import CommandMessage_pb2 as ProtoCmd
import CoreProto_pb2 as Core

# Constants
EXAMPLE_COM_PORT = 'COM3'

def print_hi(name):
    print(f'Hi, {name}')

def example_protobuf_encode_decode():
    """
    Example of how to use Protobuf
    """

    # You can either generate a wrapped message like this...
    msg = Proto.ControlMessage()
    msg.source = Core.NODE_RCU
    msg.target = Core.NODE_DMB
    msg.ack.acking_msg_id = Core.NODE_DMB
    msg.ack.acking_msg_source = Core.NODE_DMB

    # Or like this
    controlMsg = Proto.AckNack()
    controlMsg.acking_msg_source = Core.NODE_DMB
    controlMsg.acking_msg_id = Core.MSG_INVALID
    msg2 = Proto.ControlMessage()
    msg2.source = Core.NODE_RCU
    msg2.target = Core.NODE_DMB
    msg2.nack.CopyFrom(controlMsg)

    # Serialize
    print('\n\t>> Example of a serializing a ACK message')
    msgOut = msg.SerializeToString()
    print(f'{msgOut}')

    # Deserialize
    print('\n\t>> Example of a deserializing a ACK message, and reading the message field')
    msgParsed = Proto.ControlMessage()
    msgParsed.ParseFromString(msgOut)

    if(msgParsed.HasField("ack")):
        print("I got a ACK")
    elif(msgParsed.HasField("nack")):
        print("I got a NACK")

    # Serialize
    print('\n\t>> Example of a serializing a NACK message')
    msgOut = msg2.SerializeToString()
    print(f'{msgOut}')

    # Deserialize
    print('\n\t>> Example of a deserializing a NACK message, and reading the message field')
    msgParsed.ParseFromString(msg2.SerializeToString())

    if(msgParsed.HasField("ack")):
        print("I got a ACK")
    elif(msgParsed.HasField("nack")):
        print("I got a NACK")



def example_codec_encode_decode():
    """
    Example of how to use the codec
    """
    from Codec import Codec

    # Imagine we've serialized some protobuf data
    msg = Proto.ControlMessage()
    msg.source = Core.NODE_RCU
    msg.target = Core.NODE_DMB
    msg.ack.acking_msg_id = Core.NODE_DMB
    msg.ack.acking_msg_source = Core.NODE_DMB
    buf = msg.SerializeToString()

    encBuf = Codec.Encode(buf, len(buf), Core.MessageID.MSG_CONTROL)
    print('\n\t>> Example of codec encoded protobuf data')
    print(f'Original Message Size: {len(buf)}')
    print(f'Expected Encoded Size: {Codec.GetEncodedSize(len(buf))}')
    print(f'Encoded Message Size: {len(encBuf)}')
    print(bytes(encBuf))


def example_send_state_change_to_serial():
    """
    Example of how to send a state change to the serial port
    """
    import serial       # You'll need to run `pip install pyserial`
    from Codec import Codec

    # Setup serial port
    ser = serial.Serial(EXAMPLE_COM_PORT, 115200)

    # Imagine we've serialized some protobuf data
    msg = ProtoCmd.CommandMessage()
    msg.source = Core.NODE_RCU
    msg.target = Core.NODE_DMB
    msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_GOTO_PRELAUNCH
    buf = msg.SerializeToString()

    encBuf = Codec.Encode(buf, len(buf), Core.MessageID.MSG_CONTROL)
    print('\n\t>> Example of codec encoded state change command')
    print(f'Original Message Size: {len(buf)}')
    print(f'Encoded Message Size: {len(encBuf)}')
    print(bytes(encBuf))

    # Send the data to the serial port
    ser.write(encBuf)

if __name__ == '__main__':
    print_hi('World')
    example_protobuf_encode_decode()
    example_codec_encode_decode()
    #example_send_state_change_to_serial()




