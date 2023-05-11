#
# FILE: Main.py (Python Test Project)
# BRIEF: This file contains some example code for using protobuf and the codec
# AUTHOR: Christopher Chan (cjchanx)
#
# PIP PACKAGE LIST: pip install cobs; pip install pyserial; pip install protobuf
#

#todo:  dont worry about acks, but do send nacks when a message is nonsensical
#       implement reverse receive from serial interrupt and send through mqtt
#       add RCU node to Protobuf
#       figure out telemetry messages
#       figure out mqtt topic names
#       get rid of telemetry_pb2 files?



import ControlMessage_pb2 as Proto
import CommandMessage_pb2 as ProtoCmd
import TelemetryMessage_pb2 as ProtoTele
import CoreProto_pb2 as Core
import paho.mqtt.client as mqtt
import Protobuf_parser as ProtoParse

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

def populate_command_msg(command):
    global sequence_number
    
    #create message
    msg = ProtoCmd.CommandMessage()
    msg.source = Core.NODE_RCU
    msg.source_sequence_num = sequence_number
    sequence_number = sequence_number + 1

    dmb_command = pbnd.STRING_TO_RSC_PROTO_STATE.get(command)

    if dmb_command != None:
        msg.pmb_command.command_enum = dmb_command
        msg.target = Core.NODE_DMB
    else:
        pmb_comand = pbnd.STRING_TO_PMB_PROTO_STATE.get(command)

        if pmb_comand != None:
            msg.pmb_command.command_enum = pmb_comand
            msg.target = Core.NODE_DMB
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
    ack_msg.ack.acking_msg_id = msg.message_id
    ack_msg.ack.acking_msg_source = Core.NODE_RCU
    ack_msg.ack.acking_sequence_num = msg.source_sequence_number

# telemetry message
def process_telemetry_message(msg):
    msgId, data = Codec.Decode(message, len(message))

    received_message = Proto.TelemetryMessage()
    
    try:
        received_message.ParseFromString(data)
    Exception DecodeError: 
        return

    if received_message.target == Core.NODE_RCU:
        message_type = received_message.WhichOneof('message')
        ProtoParse.TELE_FUNCTION_DICTIONARY[message_type](received_message)


def process_control_message(data):
    received_message = Proto.ControlMessage()

    try:
        received_message.ParseFromString(data)
    Exception DecodeError: 
        return

    if received_message.target == Core.NODE_RCU:
        message_type = received_message.WhichOneof('message')
        if message_type == 'sys_state':
            print(received_message.sys_state)
            if received_message.source == Core.NODE_DMB:
                pbnd.MCB_CMD['CMD_DMB_STATE'] = pbnd.PROTO_STATE_TO_STRING[received_message.sys_state.rocket_state]
                print(pbnd.PROTO_STATE_TO_STRING[received_message.sys_state.rocket_state])
        elif message_type == 'hb':
            print('hb: ', received_message.source)
        elif message_type == 'ping':
            send_ack_message(received_message)
            print('we were pinged: ', received_message.source)
        elif message_type == 'ack':
            print('oh hey, we ack: ', received_message.source)
        elif message_type == 'nack':
            #add resend of message
            print('nack received, this is bad')
    

# placeholder in case the pu ever receives a command message
#def process_command_message(msg):

def on_serial_message(message):
    #decode
    msgId, data = Codec.Decode(message, len(message))

    #Process essage according to ID
    if msgId == Core.MessageID.MSG_TELEMETRY:
        process_telemetry_message(data)
    elif msgId == Core.MessageID.MSG_CONTROL:
        process_control_message(data)




if __name__ == '__main__':
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
        