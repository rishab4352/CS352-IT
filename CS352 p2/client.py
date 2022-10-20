import threading
import os
import time
import sys
import random
import socket

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print("[C]: Client socket created")
    except socket.error as err:
        print('Client: socket open error: {} \n'.format(err))
        exit()

    port = (str(sys.argv[1]),int(sys.argv[2]))
    
    cs.connect(port) 
    
    input_file = open("PROJ2-HNS.txt", "r")
    queries = input_file.read().splitlines()
    input_file.close()
    file = open("RESOLVED.txt", "w+")
    
    for query in queries:
        print ("[C]: Sent: " + query)
        cs.send(query.encode('utf-8'))
        lsResponse = cs.recv(4096).decode("utf-8")
        print ("[C]: The received response is: "+ lsResponse + " IN")
        file.write(lsResponse + "\n")
        

    file.close()
    cs.close()
    exit()

if __name__ == "__main__":
    t1 = threading.Thread(name='client', target=client)
    t1.start()
    time.sleep(1)
    print("Client: done sending queries.")