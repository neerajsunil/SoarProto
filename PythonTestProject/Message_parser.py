import lib.ControlMessage_pb2 as ProtoCtr
import lib.CommandMessage_pb2 as ProtoCmd
import lib.TelemetryMessage_pb2 as ProtoTele
import lib.CoreProto_pb2 as Core
import Protobuf_parser as ProtoParse
import json

# Constants
PASSPHRASE = '1'
DMB_SEQ_NUM = 10
PBB_SEQ_NUM = 20
SOB_SEQ_NUM = 30

# Globals
sequence_number = 1

def send_command_msg(data_dictionary):
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
            EtHan.soar_publish("TELE_PI_ERROR", json.dumps({"error": "Invalid Passphrase"}))
            return False

        if command not in ProtoParse.ALLOWED_COMMANDS_FROM_STATE[TelO.tele_dmb_obj.current_state]:
            EtHan.soar_publish("TELE_PI_ERROR", json.dumps({"error": "Invalid RSC Command"}))
            return False

        msg.dmb_command.command_enum = dmb_command
        msg.target = Core.NODE_DMB
        SeHan.send_serial_message(msg)
        return True

    pbb_command = ProtoParse.STRING_TO_PBB_PROTO_COMMAND.get(command)

    if pbb_command != None:
        msg.pbb_command.command_enum = pbb_command
        msg.target = Core.NODE_PBB
        SeHan.send_serial_message(msg)
        return True

    rcu_command = ProtoParse.STRING_TO_RCU_PROTO_COMMAND.get(command)

    if rcu_command != None:
        if rcu_command == ProtoCmd.RCUCommand.RCU_IGNITE_PAD_BOX1 or rcu_command == ProtoCmd.RCUCommand.RCU_IGNITE_PAD_BOX2:
            if TelO.tele_dmb_obj.current_state != "RS_LAUNCH" and TelO.tele_dmb_obj.current_state != "RS_ARM" and TelO.tele_dmb_obj.current_state != "RS_TEST":
                EtHan.soar_publish("TELE_PI_ERROR", json.dumps({"error": "Cant ignite on: " + str(TelO.tele_dmb_obj.current_state)}))
                return False

        msg.rcu_command.command_enum = rcu_command
        msg.target = Core.NODE_RCU
        SeHan.send_serial_message(msg)
        return True

	# if rcu command is sol8a, then send also send the opposite command for the sol8b & vice versa

    sob_command = ProtoParse.STRING_TO_SOB_PROTO_COMMAND.get(command)

    if sob_command != None:
        msg.sob_command.command_enum = sob_command
        msg.target = Core.NODE_SOB
        SeHan.send_serial_message(msg)
        return True

    pi_command = ProtoParse.STRING_TO_PI_COMMAND.get(command)

    if pi_command != None:
        ProtoParse.STRING_TO_PI_COMMAND_FUNCTION.get(pi_command)(float(data_dictionary["passphrase"]))
        return False

    EtHan.soar_publish("TELE_PI_ERROR", json.dumps({"error": "Invalid Command"}))
    return False

def send_ack_message(msg):
    ack_msg = ProtoCmd.ControlMessage()
    ack_msg.source = Core.NODE_RCU
    ack_msg.target = msg.source
    ack_msg.message_id = Core.MSG_CONTROL
    ack_msg.source_sequence_number = 0
    ack_msg.ack.acking_msg_id = msg.message_id
    ack_msg.ack.acking_msg_source = Core.NODE_RCU
    ack_msg.ack.acking_sequence_num = msg.source_sequence_number
    
    SeHan.send_serial_message(msg)

def send_ping_message(target):
    global sequence_number

    #create message  
    msg = ProtoCtr.ControlMessage()
    msg.source = Core.NODE_RCU
    msg.source_sequence_num = sequence_number
    sequence_number = sequence_number + 1
    ping = ProtoCtr.Ping()

    if target == "DMB":
        msg.target == Core.NODE_DMB
        ping.ping_ack_id = Core.MSG_CONTROL
        ping.ping_response_sequence_num = DMB_SEQ_NUM
        ping.sys_state_response_required = True
    elif target == "PBB":
        msg.target == Core.NODE_PBB
        ping.ping_ack_id = Core.MSG_CONTROL
        ping.ping_response_sequence_num = PBB_SEQ_NUM
        ping.sys_state_response_required = False
    elif target == "SOB":
        msg.target == Core.NODE_SOB
        ping.ping_ack_id = Core.MSG_CONTROL
        ping.ping_response_sequence_num = SOB_SEQ_NUM
        ping.sys_state_response_required = False

    msg.ping.CopyFrom(ping)

    SeHan.send_serial_message(msg)

def send_heartbeat_msg(target):
    msg = ProtoCtr.ControlMessage()
    msg.source = Core.NODE_RCU
    msg.target = target
    foo = ProtoCtr.Heartbeat()
    msg.hb.CopyFrom(foo)

    SeHan.send_serial_message(msg)