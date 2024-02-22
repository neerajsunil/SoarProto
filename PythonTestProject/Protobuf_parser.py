# FILE: ProtobufParser.py
# BRIEF: This file contains the protobuf parser class for converting protobuf messages to JSON
#         and pushing telemetry messages to PocketBase

import os
import json
import time
# import serial
import supabase
import datetime
import threading
import CoreProto_pb2 as Core
import CommandMessage_pb2 as ProtoCmd
import ControlMessage_pb2 as ProtoCtrl
import TelemetryMessage_pb2 as ProtoTele


from realtime.connection import Socket
# from Configuration import *
# from LoadCell import LoadCell
# from TestStand import TestStand
# from DataCapture import data_capture
# from LabJackTVC import LabJack, DigitalOutput
# from DataCaptureStream import data_capture_stream
from google.protobuf.json_format import MessageToJson
# from VaneControlDBG import VaneThreadHandler, VaneControlDebug


class ProtobufParser:
    # FIXME: This is a temporary solution to the labjack and test_stand objects
    labjack = None
    test_stand = None
    ignitionOut = None
    # Attempt to initialize serial
    SER = None

    @staticmethod
    def flatten_json(json_data, parent_key='', separator='_'):
        """
            Flattens nested JSON object.

            Parameters:
                json_data (dict): The nested JSON object.
                parent_key (str): The parent key in case of recursion (default is '').
                separator (str): The separator to use between keys (default is '_').

            Returns:
                dict: The flattened JSON object.
        """
        items = {}
        for key in json_data:
            new_key = parent_key + separator + key if parent_key else key
            if isinstance(json_data[key], dict):
                items.update(ProtobufParser.flatten_json(json_data[key], new_key, separator=separator))
            else:
                items[new_key] = json_data[key]
        return items

    @staticmethod
    def parse_protobuf_to_json(protobuf_message):
        # Convert the protobuf message to a JSON string
        json_string = MessageToJson(protobuf_message, preserving_proto_field_name=True)
        return json_string

    @staticmethod
    def parse_serial_to_json(serialized_message, msg_id):
        '''
        Parse a serialized message to a JSON string

        Args:
            serialized_message: The serialized message
            msg_id: The message ID
        Throws:
            ValueError: If the message ID is invalid
        '''

        # Create message object based on message ID
        message = None
        if msg_id == Core.MessageID.MSG_COMMAND:
            message = ProtoCmd.CommandMessage()
        elif msg_id == Core.MessageID.MSG_TELEMETRY:
            message = ProtoTele.TelemetryMessage()
        elif msg_id == Core.MessageID.MSG_CONTROL:
            message = ProtoCtrl.ControlMessage()
        else:
            raise ValueError(f'Invalid message ID: {msg_id}')
        
        # Parse the serialized message
        message.ParseFromString(serialized_message)
        
        # Convert the message to JSON and print it
        json_string = ProtobufParser.parse_protobuf_to_json(message)
        return json_string

    # TODO: Add method to push JSON to DB
    @staticmethod
    def push_tele_json_to_database(client, json_data):
        '''
        Push a telemetry JSON message to DataBase

        Note: The third key in the JSON data is assumed to be the table name
        '''
    
        # Extract the table name from the JSON data
        table_name = list(json_data.keys())[2]
        
        # Flatten data to fix to table columns
        flattened_data = ProtobufParser.flatten_json(json_data[table_name])

        # print("Pushing to table: " + table_name + " data: ")
        print(flattened_data)
        
        # Push the JSON data to supabase using the correct schema
        data, count = client.table(table_name).insert(flattened_data).execute()


def generate_gps_serial():
    # Create a new GPS message
    gps_message = ProtoTele.GPS()

    # Latitude for Calgary
    gps_message.latitude.degrees = 51
    gps_message.latitude.minutes = int((0.0447 * 60))

    # Longitude for Calgary
    gps_message.longitude.degrees = -114
    gps_message.longitude.minutes = int((0.0719 * 60))

    gps_message.antenna_alt.altitude = 123
    gps_message.antenna_alt.unit = 1
    gps_message.geoidAltitude.altitude = 123
    gps_message.geoidAltitude.unit = 1
    gps_message.total_alt.altitude = 123
    gps_message.total_alt.unit = 1

    # Set the time to 2024-01-01T00:00:00Z
    gps_message.time = int(time.mktime(datetime.datetime(2024, 1, 1).timetuple()))

    # Wrap in TelemetryMessage
    telemetry_message = ProtoTele.TelemetryMessage()
    telemetry_message.coord.CopyFrom(gps_message)
    telemetry_message.source = Core.NODE_DMB
    telemetry_message.target = Core.NODE_RCU

    # Serialize the message
    serialized_message = telemetry_message.SerializeToString()
    return serialized_message

def generate_tvc_message():
    # Create a new GPS message
    vanes = ProtoTele.VanePosition()

    vanes.vane_profile = 0
    vanes.vane_1 = 0.5
    vanes.vane_2 = 0.5
    vanes.vane_3 = 0.5
    vanes.vane_4 = 0.5

    # Wrap in TelemetryMessage
    telemetry_message = ProtoTele.TelemetryMessage()
    telemetry_message.vanes.CopyFrom(vanes)
    telemetry_message.source = Core.NODE_DMB
    telemetry_message.target = Core.NODE_RCU

    # Serialize the message
    serialized_message = telemetry_message.SerializeToString()
    return serialized_message

def generate_imu_message():
    imu = ProtoTele.IMU()

    imu.accelx = 1000
    imu.accely = 1000
    imu.accelz = 1000

    imu.gyrox = 100
    imu.gyroy = 100
    imu.gyroz = 100

    imu.magx = 100
    imu.magy = 100
    imu.magz = 100

    # Wrap in TelemetryMessage
    telemetry_message = ProtoTele.TelemetryMessage()
    telemetry_message.imu.CopyFrom(imu)
    telemetry_message.source = Core.NODE_DMB
    telemetry_message.target = Core.NODE_RCU

    # Serialize the message
    serialized_message = telemetry_message.SerializeToString()
    return serialized_message

"""
def ignite_pulse(do: DigitalOutput, duration: float):
    print(f"FIO3 pulsing for {duration*1000}ms")
    do = DigitalOutput(labjack, "FIO3")
    do.write(1)
    time.sleep(duration)
    do.write(0)

# Start data capture in Stream mode
def option_data_capture_stream():
    data_capture_stream_thread = threading.Thread(target=data_capture_stream, args=(labjack, test_stand, test_stand.get_rate()))
    data_capture_stream_thread.start()

# Start data capture in Command-Response mode
def option_data_capture_cmd():

    data_capture_cmd_thread = threading.Thread(target=data_capture, args=(test_stand, test_stand.get_rate()))
    data_capture_cmd_thread.start()

# Stop data capture
def option_data_capture_stop():
    return

# Start ignition
def option_ignition_on():
    ignite_pulse(ignitionOut, 0.7)

# Stop ignition
def option_ignition_off():
    ignitionOut.write(0)

# Ignite stream
def option_ignite_stream():
    # Ignite, Stream (100ms), Replay on Z force > X
    reading_queue = None
    vth = None
    if SER is not None:
        vane_control_debug = VaneControlDebug(SER)
        vth = VaneThreadHandler(vane_control_debug, VANE_PROFILE_DIFFERENTIAL_Z_FORCE, REPLAY_VANE_PROFILE, True)
        reading_queue = vth.get_input_queue()
    
    # If the queue is None then pause here and notify of the failure
    if reading_queue is None and SER is not None:
        print("Error: Could not start the vane control thread. Please check the serial port.")
        input("Press Enter to continue...")
        return

    # Ignite
    ignitionOut.write(1)

    # Start the data capture in Stream mode
    data_capture_stream_thread = threading.Thread(target=data_capture_stream, args=(labjack, test_stand, test_stand.get_rate(), reading_queue))
    data_capture_stream_thread.start()
    
    # Cleanup
    ignitionOut.write(0)
    vth.stop()

# Ignite command
def option_ignite_command():
    # Ignite, Command-Response (100ms), Replay on Z force > X or timeout
    reading_queue = None
    vth = None
    if SER is not None:
        vane_control_debug = VaneControlDebug(SER)
        vth = VaneThreadHandler(vane_control_debug, VANE_PROFILE_DIFFERENTIAL_Z_FORCE, REPLAY_VANE_PROFILE, True)
        reading_queue = vth.get_input_queue()
    
    # If the queue is None then pause here and notify of the failure
    if reading_queue is None and vth is None:
        print("Error: Could not start the vane control thread. Please check the serial port.")
        input("Press Enter to continue...")
        return
        
    # Ignite
    ignitionOut.write(1)

    # Start the data capture in C-R mode
    data_capture_cmd_thread = threading.Thread(target=data_capture, args=(test_stand, test_stand.get_rate(), reading_queue))
    data_capture_cmd_thread.start()

    # Cleanup
    ignitionOut.write(0)
    vth.stop()

# Ignite replay stream
def option_ignite_replay_stream():
    # Ignite, Replay, Stream
    ignitionOut.write(1)

    # Start the data capture in Stream mode
    data_capture_stream_thread = threading.Thread(target=data_capture_stream, args=(labjack, test_stand, test_stand.get_rate()))
    data_capture_stream_thread.start()

    # Cleanup
    ignitionOut.write(0)

def setup_serial(com_port : str):
    # Setup serial port
    if SER is None:
        try:
            SER = serial.Serial(port=com_port, baudrate=115200, bytesize=8, parity=serial.PARITY_NONE, timeout=None, stopbits=serial.STOPBITS_ONE)
        except Exception as e:
            print(f"Error: Could not connect to serial port {com_port}. Please check the port, servo-command comms will be disabled. {e}")

    return SER
"""
# Function to handle new commands
def handle_new_command(payload):
    print("New command received")
    print(payload)

    try:
        new_cmd = payload['record']['cmd']
        if new_cmd == 'data_capture_stream':
            # option_data_capture_stream()
            print("Data capture stream")
        elif new_cmd == 'data_capture_cmd':
            # option_data_capture_cmd()
            print("Data capture cmd")
        elif new_cmd == 'data_capture_stop':
            # option_data_capture_stop()
            print("Data capture stop")
        elif new_cmd == 'ignition_on':
            # option_ignition_on()
            print("Ignition on")
        elif new_cmd == 'ignition_off':
            # option_ignition_off()
            print("Ignition off")
        elif new_cmd == 'ignite_stream':
            # option_ignite_stream()
            print("Ignite stream")
        elif new_cmd == 'ignite_command':
            # option_ignite_command()
            print("Ignite command")
        elif new_cmd == 'ignite_replay_stream':
            # option_ignite_replay_stream()
            print("Ignite replay stream")
        else:
            print(f'Invalid command: {new_cmd}')
    except Exception as e:
        print(f"Error: Could not parse command. {e}")

# Subscribe to real-time changes in the 'commands' table
def listen_for_commands(client, key):
    #start listening for commands
    s = Socket(client.realtime_url + f"/websocket?apikey={key}&vsn=1.0.0")
    s.connect()

    channel = s.set_channel("realtime:*")
    channel.join().on("INSERT", handle_new_command)
    s.listen()

if __name__ == "__main__":
    # Set up the LabJack

    """
    try:
        labjack = LabJack()
    except Exception as e:
        print("\033[91mError: Could not connect to LabJack. Please check the connection.\033[0m")
        input("Press Enter to exit...")
        exit(1)

    # Initialize the load cells
    lc_x = LoadCell(labjack, ANALOG_CHANNELS["LOAD_CELL_X"])
    lc_y = LoadCell(labjack, ANALOG_CHANNELS["LOAD_CELL_Y"])
    lc_z = LoadCell(labjack, ANALOG_CHANNELS["LOAD_CELL_Z"])
    lc_t = LoadCell(labjack, ANALOG_CHANNELS["LOAD_CELL_T"])
    lclist = [lc_x, lc_y, lc_z, lc_t]

    # Initialize the Test Stand
    test_stand = TestStand(lc_x, lc_y, lc_z, lc_t)

    # Initialize the digital output
    ignitionOut = DigitalOutput(labjack, "FIO3")

    SER = setup_serial(COM_PORT)
    """

    # Connect supabase
    url: str = "http://127.0.0.1:54321"
    key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"


    client = supabase.create_client(url, key)

    # Generate a GPS message
    serialized_message = generate_gps_serial()

    # Parse the serialized message to JSON
    parsed = ProtobufParser.parse_serial_to_json(serialized_message, Core.MessageID.MSG_TELEMETRY)

    # Push to database
    ProtobufParser.push_tele_json_to_database(client, json.loads(parsed))

    # Output
    # parsedJson = json.loads(parsed)

    # Generate a TVC message
    serialized_message = generate_tvc_message()

    # Parse the serialized message to JSON
    parsed = ProtobufParser.parse_serial_to_json(serialized_message, Core.MessageID.MSG_TELEMETRY)

    # Push to database
    ProtobufParser.push_tele_json_to_database(client, json.loads(parsed))
    # Output
    # print(parsed)

    # Generate an IMU message
    serialized_message = generate_imu_message()

    # Parse the serialized message to JSON
    parsed = ProtobufParser.parse_serial_to_json(serialized_message, Core.MessageID.MSG_TELEMETRY)

    # Push to database
    ProtobufParser.push_tele_json_to_database(client, json.loads(parsed))

    # Output
    # print(parsed)

    listen_for_commands(client, key)

