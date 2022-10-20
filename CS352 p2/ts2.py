
import threading
import os
import time
import json 
import sys
import socket as mysoc

def newSocket():
	try: 
		ret_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print ("[TS2]: Top-Level Server 2 socket created")
	except mysoc.error as err: 
		print ("[TS2]: Could not create socket \n Error: " + str(err))
	return ret_socket

def getDNS():
	file = open("PROJ2-DNSTS2.txt", "r")
	dns = {}
	for line in file:
		line = line.strip()
		word = line.split(' ')
		dns[word[0]] = line
	file.close()	
	
	return dns

def ts2():
	
	dns = getDNS()
	ts1Socket = newSocket()
	server_binding = ("", int(sys.argv[1]))
	ts1Socket.bind(server_binding)
	ts1Socket.listen(5)
	hsName = mysoc.gethostname()
	ipAddr = mysoc.gethostbyname(hsName)
	print("[TS2]: Running on Hostname, IP: ", hsName, ", ", ipAddr)
	clientSocket, addr = ts1Socket.accept()
	print("[TS2]: Got a connection request from: ", addr)

	while True:
		data = clientSocket.recv(4096).decode("utf-8").strip()
		print("[TS2]: Received Message: ", data)
		if not data: 
			break
		if data in dns:
			print("[TS2]: Data found in DNS")
			ret = dns.get(data)
			clientSocket.send(ret.encode("utf-8"))
	
	clientSocket.close()
	ts1Socket.close()
	exit()

ts2()