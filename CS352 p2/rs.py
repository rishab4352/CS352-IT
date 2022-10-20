import sys
import socket as mysoc

def newSocket():
    try: 
        ret_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print ("[rs]: socket created")
    except mysoc.error as err: 
        print ("[rs]: Could not create socket \n Error: " + str(err))
    return ret_socket


def rs():

    rsSocket = newSocket()
    ts1Socket = newSocket()
    ts2Socket = newSocket()

    rsBind = ("", int(sys.argv[1])) 
    ts1Bind = (str(sys.argv[2]),int(sys.argv[3]))
    ts2Bind = (str(sys.argv[4]),int(sys.argv[5]))
    
    rsSocket.bind(rsBind)
    ts1Socket.connect(ts1Bind)
    ts2Socket.connect(ts2Bind)

    rsSocket.listen(5)
    ts1Socket.settimeout(5)
    ts2Socket.settimeout(5)

    clientSocket, addr = rsSocket.accept()
    print('[rs}: Got a connection request from: ' , addr)

    while True:
        data = clientSocket.recv(4096).decode("utf-8").strip()
        if not data:
            break
        print("[rs]: Received from Client: " + data)

        ts1Socket.send(data.encode("utf-8"))
        ts2Socket.send(data.encode("utf-8"))

        try:
            ts1Data = ts1Socket.recv(4096).decode("utf-8")
            print("[rs]: Data from [TS1]: " + ts1Data +"IN")
            clientSocket.send(ts1Data.encode('utf-8'))
        except mysoc.timeout:
            print("[rs]: No response from [TS1]")
            try:
                ts2Data = ts2Socket.recv(4096).decode("utf-8")
                print("[rs]: Data from [TS2]: " + ts2Data +"IN")
                clientSocket.send(ts2Data.encode("utf-8"))
            except mysoc.timeout:
                print("[rs]: No response from [TS2]")
                err_str = data + " - TIMED OUT"
                clientSocket.send(err_str.encode("utf-8"))

    rsSocket.close()
    ts1Socket.close()
    ts2Socket.close()
    exit()

rs()