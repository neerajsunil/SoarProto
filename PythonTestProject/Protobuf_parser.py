#Telemetry_parser.py

import time
import json
import paho.mqtt.client as mqtt
import ControlMessage_pb2 as Proto
import CommandMessage_pb2 as ProtoCmd
import TelemetryMessage_pb2 as ProtoTele
import CoreProto_pb2 as Core
import Publisher_nodered as pbnd

client = mqtt.Client()

PROTO_STATE_TO_STRING = {
Core.RS_ABORT : 'RS_ABORT',
Core.RS_ARM : 'RS_ARM',
Core.RS_BURN : 'RS_BURN',
Core.RS_COAST : 'RS_COAST',
Core.RS_DESCENT : 'RS_DESCENT',
Core.RS_FILL : 'RS_FILL',
Core.RS_IGNITION : 'RS_IGNITION',
Core.RS_LAUNCH : 'RS_LAUNCH',
Core.RS_NONE : 'RS_NONE',
Core.RS_PRELAUNCH : 'RS_PRELAUNCH',
Core.RS_RECOVERY : 'RS_RECOVERY'
}

STRING_TO_RSC_PROTO_COMMAND = {
	"RSC_ANY_TO_ABORT": ProtoCmd.DMBCommand.RSC_ANY_TO_ABORT,
	"RSC_ARM_CONFIRM_1": ProtoCmd.DMBCommand.RSC_ARM_CONFIRM_1,
	"RSC_ARM_CONFIRM_2": ProtoCmd.DMBCommand.RSC_ARM_CONFIRM_2,
	"RSC_BURN_TO_COAST": ProtoCmd.DMBCommand.RSC_BURN_TO_COAST,
	"RSC_CLOSE_DRAIN": ProtoCmd.DMBCommand.RSC_CLOSE_DRAIN,
	"RSC_CLOSE_VENT": ProtoCmd.DMBCommand.RSC_CLOSE_VENT,
	"RSC_COAST_TO_DESCENT": ProtoCmd.DMBCommand.RSC_COAST_TO_DESCENT,
	"RSC_DESCENT_TO_RECOVERY": ProtoCmd.DMBCommand.RSC_DESCENT_TO_RECOVERY,
	"RSC_FIRST_INVALID": ProtoCmd.DMBCommand.RSC_FIRST_INVALID,
	"RSC_GOTO_ARM": ProtoCmd.DMBCommand.RSC_GOTO_ARM,
	"RSC_GOTO_FILL": ProtoCmd.DMBCommand.RSC_GOTO_FILL,
	"RSC_GOTO_IGNITION": ProtoCmd.DMBCommand.RSC_GOTO_IGNITION,
	"RSC_GOTO_PRELAUNCH": ProtoCmd.DMBCommand.RSC_GOTO_PRELAUNCH,
	"RSC_IGNITION_TO_LAUNCH": ProtoCmd.DMBCommand.RSC_IGNITION_TO_LAUNCH,
	"RSC_LAUNCH_TO_BURN": ProtoCmd.DMBCommand.RSC_LAUNCH_TO_BURN,
	"RSC_MEV_CLOSE": ProtoCmd.DMBCommand.RSC_MEV_CLOSE,
	"RSC_OPEN_DRAIN": ProtoCmd.DMBCommand.RSC_OPEN_DRAIN,
	"RSC_OPEN_VENT": ProtoCmd.DMBCommand.RSC_OPEN_VENT,
	"RSC_POWER_TRANSITION_EXTERNAL": ProtoCmd.DMBCommand.RSC_POWER_TRANSITION_EXTERNAL,
	"RSC_POWER_TRANSITION_ONBOARD": ProtoCmd.DMBCommand.RSC_POWER_TRANSITION_ONBOARD,
	"RSC_NONE" : ProtoCmd.DMBCommand.RSC_NONE
}

STRING_TO_PBB_PROTO_COMMAND = {
	"PBB_NONE": ProtoCmd.PBBCommand.PBB_NONE,
	"PBB_OPEN_MEV": ProtoCmd.PBBCommand.PBB_OPEN_MEV,
	"PBB_CLOSE_MEV": ProtoCmd.PBBCommand.PBB_CLOSE_MEV,
    "PMB_LAST": ProtoCmd.PBBCommand.PMB_LAST,
}

STRING_TO_RCU_PROTO_COMMAND = {
	"RCU_NONE": ProtoCmd.RCUCommand.RCU_NONE,
    "RCU_TARE_NOS1_LOAD_CELL": ProtoCmd.RCUCommand.RCU_TARE_NOS1_LOAD_CELL,
    "RCU_TARE_NOS2_LOAD_CELL": ProtoCmd.RCUCommand.RCU_TARE_NOS2_LOAD_CELL,
    "RCU_CAL_NOS1_LOAD_CELL": ProtoCmd.RCUCommand.RCU_CALIBRATE_NOS1_LOAD_CELL,
    "RCU_CAL_NOS2_LOAD_CELL": ProtoCmd.RCUCommand.RCU_CALIBRATE_NOS2_LOAD_CELL,
	"RCU_OPEN_AC1": ProtoCmd.RCUCommand.RCU_OPEN_AC1,
    "RCU_CLOSE_AC1": ProtoCmd.RCUCommand.RCU_CLOSE_AC1,
	"RCU_OPEN_AC2": ProtoCmd.RCUCommand.RCU_OPEN_AC2,
    "RCU_CLOSE_AC2": ProtoCmd.RCUCommand.RCU_CLOSE_AC2,
    "RCU_OPEN_PBV1": ProtoCmd.RCUCommand.RCU_OPEN_PBV1,
	"RCU_CLOSE_PBV1": ProtoCmd.RCUCommand.RCU_CLOSE_PBV1,
    "RCU_OPEN_PBV2": ProtoCmd.RCUCommand.RCU_OPEN_PBV2,
    "RCU_CLOSE_PBV2": ProtoCmd.RCUCommand.RCU_CLOSE_PBV2,
	"RCU_OPEN_PBV3": ProtoCmd.RCUCommand.RCU_OPEN_PBV3,
    "RCU_CLOSE_PBV3": ProtoCmd.RCUCommand.RCU_CLOSE_PBV3,
    "RCU_OPEN_SOL1": ProtoCmd.RCUCommand.RCU_OPEN_SOL1,
    "RCU_CLOSE_SOL1": ProtoCmd.RCUCommand.RCU_CLOSE_SOL1,
    "RCU_OPEN_SOL2": ProtoCmd.RCUCommand.RCU_OPEN_SOL2,
    "RCU_CLOSE_SOL2": ProtoCmd.RCUCommand.RCU_CLOSE_SOL2,
    "RCU_CLOSE_SOL3": ProtoCmd.RCUCommand.RCU_CLOSE_SOL3,
    "RCU_OPEN_SOL4": ProtoCmd.RCUCommand.RCU_OPEN_SOL4,
    "RCU_CLOSE_SOL4": ProtoCmd.RCUCommand.RCU_CLOSE_SOL4,
    "RCU_OPEN_SOL5": ProtoCmd.RCUCommand.RCU_OPEN_SOL5,
    "RCU_CLOSE_SOL5": ProtoCmd.RCUCommand.RCU_CLOSE_SOL5,
    "RCU_OPEN_SOL6": ProtoCmd.RCUCommand.RCU_OPEN_SOL6,
    "RCU_CLOSE_SOL6": ProtoCmd.RCUCommand.RCU_CLOSE_SOL6,
    "RCU_OPEN_SOL7": ProtoCmd.RCUCommand.RCU_OPEN_SOL7,
    "RCU_CLOSE_SOL7": ProtoCmd.RCUCommand.RCU_CLOSE_SOL7,
    "RCU_OPEN_SOL8A": ProtoCmd.RCUCommand.RCU_OPEN_SOL8A,
    "RCU_CLOSE_SOL8A": ProtoCmd.RCUCommand.RCU_CLOSE_SOL8A,
    "RCU_OPEN_SOL8B": ProtoCmd.RCUCommand.RCU_OPEN_SOL8B,
    "RCU_CLOSE_SOL8B": ProtoCmd.RCUCommand.RCU_CLOSE_SOL8B,
    "RCU_IGNITE_PAD_BOX1": ProtoCmd.RCUCommand.RCU_IGNITE_PAD_BOX1,
    "RCU_IGNITE_PAD_BOX2": ProtoCmd.RCUCommand.RCU_IGNITE_PAD_BOX2,
    "RCU_LAST": ProtoCmd.RCUCommand.RCU_LAST
}

STRING_TO_SOB_PROTO_COMMAND = {
	"SOB_NONE": ProtoCmd.SOBCommand.SOB_NONE,
	"SOB_SLOW_SAMPLE_IR": ProtoCmd.SOBCommand.SOB_SLOW_SAMPLE_IR,
	"SOB_FAST_SAMPLE_IR": ProtoCmd.SOBCommand.SOB_FAST_SAMPLE_IR,
	"SOB_TARE_LOAD_CELL": ProtoCmd.SOBCommand.SOB_TARE_LOAD_CELL,
    "SOB_CALIBRATE_LOAD_CELL": ProtoCmd.SOBCommand.SOB_CALIBRATE_LOAD_CELL,
    "SOB_LAST": ProtoCmd.SOBCommand.SOB_LAST,
}

#TODO remove drain and vent command from allowed commands

ALLOWED_COMMANDS_FROM_STATE = {
    'RS_ABORT': ["RSC_ANY_TO_ABORT", "RSC_GOTO_PRELAUNCH", "RSC_CLOSE_DRAIN", "RSC_OPEN_DRAIN", "RSC_CLOSE_VENT", "RSC_OPEN_VENT"],
    'RS_ARM': ["RSC_ANY_TO_ABORT", "RSC_POWER_TRANSITION_ONBOARD", "RSC_POWER_TRANSITION_EXTERNAL", "RSC_GOTO_FILL", "RSC_GOTO_IGNITION", "RSC_OPEN_VENT", "RSC_CLOSE_VENT", "RSC_OPEN_DRAIN", "RSC_CLOSE_DRAIN", "RSC_MEV_CLOSE", "RSC_CLOSE_DRAIN", "RSC_OPEN_DRAIN", "RSC_CLOSE_VENT", "RSC_OPEN_VENT"],
    'RS_BURN': ["RSC_ANY_TO_ABORT", "RSC_BURN_TO_COAST", "RSC_CLOSE_DRAIN", "RSC_OPEN_DRAIN", "RSC_CLOSE_VENT", "RSC_OPEN_VENT"],
    'RS_COAST': ["RSC_ANY_TO_ABORT", "RSC_COAST_TO_DESCENT", "RSC_CLOSE_DRAIN", "RSC_OPEN_DRAIN", "RSC_CLOSE_VENT", "RSC_OPEN_VENT"],
    'RS_DESCENT': ["RSC_ANY_TO_ABORT", "RSC_DESCENT_TO_RECOVERY", "RSC_CLOSE_DRAIN", "RSC_OPEN_DRAIN", "RSC_CLOSE_VENT", "RSC_OPEN_VENT"],
    'RS_FILL': ["RSC_ANY_TO_ABORT", "RSC_ARM_CONFIRM_1", "RSC_ARM_CONFIRM_2", "RSC_GOTO_ARM", "RSC_GOTO_PRELAUNCH", "RSC_OPEN_VENT", "RSC_CLOSE_VENT", "RSC_OPEN_DRAIN", "RSC_CLOSE_DRAIN", "RSC_MEV_CLOSE", "RSC_CLOSE_DRAIN", "RSC_OPEN_DRAIN", "RSC_CLOSE_VENT", "RSC_OPEN_VENT"],
    'RS_IGNITION': ["RSC_ANY_TO_ABORT", "RSC_IGNITION_TO_LAUNCH", "RSC_GOTO_ARM", "RSC_CLOSE_DRAIN", "RSC_OPEN_DRAIN", "RSC_CLOSE_VENT", "RSC_OPEN_VENT"],
    'RS_LAUNCH': ["RSC_ANY_TO_ABORT", "RSC_LAUNCH_TO_BURN", "RSC_CLOSE_DRAIN", "RSC_OPEN_DRAIN", "RSC_CLOSE_VENT", "RSC_OPEN_VENT"],
    'RS_NONE': ["RSC_ANY_TO_ABORT", "RSC_CLOSE_DRAIN", "RSC_OPEN_DRAIN", "RSC_CLOSE_VENT", "RSC_OPEN_VENT"],
    'RS_PRELAUNCH': ["RSC_ANY_TO_ABORT", "RSC_GOTO_FILL", "RSC_OPEN_VENT", "RSC_CLOSE_VENT", "RSC_OPEN_DRAIN", "RSC_CLOSE_DRAIN", "RSC_MEV_CLOSE", "RSC_CLOSE_DRAIN", "RSC_OPEN_DRAIN", "RSC_CLOSE_VENT", "RSC_OPEN_VENT"],
    'RS_RECOVERY': ["RSC_ANY_TO_ABORT", "RSC_OPEN_VENT", "RSC_CLOSE_VENT", "RSC_OPEN_DRAIN", "RSC_CLOSE_DRAIN", "RSC_MEV_CLOSE", "RSC_CLOSE_DRAIN", "RSC_OPEN_DRAIN", "RSC_CLOSE_VENT", "RSC_OPEN_VENT"]
}

def coord_parse_json_send(msg):
    dmb_jsonStr_gps = json.dumps(pbnd.tele_dmb_obj.tele_gps(msg.coord.latitude.minutes, msg.coord.latitude.degrees,
                                                            msg.coord.longitude.minutes, msg.coord.longitude.degrees,
                                                            msg.coord.antenna_alt.altitude, msg.coord.antenna_alt.unit,
                                                            msg.coord.geoidAltitude.altitude, msg.coord.geoidAltitude.unit,
                                                            msg.coord.total_alt.altitude, msg.coord.total_alt.unit,
                                                            msg.coord.time))
    client.publish("TELE_DMB_GPS", dmb_jsonStr_gps)

def baro_parse_json_send(msg):
    dmb_jsonStr_baro = json.dumps(pbnd.tele_dmb_obj.tele_baro(msg.baro.baro_pressure, msg.baro.baro_temp))
    client.publish("TELE_DMB_BARO", dmb_jsonStr_baro)

def imu_parse_json_send(msg):
    accel = [msg.imu.accelx, msg.imu.accely, msg.imu.accelz]
    gyro = [msg.imu.gyrox, msg.imu.gyroy, msg.imu.gyroz]
    magn = [msg.imu.magx, msg.imu.magy, msg.imu.magz]
    dmb_jsonStr_imu = json.dumps(pbnd.tele_dmb_obj.tele_imu(accel, gyro, magn))
    client.publish("TELE_DMB_IMU", dmb_jsonStr_imu)

def bat_parse_json_send(msg):
    dmb_jsonStr_battery = json.dumps(pbnd.tele_dmb_obj.tele_battery(msg.bat.p_source, msg.bat.volt))
    client.publish("TELE_DMB_BATTERY", dmb_jsonStr_battery)

def flash_parse_json_send(msg):
    dmb_jsonStr_flash = json.dumps(pbnd.tele_dmb_obj.tele_flash(msg.flash.sector_address, msg.flash.logging_rate))
    client.publish("TELE_DMB_FLASH", dmb_jsonStr_flash)

def pressdmb_parse_json_send(msg):
    dmb_jsonStr_pressure = json.dumps(pbnd.tele_dmb_obj.tele_pressure(msg.pressdmb.upper_pv_pressure))
    client.publish("TELE_DMB_PRESSURE", dmb_jsonStr_pressure)

def presspbb_parse_json_send(msg):
    pbb_jsonStr_pressure = json.dumps(pbnd.tele_pbb_obj.tele_pressure(msg.presspbb.ib_pressure, msg.presspbb.lower_pv_pressure))
    client.publish("TELE_PBB_PRESSURE", pbb_jsonStr_pressure)

def temppbb_parse_json_send(msg):
    pbb_jsonStr_temperature = json.dumps(pbnd.tele_pbb_obj.tele_temp(msg.temppbb.ib_temperature, msg.temppbb.pv_temperature))
    client.publish("TELE_PBB_TEMP", pbb_jsonStr_temperature)

def gpio_parse_json_send(msg):
    pbb_jsonStr_gpio_status = json.dumps(pbnd.tele_pbb_obj.tele_gpio_status(msg.gpio.main_engine_valve_open, msg.gpio.vent_open, msg.gpio.drain_open))
    client.publish("TELE_PBB_GPIO", pbb_jsonStr_gpio_status)

def mevstate_parse_json_send(msg):
    pbb_jsonStr_mevstate = json.dumps(pbnd.tele_pbb_obj.tele_mevstate(msg.mevstate.mev_open))
    client.publish("TELE_PBB_MEVSTATE", pbb_jsonStr_mevstate)

def pressrcu_parse_json_send(msg):
    rcu_jsonStr_pressure = json.dumps(pbnd.tele_rcu_obj.tele_pressure(msg.pressrcu.pt1_pressure, msg.pressrcu.pt2_pressure, msg.pressrcu.pt3_pressure, msg.pressrcu.pt4_pressure))
    client.publish("TELE_RCU_PRESSURE", rcu_jsonStr_pressure)

def temprcu_parse_json_send(msg):
    rcu_jsonStr_temp = json.dumps(pbnd.tele_rcu_obj.tele_temp(msg.temprcu.tc1_temp, msg.temprcu.tc2_temp))
    client.publish("TELE_RCU_TEMP", rcu_jsonStr_temp)

def nos_parse_json_send(msg):
    rcu_jsonStr_nos_load_cell = json.dumps(pbnd.tele_rcu_obj.tele_nos_load_cell(msg.nos.nos1_mass, msg.nos.nos2_mass))
    client.publish("TELE_RCU_NOS", rcu_jsonStr_nos_load_cell)

def relay_parse_json_send(msg):
    rcu_jsonStr_relay_status = json.dumps(pbnd.tele_rcu_obj.tele_relay_status(msg.relay.ac1_open, msg.relay.ac2_open, 
                                                                              msg.relay.pbv1_open, msg.relay.pbv2_open, msg.relay.pbv3_open,
                                                                              msg.relay.sol1_open, msg.relay.sol2_open, msg.relay.sol3_open, msg.relay.sol4_open, msg.relay.sol5_open, msg.relay.sol6_open, msg.relay.sol7_open, msg.relay.sol8a_open, msg.relay.sol8b_open))
    #print(rcu_jsonStr_relay_status)
    client.publish("TELE_RCU_RELAY", rcu_jsonStr_relay_status)

def padbox_parse_json_send(msg):
    rcu_jsonStr_padbox_status = json.dumps(pbnd.tele_rcu_obj.tele_padbox_status(msg.padbox.cont1, msg.padbox.cont2))
    client.publish("TELE_RCU_PADBOX", rcu_jsonStr_padbox_status)

def lr_parse_json_send(msg):
    sob_jsonStr_lr_load_cell = json.dumps(pbnd.tele_sob_obj.tele_lr_load_cell(msg.lr.rocket_mass))
    client.publish("TELE_SOB_LOAD_CELL", sob_jsonStr_lr_load_cell)

def tempsob_parse_json_send(msg):
    sob_jsonStr_temp = json.dumps(pbnd.tele_sob_obj.tele_temp(msg.tempsob.tc1_temp, msg.tempsob.tc2_temp))
    client.publish("TELE_SOB_TEMP", sob_jsonStr_temp)

def irtemp_parse_json_send(msg):
    sob_jsonStr_irtemp = json.dumps(pbnd.tele_sob_obj.tele_temp(msg.irtemp.ambient_temp, msg.irtemp.object_temp))
    client.publish("TELE_SOB_IRTEMP", sob_jsonStr_irtemp)

TELE_FUNCTION_DICTIONARY = {
	"coord": coord_parse_json_send,
	"baro": baro_parse_json_send,
	"imu": imu_parse_json_send,
	"bat": bat_parse_json_send,
	"flash": flash_parse_json_send,
	"pressdmb": pressdmb_parse_json_send,
    "presspbb": presspbb_parse_json_send,
	"temppbb": temppbb_parse_json_send,
	"gpio": gpio_parse_json_send,
    "mevstate": mevstate_parse_json_send,
	"pressrcu": pressrcu_parse_json_send,
	"temprcu": temprcu_parse_json_send,
	"nos": nos_parse_json_send,
	"relay": relay_parse_json_send,
	"padbox": padbox_parse_json_send,
	"lr": lr_parse_json_send,
	"tempsob": tempsob_parse_json_send,
    "irtemp": irtemp_parse_json_send
}

'''

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

'''
