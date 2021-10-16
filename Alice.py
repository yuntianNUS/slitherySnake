from socket import *
import sys
import zlib

messagesByteArray = []


def AliceApp():
    unreliPortNum = int(sys.argv[1])
    aliceSocket = socket(AF_INET, SOCK_DGRAM)
    timeout = 0.050
    ackNum = 0
    sequenceNum = 0
    sendBase = 0
    while True:
        payload = []
        while len(payload) < 44:
            msg = sys.stdin.buffer.read1(1)
            if msg == b'':
                break
            payload.append(msg)
        if len(payload) == 0 and sendBase == len(messagesByteArray):
            break
        else:
            if len(payload) > 0:
                messagesByteArray.append(b''.join(payload))

            while True:
                aToBmsg = generateMessage(sequenceNum)
                aliceSocket.sendto(aToBmsg, ('', unreliPortNum))
                aliceSocket.settimeout(timeout)
                try:
                    bobReply, serverAddress = aliceSocket.recvfrom(64)
                    ackLetters = bobReply[:3]
                    if ackLetters != b'ACK': #corrupt
                        raise Exception
                    ackNum = int(bobReply[3:].decode())
                    if ackNum == sequenceNum:  # steady
                        # bobAcks.append(ackNum)
                        sequenceNum += 1
                        sendBase += 1
                        break
                    else: #corrupt
                        raise Exception
                except:  # corrupted ACK or Timeout
                    continue  # stop and wait



def generateMessage(sequenceNumber):
    global messagesByteArray
    return b''.join([f'CS{zlib.crc32(messagesByteArray[sequenceNumber])}|'.encode(
    ), f'SEQ{sequenceNumber}|'.encode(), messagesByteArray[sequenceNumber]])


if __name__ == "__main__":
    AliceApp()
