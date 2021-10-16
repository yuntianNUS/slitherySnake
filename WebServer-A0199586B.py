import sys
import os
from socket import *

keyValueStoreDict = {}
counterDict = {}

def main():
    serverPort = int(sys.argv[1])
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', serverPort))
    server_socket.listen() # server ready to receive  
    
    while True:
        while True:

            connectionSocket, clientAddr = server_socket.accept()
            request = b''
            while not request.endswith(b'  '):
                recv0 = connectionSocket.recv(1)
                request += recv0
                
                if request.endswith(b'  '): #full header gotten
                    processHeaderPlease(request, connectionSocket)
                    request = b''
                
                if not recv0:
                    if len(request) > 0:
                        processHeaderPlease(request, connectionSocket)
                        request = b''
                    connectionSocket.close()
                    break
            
            
def processHeaderPlease(request, connectionSocket): 
    requestSplit = request.split(b' ')
    httpMethod = requestSplit[0]
    httpMethodAscii = httpMethod.decode().upper()
    path = requestSplit[1]
    contentLength = 0
    value = b''
    contentMain = b''

    for i in range(2, len(requestSplit) - 1):
        eleStringLower = requestSplit[i].decode().lower()
        
        if eleStringLower == 'content-length':
            try:
                nextEleInt = int(requestSplit[i + 1])
                print("nextEleInt",nextEleInt)
                contentLength = nextEleInt      
                while nextEleInt > 0:
                    print("nextEleInt::",nextEleInt)
                    contentRecv = connectionSocket.recv(nextEleInt)
                    print("len(contentReceived)::",len(contentRecv))
                    nextEleInt -= len(contentRecv)
                    contentMain += contentRecv
                    print("contentMain is::::::",contentMain)
            except:
                continue
    
    value = b'content-length ' + str(contentLength).encode() + b'  ' + contentMain
    
    
    if path.split(b'/')[1] == b'key':
        clientMessage = processKeyRequest(httpMethodAscii, path.split(b'/')[2], value)
        print(clientMessage)
        connectionSocket.sendall(clientMessage)
    
    if path.split(b'/')[1] == b'counter':
        clientMessage = processCounterRequest(httpMethodAscii, path.split(b'/')[2])
        print(clientMessage)
        connectionSocket.sendall(clientMessage)

def processKeyRequest(inHttpMethod, recvKey, recvValue):
    global keyValueStoreDict

    if recvKey in keyValueStoreDict.keys():
        if inHttpMethod == "POST":
            keyValueStoreDict[recvKey] = recvValue
            # print("keyValueStoreDict: ", keyValueStoreDict)
            return (b'200 OK  ')

        elif inHttpMethod == "GET":
            # print("keyValueStoreDict: ", keyValueStoreDict)
            return (b'200 OK '  + keyValueStoreDict[recvKey])

        elif inHttpMethod == "DELETE":
            contentLengthHeader = keyValueStoreDict[recvKey].split(b'  ')[0]
            toSendContentBody = keyValueStoreDict[recvKey].split(b'  ')[1]       
            del keyValueStoreDict[recvKey]
            # print("keyValueStoreDict: ", keyValueStoreDict)
            return (b'200 OK ' + contentLengthHeader + b'  ' + toSendContentBody)
            
    
    elif recvKey not in keyValueStoreDict.keys() and inHttpMethod == "POST":
        keyValueStoreDict[recvKey] = recvValue
        # print("keyValueStoreDict: ", keyValueStoreDict)
        return (b'200 OK  ')
    
    return (b'404 NotFound  ')

def processCounterRequest(inHttpMethod, recvKey):
    global counterDict

    if inHttpMethod == "POST":
        if recvKey in counterDict.keys():
            ogIntValue = counterDict[recvKey]
            counterDict[recvKey] = ogIntValue + 1
        else:
            counterDict[recvKey] = 1
        return (b'200 OK  ')
    
    elif inHttpMethod == 'GET':
        value = b'0'
        
        if recvKey in counterDict.keys():
            return b'200 OK content-length 1  ' + str(counterDict[recvKey]).encode() 

        return b'200 OK content-length 1  ' + value

if __name__ == "__main__":
    main()

