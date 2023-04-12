#
# FILE: Main.py (Python Test Project)
# BRIEF: This file contains some example code for using protobuf and the codec
# AUTHOR: Christopher Chan (cjchanx)
#
# PIP PACKAGE LIST: pip install cobs; pip install pyserial; pip install protobuf
#

#todo:  dont worry about acks, but do send nacks when a message is nonsensical
#       implement reverse receive from serial interrupt and send throgh mqtt



import ControlMessage_pb2 as Proto
import CommandMessage_pb2 as ProtoCmd
import CoreProto_pb2 as Core
import paho.mqtt.client as mqtt
import Publisher_nodered as pbnd

import serial       # You'll need to run `pip install pyserial`
from Codec import Codec
import time
import json

# Constants
EXAMPLE_COM_PORT = '/dev/ttyS0'
MQTT_BROKER = '127.0.0.1'
PASSPHRASE = '1'

CONTORL_MESSAGE_TOPIC = ''
# Setup serial port
SER = serial.Serial(EXAMPLE_COM_PORT, 115200)

# Globals
sequence_number = 1

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
    msg.ack.acking_msg_id = Core.MSG_INVALID
    msg.ack.acking_msg_source = Core.NODE_DMB
    print(msg)

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


def populate_command_msg(command):
    global sequence_number
    
    #create message
    msg = ProtoCmd.CommandMessage()
    msg.source = Core.NODE_RCU
    buf = msg.SerializeToString()
    msg.source_sequence_num = sequence_number
    sequence_number = sequence_number + 1

    if command == "RSC_ANY_TO_ABORT":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_ANY_TO_ABORT
        msg.target = Core.NODE_DMB
    elif command == "RSC_ARM_CONFIRM_1":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_ARM_CONFIRM_1
        msg.target = Core.NODE_DMB
    elif command == "RSC_ARM_CONFIRM_2":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_ARM_CONFIRM_2
        msg.target = Core.NODE_DMB
    elif command == "RSC_BURN_TO_COAST":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_BURN_TO_COAST
        msg.target = Core.NODE_DMB
    elif command == "RSC_CLOSE_DRAIN":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_CLOSE_DRAIN
        msg.target = Core.NODE_DMB
    elif command == "RSC_CLOSE_VENT":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_CLOSE_VENT
        msg.target = Core.NODE_DMB
    elif command == "RSC_COAST_TO_DESCENT":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_COAST_TO_DESCENT
        msg.target = Core.NODE_DMB
    elif command == "RSC_DESCENT_TO_RECOVERY":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_DESCENT_TO_RECOVERY
        msg.target = Core.NODE_DMB
    elif command == "RSC_FIRST_INVALID":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_FIRST_INVALID
        msg.target = Core.NODE_DMB
    elif command == "RSC_GOTO_ARM":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_GOTO_ARM
        msg.target = Core.NODE_DMB
    elif command == "RSC_GOTO_FILL":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_GOTO_FILL
        msg.target = Core.NODE_DMB
    elif command == "RSC_GOTO_IGNITION":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_GOTO_IGNITION
        msg.target = Core.NODE_DMB
    elif command == "RSC_GOTO_PRELAUNCH":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_GOTO_PRELAUNCH
        msg.target = Core.NODE_DMB
    elif command == "RSC_IGNITION_TO_LAUNCH":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_IGNITION_TO_LAUNCH
        msg.target = Core.NODE_DMB
    elif command == "RSC_LAUNCH_TO_BURN":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_LAUNCH_TO_BURN
        msg.target = Core.NODE_DMB
    elif command == "RSC_MEV_CLOSE":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_MEV_CLOSE
        msg.target = Core.NODE_DMB
    elif command == "RSC_OPEN_DRAIN":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_OPEN_DRAIN
        msg.target = Core.NODE_DMB
    elif command == "RSC_OPEN_VENT":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_OPEN_VENT
        msg.target = Core.NODE_DMB
    elif command == "RSC_POWER_TRANSITION_EXTERNAL":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_POWER_TRANSITION_EXTERNAL
        msg.target = Core.NODE_DMB
    elif command == "RSC_POWER_TRANSITION_ONBOARD":
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_POWER_TRANSITION_ONBOARD
        msg.target = Core.NODE_DMB
    elif command == "PMB_CLOSE_MEV":
        msg.pmb_command.command_enum = ProtoCmd.PMBCommand.Command.PMB_CLOSE_MEV
        msg.target = Core.NODE_PBB
    elif command == "PMB_LAST":
        msg.pmb_command.command_enum = ProtoCmd.PMBCommand.Command.PMB_LAST
        msg.target = Core.NODE_PBB
    elif command == "PMB_NONE":
        msg.pmb_command.command_enum = ProtoCmd.PMBCommand.Command.PMB_NONE
        msg.target = Core.NODE_PBB
    elif command == "PMB_OPEN_MEV":
        msg.pmb_command.command_enum = ProtoCmd.PMBCommand.Command.PMB_OPEN_MEV
        msg.target = Core.NODE_PBB
    else:
        msg.dmb_command.command_enum = ProtoCmd.DMBCommand.Command.RSC_NONE
        msg.target = Core.NODE_DMB

    return msg

def send_command_msg(command):
    #create msg
    msg = populate_command_msg(command)
    print("msg: ", msg)
    
    #encode
    buf = msg.SerializeToString()
    encBuf = Codec.Encode(buf, len(buf), Core.MessageID.MSG_COMMAND)
    print("buffer: ", buf)

    # Send the data to the serial port
    SER.write(encBuf)

def on_mqtt_message(client, userdata, message):
    while True:
        print("received message: ",str(message.payload.decode("utf-8")))
        data_dictionary = json.loads(message.payload.decode("utf-8"))

        if data_dictionary["passphrase"] != PASSPHRASE:
            print("wrong passphrase")
            #return False

        if message.topic == "RCU/Commands":
            send_command_msg(data_dictionary["command"])
        else:
            print("unknown topic")
            #return False

        #return True

def send_ack_message(msg):
    ack_msg = Proto.ControlMessage()
    ack_msg.source = Core.NODE_RCU
    ack_msg.target = msg.source
    ack_msg.message_id = Core.MSG_CONTROL
    ack_msg.source_sequence_number = 0
    ack_msg.ack.acking_msg_id = Core.MSG_INVALID
    ack_msg.ack.acking_msg_source = Core.NODE_RCU
    ack_msg.ack.acking_sequence_num = msg.source_sequence_number

# telemetry message is very primitive in the protobuf
#def process_telemetry_message(msg):

def process_control_message(msg):
    
    
    #how do I find out which oneof message is it, and what do I do with it? send it through a mqtt topic?

# placeholder in case the pu ever receives a command message
#def process_command_message(msg):

def on_serial_message(message):
    #decode
    msgId, data = Codec.Decode(message, len(message))

    #Process essage according to ID
    if msgId == Core.MessageID.MSG_TELEMETRY:
        #parse onto protobuf object
        #msgParsed.ParseFromString(buf) #?
        x = None
    elif msgId == Core.MessageID.MSG_CONTROL:
        process_control_message(data)




if __name__ == '__main__':

    #print_hi('World')
    example_protobuf_encode_decode()
    #example_codec_encode_decode()
    #example_send_state_change_to_serial()

    client = mqtt.Client()
    client.connect(MQTT_BROKER)

    client.loop_start()
    client.subscribe("RCU/Commands")
    client.on_message=on_mqtt_message
    #client.loop_stop()

    while True:
        #client.publish("TELE_TEST", "side")


        # codec encodes the end of a message through a 0x00
        #serial_message = SER.read_until(expected = b'\x00', size = None)
        #on_serial_message(serial_message)

        time.sleep(1)
        