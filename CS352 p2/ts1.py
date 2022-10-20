
import threading
import os
import time
import json 
import sys

import socket as mysoc

def newSocket():
	try: 
		ret_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
		print ("[TS1]: Top-Level Server 1 socket created")
	except mysoc.error as err: 
		print ("[TS1]: Could not create socket \n Error: " + str(err))
	return ret_socket

def argCheck(size, expected):
	if size is not expected:
		raise TypeError("Expected %d arguments, got %d" % (expected, size))
		exit()

def getDNS():
	file = open("PROJ2-DNSTS1.txt", "r")
	dns = {}
	for line in file:
		line = line.strip()
		word = line.split(' ')
		dns[word[0]] = line
	file.close()	
	
	return dns

def ts():
	argCheck(len(sys.argv), 2)
	dns = getDNS()
	ts1Socket = newSocket()
	server_binding = ("", int(sys.argv[1]))
	ts1Socket.bind(server_binding)
	ts1Socket.listen(5)
	hsName = mysoc.gethostname()
	ipAddr = mysoc.gethostbyname(hsName)
	print("[TS1]: Running on Hostname, IP: ", hsName, ", ", ipAddr)
	clientSocket, addr = ts1Socket.accept()
	print("[TS1]: Got a connection request from: ", addr)
	
	while True:
		data = clientSocket.recv(4096).decode("utf-8").strip()
		print("[TS1]: Received Message: ", data)
		if not data:
			break
		if data in dns:
			print("[TS1]: Data found in DNS")
			ret = dns.get(data)
			clientSocket.send(ret.encode("utf-8"))
	
	clientSocket.close()
	ts1Socket.close()
	exit()

ts()