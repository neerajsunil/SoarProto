#
# FILE: Main.py (Python Test Project)
# BRIEF: This file contains some example code for using protobuf and the codec
# AUTHOR: Christopher Chan (cjchanx)
#
# PIP PACKAGE LIST: pip install cobs; pip install pyserial; pip install protobuf
#

#todo:  dont worry about acks, but do send nacks when a message is nonsensical
#       Check Nacks



from asyncio import sleep
import ControlMessage_pb2 as ProtoCtr
import CommandMessage_pb2 as ProtoCmd
import TelemetryMessage_pb2 as ProtoTele
import CoreProto_pb2 as Core
import paho.mqtt.client as mqtt
import Protobuf_parser as ProtoParse
import Publisher_nodered as pbnd
import google.protobuf.message as message
from cobs import cobs   # pip install cobs

import serial       # You'll need to run `pip install pyserial`
from Codec import Codec
import time
import json

# Constant
EXAMPLE_COM_PORT = '/dev/ttyS0'
MQTT_BROKER = '127.0.0.1'
PASSPHRASE = '1'
DMB_SEQ_NUM = 10
PBB_SEQ_NUM = 20
SOB_SEQ_NUM = 30

# Setup serial port
# 
SER = serial.Serial(port=EXAMPLE_COM_PORT, baudrate=115200, bytesize=8, parity=serial.PARITY_NONE, timeout=None, stopbits=serial.STOPBITS_ONE)

# Globals
sequence_number = 1
current_state = "RS_ABORT"
nos1_hold_mass = 0
nos2_hold_mass = 0

def handle_pi_command(data_dictionary):
    global nos1_hold_mass, nos2_hold_mass
    command = data_dictionary["command"]
 
    if command == "NOS1_HOLD":
        pbnd.tele_rcu_obj.is_nos1_hold_enable = True
    elif command == "NOS2_HOLD":
        pbnd.tele_rcu_obj.is_nos2_hold_enable = True
    elif command == "NOS1_RESET":
        pbnd.tele_rcu_obj.is_nos1_hold_enable = False
    elif command == "NOS2_RESET":
        pbnd.tele_rcu_obj.is_nos2_hold_enable = False
    else:
        ProtoParse.client.publish("TELE_PI_ERROR", json.dumps({"error": "Invalid Command"}))
        return False

def populate_command_msg(data_dictionary):
    global sequence_number

    command = data_dictionary["command"]

    #create message  
    msg = ProtoCmd.CommandMessage()
    msg.source = Core.NODE_RCU
    msg.source_sequence_num = sequence_number
    sequence_number = sequence_number + 1

    dmb_command = ProtoParse.STRING_TO_RSC_PROTO_COMMAND.get(command)

    if dmb_command != None:
        if data_dictionary["passphrase"] != PASSPHRASE:
            ProtoParse.client.publish("TELE_PI_ERROR", json.dumps({"error": "Invalid Passphrase"}))
            return False

        if command not in ProtoParse.ALLOWED_COMMANDS_FROM_STATE[current_state]:
            ProtoParse.client.publish("TELE_PI_ERROR", json.dumps({"error": "Invalid RSC Command"}))
            return False
 
        msg.dmb_command.command_enum = dmb_command
        msg.target = Core.NODE_DMB
        return msg
    
    pbb_command = ProtoParse.STRING_TO_PBB_PROTO_COMMAND.get(command)

    if pbb_command != None:
        msg.pbb_command.command_enum = pbb_command
        msg.target = Core.NODE_PBB
        return msg

    rcu_command = ProtoParse.STRING_TO_RCU_PROTO_COMMAND.get(command)

    if rcu_command != None:
        msg.rcu_command.command_enum = rcu_command
        if rcu_command == ProtoCmd.RCUCommand.RCU_CALIBRATE_NOS1_LOAD_CELL or rcu_command == ProtoCmd.RCUCommand.RCU_CALIBRATE_NOS2_LOAD_CELL:
            # for now, sending calibration known mass as passphrase
            msg.rcu_command.command_param = int(data_dictionary["passphrase"])
        msg.target = Core.NODE_RCU
        return msg

    sob_command = ProtoParse.STRING_TO_SOB_PROTO_COMMAND.get(command)

    if sob_command != None:
        msg.sob_command.command_enum = sob_command
        if sob_command == ProtoCmd.SOBCommand.SOB_CALIBRATE_LOAD_CELL:
            # for now, sending calibration known mass as passphrase
            msg.sob_command.command_param = int(data_dictionary["passphrase"])
        msg.target = Core.NODE_SOB
        return msg
    
    # insert handling for control message
    # if PING_DMB
    # if PING_PBB
    # if PING_SOB
    # Send received PING ACKS to TELE_PI_ERROR :)
    
    ProtoParse.client.publish("TELE_PI_ERROR", json.dumps({"error": "Invalid Command"}))
    return False

def send_command_msg(data_dictionary):
    #create msg
    msg = populate_command_msg(data_dictionary)

    if(msg == False):
        return

    print(msg)

    #encode
    buf = msg.SerializeToString()
    encBuf = Codec.Encode(buf, len(buf), Core.MessageID.MSG_COMMAND)
    #print(len(encBuf))
    #print(encBuf)

    # Send the data to the serial port
    SER.write(encBuf)

def send_ping_message(data_dictionary):
    global sequence_number

    #create message  
    msg = ProtoCtr.ControlMessage()
    msg.source = Core.NODE_RCU
    msg.source_sequence_num = sequence_number
    sequence_number = sequence_number + 1
    ping = ProtoCtr.Ping()

    if data_dictionary.get("Target") == "DMB":
        msg.target == Core.NODE_DMB
        ping.ping_ack_id = Core.MSG_CONTROL
        ping.ping_response_sequence_num = DMB_SEQ_NUM
        ping.sys_state_response_required = True
    elif data_dictionary.get("Target") == "PBB":
        msg.target == Core.NODE_PBB
        ping.ping_ack_id = Core.MSG_CONTROL
        ping.ping_response_sequence_num = PBB_SEQ_NUM
        ping.sys_state_response_required = False
    elif data_dictionary.get("Target") == "SOB":
        msg.target == Core.NODE_SOB
        ping.ping_ack_id = Core.MSG_CONTROL
        ping.ping_response_sequence_num = SOB_SEQ_NUM
        ping.sys_state_response_required = False

    msg.ping.CopyFrom(ping)

    #encode
    buf = msg.SerializeToString()
    encBuf = Codec.Encode(buf, len(buf), Core.MessageID.MSG_COMMAND)
    #print(len(encBuf))
    #print(encBuf)

    # Send the data to the serial port
    SER.write(encBuf)


    

def on_mqtt_message(client, userdata, message):
    print("----------------------------------------------------received message:\n ",str(message.payload.decode("utf-8")))
    data_dictionary = json.loads(message.payload.decode("utf-8"))

    if message.topic == "RCU/Commands":
        send_command_msg(data_dictionary)
    elif message.topic == "RCU/Pings":
        send_ping_message(data_dictionary)
    elif message.topic == "Pi/Commands":
        handle_pi_command(data_dictionary)
    else:
        ProtoParse.client.publish("TELE_PI_ERROR", json.dumps({"error": "Unknown Command Topic"}))
        print("unknown topic")
        return False
        
    return True

def send_ack_message(msg):
    ack_msg = ProtoCmd.ControlMessage()
    ack_msg.source = Core.NODE_RCU
    ack_msg.target = msg.source
    ack_msg.message_id = Core.MSG_CONTROL
    ack_msg.source_sequence_number = 0
    ack_msg.ack.acking_msg_id = msg.message_id
    ack_msg.ack.acking_msg_source = Core.NODE_RCU
    ack_msg.ack.acking_sequence_num = msg.source_sequence_number

# telemetry message
def process_telemetry_message(data):
    received_message = ProtoTele.TelemetryMessage()
    try:
        received_message.ParseFromString(data)
    except message.Decoprocess_control_messagedeError: 
        print("cannot decode telemetry message")
        return

    print(received_message)

    if received_message.target == Core.NODE_RCU:
        message_type = received_message.WhichOneof('message')
        #print(message_type)
        #print(received_message)

        if(message_type != None):
            ProtoParse.TELE_FUNCTION_DICTIONARY[message_type](received_message)
            return
        else:
            print("received invalid telemetry message type")
            ProtoParse.client.publish("TELE_PI_ERROR", json.dumps({"error": "Invalid telemetry message type"}))

# control message 
def process_control_message(data):
    received_message = ProtoCtr.ControlMessage()

    try:
        received_message.ParseFromString(data)
    except message.DecodeError:
        print("cannot decode control message")
        return

    print(received_message)

    if received_message.target == Core.NODE_RCU:
        message_type = received_message.WhichOneof('message')
        if message_type == 'sys_state':
            #print(received_message.sys_state)
            if received_message.source == Core.NODE_DMB:
                global current_state
                current_state = ProtoParse.PROTO_STATE_TO_STRING[received_message.sys_state.rocket_state]
                ProtoParse.client.publish("CONTROL_SYS_STATE", json.dumps({"dmb_state": str(current_state)}))

                #print(ProtoParse.PROTO_STATE_TO_STRING[received_message.sys_state.rocket_state])
        elif message_type == 'hb':
            print('hb: ', received_message.source)
        elif message_type == 'ping':
            if received_message.source == Core.NODE_DMB and received_message.ping.ping_response_sequence_num == DMB_SEQ_NUM:
                ProtoParse.client.publish("TELE_PI_ERROR", '{"ping_status" : "ping from DMB received"}')
            elif received_message.source == Core.NODE_PBB and received_message.ping.ping_response_sequence_num == PBB_SEQ_NUM:
                ProtoParse.client.publish("TELE_PI_ERROR", '{"ping_status" : "ping from PBB received"}')
            elif received_message.source == Core.NODE_SOB and received_message.ping.ping_response_sequence_num == SOB_SEQ_NUM:
                ProtoParse.client.publish("TELE_PI_ERROR", '{"ping_status" : "ping from SOB received"}')
            else:
                ProtoParse.client.publish("TELE_PI_ERROR", '{"ping_status" : "unknown ping received"}')
            print('we were pinged: ', received_message.source)
        elif message_type == 'ack':
            print('oh hey, we ack: ', received_message.source)
        elif message_type == 'nack':
            #add resend of message
            print('nack received, this is bad')
    
# placeholder in case the pi ever receives a command message
#def process_command_message(msg):

def on_serial_message(message):
    if len(message) < 5:
        print("Pi error message too short")
        ProtoParse.cliprocess_control_message
    
    #print("message received")
    #decode, remove 0x00 byte
    try:
        msgId, data = Codec.Decode(message[:-1], len(message) - 1)
    except cobs.DecodeError:
        print("invalid cobs message")
        ProtoParse.client.publish("TELE_PI_ERROR", json.dumps({"error": "Received invalid cobs message"}))
        return

    #Process essage according to ID
    if msgId == Core.MessageID.MSG_TELEMETRY:
        process_telemetry_message(data)
    elif msgId == Core.MessageID.MSG_CONTROL:
        process_control_message(data)
    else:
        print("Pi error")
        ProtoParse.client.publish("TELE_PI_ERROR", json.dumps({"error": "Received invalid MessageID"}))

if __name__ == '__main__':
    ProtoParse.client.connect(MQTT_BROKER)

    ProtoParse.client.loop_start()
    ProtoParse.client.subscribe("RCU/Commands")
    ProtoParse.client.subscribe("Pi/Commands")
    ProtoParse.client.subscribe("RCU/Pings")
    ProtoParse.client.on_message=on_mqtt_message

    print("listening to RCU Commands")

    while True:
        # codec encodes the end of a message through a 0x00
        serial_message = SER.read_until(expected = b'\x00', size = None)
        # print(serial_message)
        on_serial_message(serial_message)
        x = None
        
