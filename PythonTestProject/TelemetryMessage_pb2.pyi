import CoreProto_pb2 as _CoreProto_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TelemetryMessage(_message.Message):
    __slots__ = ["message_id", "placeholder", "source", "target"]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PLACEHOLDER_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    message_id: _CoreProto_pb2.MessageID
    placeholder: int
    source: _CoreProto_pb2.Node
    target: _CoreProto_pb2.Node
    def __init__(self, source: _Optional[_Union[_CoreProto_pb2.Node, str]] = ..., target: _Optional[_Union[_CoreProto_pb2.Node, str]] = ..., message_id: _Optional[_Union[_CoreProto_pb2.MessageID, str]] = ..., placeholder: _Optional[int] = ...) -> None: ...