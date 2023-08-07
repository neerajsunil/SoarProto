import serial       # You'll need to run `pip install pyserial`
from cobs import cobs   # pip install cobs
from Codec import Codec
import Telemetry_Objects as TelO
import google.protobuf.message as message
import json

def init_serial_port(given_port):
    # Setup serial port
    SER = serial.Serial(port=given_port, baudrate=115200, bytesize=8, parity=serial.PARITY_NONE, timeout=None, stopbits=serial.STOPBITS_ONE)

def handle_serial_message():
    # codec encodes the end of a message through a 0x00
    message = SER.read_until(expected = b'\x00', size = None)
    
    if  len(message) < 5:
        print("Pi error message too short")

    #decode, remove 0x00 byte
    try:
        msgId, data = Codec.Decode(message[:-1], len(message) - 1)
    except cobs.DecodeError:
        print("invalid cobs message")
        EtHan.soar_publish("TELE_PI_ERROR", json.dumps({"error": "Received invalid cobs message"}))
        return

    #Process essage according to ID
    if msgId == Core.MessageID.MSG_TELEMETRY:
        process_telemetry_message(data)
    elif msgId == Core.MessageID.MSG_CONTROL:
        process_control_message(data)
    else:
        print("Pi error")
        EtHan.soar_publish("TELE_PI_ERROR", json.dumps({"error": "Received invalid MessageID"}))

def send_serial_message(message):
    #print("pre cobs message: ", message)
    #print(len(message))

    #encode
    buf = msg.SerializeToString()
    encBuf = Codec.Encode(buf, len(buf), Core.MessageID.MSG_COMMAND)

    #print("cobs message: ", encBuf)
    #print(len(encBuf))

    # Send the data to the serial port
    SER.write(encBuf)





# telemetry message
def process_telemetry_message(data):
    received_message = ProtoTele.TelemetryMessage()
    try:
        received_message.ParseFromString(data)
    except message.Decoprocess_control_messagedeError:
        print("cannot decode telemetry message")
        return

    if received_message.target == Core.NODE_RCU:
        message_type = received_message.WhichOneof('message')
        #print('========')
        #print(message_type)
        #print(received_message)
        #print('========')

        if(message_type != None):
            topic, jsnStr = ProtoParse.TELE_FUNCTION_DICTIONARY[message_type](received_message)
            EtHan.soar_publish(topic, jsnStr)
            return
        else:
            print("received invalid telemetry message type")
            EtHan.soar_publish("TELE_PI_ERROR", json.dumps({"error": "Invalid telemetry message type"}))

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
                MePa.TelO.tele_dmb_obj.current_state = ProtoParse.PROTO_STATE_TO_STRING[received_message.sys_state.rocket_state]
                EtHan.soar_publish("CONTROL_SYS_STATE", json.dumps({"dmb_state": str(MePa.TelO.tele_dmb_obj.current_state)}))

                #print(ProtoParse.PROTO_STATE_TO_STRING[received_message.sys_state.rocket_state])
        elif message_type == 'hb':
            print('hb: ', received_message.source)
        elif message_type == 'ping':
            if received_message.source == Core.NODE_DMB and received_message.ping.ping_response_sequence_num == DMB_SEQ_NUM:
                EtHan.soar_publish("TELE_PI_ERROR", '{"ping_status" : "ping from DMB received"}')
            elif received_message.source == Core.NODE_PBB and received_message.ping.ping_response_sequence_num == PBB_SEQ_NUM:
                EtHan.soar_publish("TELE_PI_ERROR", '{"ping_status" : "ping from PBB received"}')
            elif received_message.source == Core.NODE_SOB and received_message.ping.ping_response_sequence_num == SOB_SEQ_NUM:
                EtHan.soar_publish("TELE_PI_ERROR", '{"ping_status" : "ping from SOB received"}')
            else:
                EtHan.soar_publish("TELE_PI_ERROR", '{"ping_status" : "unknown ping received"}')
            print('we were pinged: ', received_message.source)
        elif message_type == 'ack':
            print('oh hey, we ack: ', received_message.source)
        elif message_type == 'nack':
            #add resend of message
            print('nack received, this is bad')


# placeholder in case the pi ever receives a command message
#def process_command_message(msg):