import socket
import threading


class Client:
	def __init__(self, address, port, msg):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.connect((address, port))

		iThread = threading.Thread(target=self.sendMsg, args=(sock, msg,))
		iThread.daemon = True
		iThread.start()

		while True:
			data = sock.recv(1024)
			if not data:
				break 
			print(str(data, 'utf-8'))


	def sendMsg(self, sock, msg):
		print("sending message")
		sock.send(bytes(msg, 'utf-8'))


