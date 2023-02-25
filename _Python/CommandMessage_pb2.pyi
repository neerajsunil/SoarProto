import CoreProto_pb2 as _CoreProto_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommandMessage(_message.Message):
    __slots__ = ["dmb_command", "message_id", "pmb_command", "source", "source_sequence_num", "target"]
    DMB_COMMAND_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PMB_COMMAND_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_SEQUENCE_NUM_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    dmb_command: DMBCommand
    message_id: int
    pmb_command: PMBCommand
    source: _CoreProto_pb2.Node
    source_sequence_num: int
    target: _CoreProto_pb2.Node
    def __init__(self, source: _Optional[_Union[_CoreProto_pb2.Node, str]] = ..., target: _Optional[_Union[_CoreProto_pb2.Node, str]] = ..., message_id: _Optional[int] = ..., source_sequence_num: _Optional[int] = ..., dmb_command: _Optional[_Union[DMBCommand, _Mapping]] = ..., pmb_command: _Optional[_Union[PMBCommand, _Mapping]] = ...) -> None: ...

class DMBCommand(_message.Message):
    __slots__ = ["command_enum"]
    class Command(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    COMMAND_ENUM_FIELD_NUMBER: _ClassVar[int]
    RSC_ANY_TO_ABORT: DMBCommand.Command
    RSC_ARM_CONFIRM_1: DMBCommand.Command
    RSC_ARM_CONFIRM_2: DMBCommand.Command
    RSC_BURN_TO_COAST: DMBCommand.Command
    RSC_CLOSE_DRAIN: DMBCommand.Command
    RSC_CLOSE_VENT: DMBCommand.Command
    RSC_COAST_TO_DESCENT: DMBCommand.Command
    RSC_DESCENT_TO_RECOVERY: DMBCommand.Command
    RSC_FIRST_INVALID: DMBCommand.Command
    RSC_GOTO_ARM: DMBCommand.Command
    RSC_GOTO_FILL: DMBCommand.Command
    RSC_GOTO_IGNITION: DMBCommand.Command
    RSC_GOTO_PRELAUNCH: DMBCommand.Command
    RSC_IGNITION_TO_LAUNCH: DMBCommand.Command
    RSC_LAUNCH_TO_BURN: DMBCommand.Command
    RSC_MEV_CLOSE: DMBCommand.Command
    RSC_NONE: DMBCommand.Command
    RSC_OPEN_DRAIN: DMBCommand.Command
    RSC_OPEN_VENT: DMBCommand.Command
    RSC_POWER_TRANSITION_EXTERNAL: DMBCommand.Command
    RSC_POWER_TRANSITION_ONBOARD: DMBCommand.Command
    command_enum: DMBCommand.Command
    def __init__(self, command_enum: _Optional[_Union[DMBCommand.Command, str]] = ...) -> None: ...

class PMBCommand(_message.Message):
    __slots__ = ["command_enum"]
    class Command(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    COMMAND_ENUM_FIELD_NUMBER: _ClassVar[int]
    PMB_CLOSE_MEV: PMBCommand.Command
    PMB_LAST: PMBCommand.Command
    PMB_NONE: PMBCommand.Command
    PMB_OPEN_MEV: PMBCommand.Command
    command_enum: PMBCommand.Command
    def __init__(self, command_enum: _Optional[_Union[PMBCommand.Command, str]] = ...) -> None: ...
