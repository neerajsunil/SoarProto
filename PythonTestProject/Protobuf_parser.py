# FILE: ProtobufParser.py
# BRIEF: This file contains the protobuf parser class for converting protobuf messages to JSON
#         and pushing telemetry messages to PocketBase

import os, sys

import json
from supabase import create_client, Client
from google.protobuf.json_format import MessageToJson
import ControlMessage_pb2 as ProtoCtrl
import CommandMessage_pb2 as ProtoCmd
import TelemetryMessage_pb2 as ProtoTele
import CoreProto_pb2 as Core


class ProtobufParser:
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
    def push_tele_json_to_database(client: Client, json_data):
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

# Example code
import time, datetime

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


if __name__ == "__main__":
    # Connect supabase
    url: str = ""
    key: str = ""
    supabase: Client = create_client(url, key)

    # Generate a GPS message
    serialized_message = generate_gps_serial()

    # Parse the serialized message to JSON
    parsed = ProtobufParser.parse_serial_to_json(serialized_message, Core.MessageID.MSG_TELEMETRY)

    # Push to database
    ProtobufParser.push_tele_json_to_database(supabase, json.loads(parsed))

    # Output
    # parsedJson = json.loads(parsed)

    # Generate a TVC message
    serialized_message = generate_tvc_message()

    # Parse the serialized message to JSON
    parsed = ProtobufParser.parse_serial_to_json(serialized_message, Core.MessageID.MSG_TELEMETRY)

    # Push to database
    ProtobufParser.push_tele_json_to_database(supabase, json.loads(parsed))
    # Output
    # print(parsed)

    # Generate an IMU message
    serialized_message = generate_imu_message()

    # Parse the serialized message to JSON
    parsed = ProtobufParser.parse_serial_to_json(serialized_message, Core.MessageID.MSG_TELEMETRY)

    # Push to database
    ProtobufParser.push_tele_json_to_database(supabase, json.loads(parsed))

    # Output
    # print(parsed)

