import socket
import threading
import time

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Server(QThread):

	data_received = pyqtSignal(object)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def __init__(self, port):
		QThread.__init__(self)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('0.0.0.0', port))
		# server_thread = threading.Thread(target=self.run_server)
		# server_thread.daemon = True
		# server_thread.start()


	def run(self):
		self.sock.listen(1)
		print("Server running..")
		while True:
			connection, address = self.sock.accept()
			cThread = threading.Thread(target=self.connection_handler, args=(connection,address))
			cThread.daemon = True
			cThread.start()
			print(str(address[0]) + ":" + str(address[1]), " connected")


	def connection_handler(self, connection, address):
		while True:
			try:
				data = connection.recv(1024)
				connection.send(data)
				connection.close()
				self.data_received.emit(str(address[0]) + ":" + str(address[1]) + "->" + str(data, "utf-8"))

			except:
				pass
