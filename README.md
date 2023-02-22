# SOAR Protocol

## Useful Info
#### Quick Generate
Run the [`GenerateProto.bat`](GenerateProto.bat) file to update the _C++ and _Python files
#### Manual Commands
 ```
 protoc --plugin=protoc-gen-eams=protoc-gen-eams.bat --eams_out=_C++ *.proto
 ```
 ```
 protoc --pyi_out=_Python --python_out=_Python *.proto
 ```

## Protocol Description
### Representation
- We use [ProtocolBuffers](https://developers.google.com/protocol-buffers) and the [EmbeddedProto](https://embeddedproto.com/) plugin for protobuf on our embedded systems to handle serialization.
### Transport
- We wrap Protobuf messages in the following format </br>
```
[MESSAGE_ID][PBUF_SIZE][PBUF_PAYLOAD][CHECKSUM]
```
```
[1_BYTE][2_BYTES][SIZE_BYTES][2_BYTES]
``` 
- Then we proceed to wrap the message inside [`COBS`](cobs.h) which delimits the end of each message with a `0x00`


## Installation (Windows)
### Auto Install
Run the [`QuickInstall.bat`](QuickInstall.bat) file with elevated privileges. </br>

### Manual Install
#### C++
 - The installation process can get quite involved in Windows, as we'll be using EmbeddedProto, we won't necessarily need protoc's regular C++ output.
 - Download or clone [EmbeddedProto](https://github.com/Embedded-AMS/EmbeddedProto) and run the script `setup.py` contained inside
 - Inside the respective C++ project, include the _C++ folder inside this directory
 - Run this to compile the protocolbuffers files:
 ```
 protoc --plugin=protoc-gen-eams=protoc-gen-eams.bat --eams_out=_C++ *.proto
 ```

<!--- Follow [this](https://github.com/protocolbuffers/protobuf/tree/main/python#installation). -->
#### Python 
 - Download [this](https://github.com/protocolbuffers/protobuf/releases/download/v21.12/protoc-21.12-win64.zip) and drag protoc.exe somewhere on PATH
 - Alternatively, run `choco install protoc` if you have Chocolatey package manager
 - Inside the respective Python project, include the _Python folder inside this directory.
 - Run this to compile the protocolbuffers files:
 ```
 protoc --pyi_out=_Python --python_out=_Python *.proto
 ```
    

## Recommendations
1. I recommend using VSCode to handle .proto files with the `vscode-proto3` extension
