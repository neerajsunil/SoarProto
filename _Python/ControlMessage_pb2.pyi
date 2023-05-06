import CoreProto_pb2 as _CoreProto_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControlMessage(_message.Message):
    __slots__ = ["source", "target", "message_id", "source_sequence_num", "ack", "nack", "ping", "hb", "sys_state"]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_SEQUENCE_NUM_FIELD_NUMBER: _ClassVar[int]
    ACK_FIELD_NUMBER: _ClassVar[int]
    NACK_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    HB_FIELD_NUMBER: _ClassVar[int]
    SYS_STATE_FIELD_NUMBER: _ClassVar[int]
    source: _CoreProto_pb2.Node
    target: _CoreProto_pb2.Node
    message_id: _CoreProto_pb2.MessageID
    source_sequence_num: int
    ack: AckNack
    nack: AckNack
    ping: Ping
    hb: Heartbeat
    sys_state: SystemState
    def __init__(self, source: _Optional[_Union[_CoreProto_pb2.Node, str]] = ..., target: _Optional[_Union[_CoreProto_pb2.Node, str]] = ..., message_id: _Optional[_Union[_CoreProto_pb2.MessageID, str]] = ..., source_sequence_num: _Optional[int] = ..., ack: _Optional[_Union[AckNack, _Mapping]] = ..., nack: _Optional[_Union[AckNack, _Mapping]] = ..., ping: _Optional[_Union[Ping, _Mapping]] = ..., hb: _Optional[_Union[Heartbeat, _Mapping]] = ..., sys_state: _Optional[_Union[SystemState, _Mapping]] = ...) -> None: ...

class AckNack(_message.Message):
    __slots__ = ["acking_msg_source", "acking_msg_id", "acking_sequence_num"]
    ACKING_MSG_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ACKING_MSG_ID_FIELD_NUMBER: _ClassVar[int]
    ACKING_SEQUENCE_NUM_FIELD_NUMBER: _ClassVar[int]
    acking_msg_source: _CoreProto_pb2.Node
    acking_msg_id: _CoreProto_pb2.MessageID
    acking_sequence_num: int
    def __init__(self, acking_msg_source: _Optional[_Union[_CoreProto_pb2.Node, str]] = ..., acking_msg_id: _Optional[_Union[_CoreProto_pb2.MessageID, str]] = ..., acking_sequence_num: _Optional[int] = ...) -> None: ...

class Ping(_message.Message):
    __slots__ = ["ping_ack_id", "ping_response_sequence_num", "sys_state_response_required"]
    PING_ACK_ID_FIELD_NUMBER: _ClassVar[int]
    PING_RESPONSE_SEQUENCE_NUM_FIELD_NUMBER: _ClassVar[int]
    SYS_STATE_RESPONSE_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    ping_ack_id: int
    ping_response_sequence_num: int
    sys_state_response_required: bool
    def __init__(self, ping_ack_id: _Optional[int] = ..., ping_response_sequence_num: _Optional[int] = ..., sys_state_response_required: bool = ...) -> None: ...

class Heartbeat(_message.Message):
    __slots__ = ["hb_response_sequence_num"]
    HB_RESPONSE_SEQUENCE_NUM_FIELD_NUMBER: _ClassVar[int]
    hb_response_sequence_num: int
    def __init__(self, hb_response_sequence_num: _Optional[int] = ...) -> None: ...

class SystemState(_message.Message):
    __slots__ = ["sys_state", "rocket_state"]
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        SYS_INVALID: _ClassVar[SystemState.State]
        SYS_BOOTUP_COMPLETE: _ClassVar[SystemState.State]
        SYS_ASSERT_FAILURE_RESET: _ClassVar[SystemState.State]
        SYS_UNCAUGHT_RESET: _ClassVar[SystemState.State]
        SYS_NORMAL_OPERATION: _ClassVar[SystemState.State]
    SYS_INVALID: SystemState.State
    SYS_BOOTUP_COMPLETE: SystemState.State
    SYS_ASSERT_FAILURE_RESET: SystemState.State
    SYS_UNCAUGHT_RESET: SystemState.State
    SYS_NORMAL_OPERATION: SystemState.State
    SYS_STATE_FIELD_NUMBER: _ClassVar[int]
    ROCKET_STATE_FIELD_NUMBER: _ClassVar[int]
    sys_state: SystemState.State
    rocket_state: _CoreProto_pb2.RocketState
    def __init__(self, sys_state: _Optional[_Union[SystemState.State, str]] = ..., rocket_state: _Optional[_Union[_CoreProto_pb2.RocketState, str]] = ...) -> None: ...
