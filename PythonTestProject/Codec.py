#
# FILE: Codec.py
# BRIEF: This file contains the codec class for the Command and Telemetry Protocol
# AUTHOR: Christopher Chan (cjchanx)
#

from cobs import cobs   # pip install cobs

# Constants and helpers
PROTO_CHKSUM_BYTES = 4
PROTO_MSGID_BYTES = 2

def GetCOBSOverhead(unencodedSize):
    return unencodedSize // 254 + 1

# Main class - import this class to use the codec
class Codec:
    @staticmethod
    def GetEncodedSize(unencodedSize):
        # The encoded size is the unencoded size + 1 byte for the message ID + COBS Overhead + 1 byte for the 0x00 delimiter
        return unencodedSize + 1 + GetCOBSOverhead(unencodedSize + 1) + 1

    @staticmethod
    def Encode(buf, len, msgId):
        # Make a new buffer encoded with just the message ID
        encodedBuf = bytearray(len+1)

        # We encode the message ID first
        encodedBuf[0] = msgId

        # Then we copy the rest of the buffer
        for i in range(0, len):
            encodedBuf[i+1] = buf[i]

        # Then we encode the whole thing in COBS
        cobsEncodedBuf = cobs.encode(encodedBuf)
        encodedBuf = bytearray(cobsEncodedBuf)

        # Add a 0x00 for delimiting the end of the message
        encodedBuf.append(0)

        return encodedBuf

    @staticmethod
    def Decode(buf, len):
        # Decode the buffer
        decodedBuf = cobs.decode(buf)

        # The first byte is the message ID
        msgId = decodedBuf[0]

        # The rest of the buffer is the data
        data = decodedBuf[1:]

        return msgId, data