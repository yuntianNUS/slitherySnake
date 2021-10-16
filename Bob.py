from socket import *
import sys
import zlib

def BobApp():
    bobPort = int(sys.argv[1])
    bobSocket = socket(AF_INET, SOCK_DGRAM)
    bobSocket.bind(('', bobPort))
    currAckNum = 0
    alreadyReceived = []
    while True:
        receivedMessage, serverAddress = bobSocket.recvfrom(64)
        try:
            receivedMessageSplit = receivedMessage.split(b'|')
            if len(receivedMessageSplit) != 3:
                raise Exception

            checkSumHeader = receivedMessageSplit[0]
            if checkSumHeader[:2] != b'CS':
                raise Exception
            checkSumHeaderNumbers = checkSumHeader.lstrip(b'CS')
            
            seqNumHeader = receivedMessageSplit[1]
            seqNumberByte = seqNumHeader.lstrip(b'SEQ')
            if seqNumHeader[:3] != b'SEQ':
                raise Exception

            seqNumberInt = int(seqNumberByte)
            
            actualMessage = receivedMessageSplit[2]

            actualMessageCheckSum = zlib.crc32(actualMessage)

            if actualMessageCheckSum == int(checkSumHeaderNumbers.decode()):
                ackToAlice = b''.join([b'ACK',seqNumberByte]) #Alice will wait to see this ACK
                bobSocket.sendto(ackToAlice,serverAddress)
                if seqNumberInt > currAckNum:
                    currAckNum = seqNumberInt
                if receivedMessage not in alreadyReceived:
                    alreadyReceived.append(receivedMessage)
                    sys.stdout.write(actualMessage.decode())
                    sys.stdout.flush()
                
            else:
                raise Exception
        #end try
        except: # data corruption
            bobSocket.sendto(b''.join([b'ACK',str(currAckNum).encode()]), serverAddress)

if __name__ == "__main__":
    BobApp()