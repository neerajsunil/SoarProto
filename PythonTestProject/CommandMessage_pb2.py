# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: CommandMessage.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import CoreProto_pb2 as CoreProto__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x43ommandMessage.proto\x12\x05Proto\x1a\x0f\x43oreProto.proto\"\xc0\x02\n\x0e\x43ommandMessage\x12\x1b\n\x06source\x18\x01 \x01(\x0e\x32\x0b.Proto.Node\x12\x1b\n\x06target\x18\x02 \x01(\x0e\x32\x0b.Proto.Node\x12$\n\nmessage_id\x18\x03 \x01(\x0e\x32\x10.Proto.MessageID\x12\x1b\n\x13source_sequence_num\x18\x04 \x01(\r\x12(\n\x0b\x64mb_command\x18\x05 \x01(\x0b\x32\x11.Proto.DMBCommandH\x00\x12(\n\x0bpbb_command\x18\x06 \x01(\x0b\x32\x11.Proto.PBBCommandH\x00\x12(\n\x0brcu_command\x18\x07 \x01(\x0b\x32\x11.Proto.RCUCommandH\x00\x12(\n\x0bsob_command\x18\x08 \x01(\x0b\x32\x11.Proto.SOBCommandH\x00\x42\t\n\x07message\"\x8d\x05\n\nDMBCommand\x12/\n\x0c\x63ommand_enum\x18\x01 \x01(\x0e\x32\x19.Proto.DMBCommand.Command\"\xcd\x04\n\x07\x43ommand\x12\x15\n\x11RSC_FIRST_INVALID\x10\x00\x12\x14\n\x10RSC_ANY_TO_ABORT\x10\x01\x12\x11\n\rRSC_OPEN_VENT\x10\x02\x12\x12\n\x0eRSC_CLOSE_VENT\x10\x03\x12\x12\n\x0eRSC_OPEN_DRAIN\x10\x04\x12\x13\n\x0fRSC_CLOSE_DRAIN\x10\x05\x12\x11\n\rRSC_MEV_CLOSE\x10\x06\x12\x11\n\rRSC_GOTO_FILL\x10\x07\x12\x15\n\x11RSC_ARM_CONFIRM_1\x10\x08\x12\x15\n\x11RSC_ARM_CONFIRM_2\x10\t\x12\x10\n\x0cRSC_GOTO_ARM\x10\n\x12\x16\n\x12RSC_GOTO_PRELAUNCH\x10\x0b\x12 \n\x1cRSC_POWER_TRANSITION_ONBOARD\x10\x0c\x12!\n\x1dRSC_POWER_TRANSITION_EXTERNAL\x10\r\x12\x15\n\x11RSC_GOTO_IGNITION\x10\x0e\x12\x1a\n\x16RSC_IGNITION_TO_LAUNCH\x10\x0f\x12\x16\n\x12RSC_LAUNCH_TO_BURN\x10\x10\x12\x15\n\x11RSC_BURN_TO_COAST\x10\x11\x12\x18\n\x14RSC_COAST_TO_DESCENT\x10\x12\x12\x1b\n\x17RSC_DESCENT_TO_RECOVERY\x10\x13\x12\x11\n\rRSC_GOTO_TEST\x10\x14\x12\x15\n\x11RSC_TEST_MEV_OPEN\x10\x15\x12\x17\n\x13RSC_TEST_MEV_ENABLE\x10\x16\x12\x18\n\x14RSC_TEST_MEV_DISABLE\x10\x17\x12\x0c\n\x08RSC_NONE\x10\x18\"\x89\x01\n\nPBBCommand\x12/\n\x0c\x63ommand_enum\x18\x01 \x01(\x0e\x32\x19.Proto.PBBCommand.Command\"J\n\x07\x43ommand\x12\x0c\n\x08PBB_NONE\x10\x00\x12\x10\n\x0cPBB_OPEN_MEV\x10\x01\x12\x11\n\rPBB_CLOSE_MEV\x10\x02\x12\x0c\n\x08PMB_LAST\x10\x05\"\xe1\x01\n\nSOBCommand\x12/\n\x0c\x63ommand_enum\x18\x01 \x01(\x0e\x32\x19.Proto.SOBCommand.Command\x12\x15\n\rcommand_param\x18\x02 \x01(\x05\"\x8a\x01\n\x07\x43ommand\x12\x0c\n\x08SOB_NONE\x10\x00\x12\x16\n\x12SOB_SLOW_SAMPLE_IR\x10\x01\x12\x16\n\x12SOB_FAST_SAMPLE_IR\x10\x02\x12\x16\n\x12SOB_TARE_LOAD_CELL\x10\x03\x12\x1b\n\x17SOB_CALIBRATE_LOAD_CELL\x10\x04\x12\x0c\n\x08SOB_LAST\x10\x05\"\xfc\x06\n\nRCUCommand\x12/\n\x0c\x63ommand_enum\x18\x01 \x01(\x0e\x32\x19.Proto.RCUCommand.Command\x12\x15\n\rcommand_param\x18\x02 \x01(\x05\"\xa5\x06\n\x07\x43ommand\x12\x0c\n\x08RCU_NONE\x10\x00\x12\x10\n\x0cRCU_OPEN_AC1\x10\x03\x12\x11\n\rRCU_CLOSE_AC1\x10\x04\x12\x10\n\x0cRCU_OPEN_AC2\x10\x05\x12\x11\n\rRCU_CLOSE_AC2\x10\x06\x12\x11\n\rRCU_OPEN_PBV1\x10\x07\x12\x12\n\x0eRCU_CLOSE_PBV1\x10\x08\x12\x11\n\rRCU_OPEN_PBV2\x10\t\x12\x12\n\x0eRCU_CLOSE_PBV2\x10\n\x12\x11\n\rRCU_OPEN_PBV3\x10\x0b\x12\x12\n\x0eRCU_CLOSE_PBV3\x10\x0c\x12\x11\n\rRCU_OPEN_SOL1\x10\r\x12\x12\n\x0eRCU_CLOSE_SOL1\x10\x0e\x12\x11\n\rRCU_OPEN_SOL2\x10\x0f\x12\x12\n\x0eRCU_CLOSE_SOL2\x10\x10\x12\x11\n\rRCU_OPEN_SOL3\x10\x11\x12\x12\n\x0eRCU_CLOSE_SOL3\x10\x12\x12\x11\n\rRCU_OPEN_SOL4\x10\x13\x12\x12\n\x0eRCU_CLOSE_SOL4\x10\x14\x12\x11\n\rRCU_OPEN_SOL5\x10\x15\x12\x12\n\x0eRCU_CLOSE_SOL5\x10\x16\x12\x11\n\rRCU_OPEN_SOL6\x10\x17\x12\x12\n\x0eRCU_CLOSE_SOL6\x10\x18\x12\x11\n\rRCU_OPEN_SOL7\x10\x19\x12\x12\n\x0eRCU_CLOSE_SOL7\x10\x1a\x12\x12\n\x0eRCU_OPEN_SOL8A\x10\x1b\x12\x13\n\x0fRCU_CLOSE_SOL8A\x10\x1c\x12\x12\n\x0eRCU_OPEN_SOL8B\x10\x1d\x12\x13\n\x0fRCU_CLOSE_SOL8B\x10\x1e\x12\x1b\n\x17RCU_TARE_NOS1_LOAD_CELL\x10!\x12\x1b\n\x17RCU_TARE_NOS2_LOAD_CELL\x10\"\x12 \n\x1cRCU_CALIBRATE_NOS1_LOAD_CELL\x10#\x12 \n\x1cRCU_CALIBRATE_NOS2_LOAD_CELL\x10$\x12\x17\n\x13RCU_IGNITE_PAD_BOX1\x10\x1f\x12\x17\n\x13RCU_IGNITE_PAD_BOX2\x10 \x12\x15\n\x11RCU_KILL_PAD_BOX1\x10%\x12\x15\n\x11RCU_KILL_PAD_BOX2\x10&\x12\x0c\n\x08RCU_LAST\x10\'b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'CommandMessage_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _COMMANDMESSAGE._serialized_start=49
  _COMMANDMESSAGE._serialized_end=369
  _DMBCOMMAND._serialized_start=372
  _DMBCOMMAND._serialized_end=1025
  _DMBCOMMAND_COMMAND._serialized_start=436
  _DMBCOMMAND_COMMAND._serialized_end=1025
  _PBBCOMMAND._serialized_start=1028
  _PBBCOMMAND._serialized_end=1165
  _PBBCOMMAND_COMMAND._serialized_start=1091
  _PBBCOMMAND_COMMAND._serialized_end=1165
  _SOBCOMMAND._serialized_start=1168
  _SOBCOMMAND._serialized_end=1393
  _SOBCOMMAND_COMMAND._serialized_start=1255
  _SOBCOMMAND_COMMAND._serialized_end=1393
  _RCUCOMMAND._serialized_start=1396
  _RCUCOMMAND._serialized_end=2288
  _RCUCOMMAND_COMMAND._serialized_start=1483
  _RCUCOMMAND_COMMAND._serialized_end=2288
# @@protoc_insertion_point(module_scope)
