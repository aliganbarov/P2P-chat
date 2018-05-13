import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Server import Server

import socket


class Application(QWidget):


	def __init__(self, port):
		super().__init__()
		self.setWindowTitle("P2P Chat")
		self.show()
		self.init_gui()
		self.server = Server(int(port))
		self.server.data_received.connect(self.update_gui)
		self.server.start()

	def init_gui(self):
		self.layout = QVBoxLayout()
		self.layout.setSpacing(0)
		self.layout.setContentsMargins(0, 0, 0, 0)

		# Create Tab Bar
		self.tab_bar = QTabBar(movable=True, tabsClosable=True)
		self.tab_bar.tabCloseRequested.connect(self.CloseTab)
		self.tab_bar.tabBarClicked.connect(self.SwitchTab)

		self.tab_bar.setCurrentIndex(0)

		# Keep track of tabs
		self.tab_count = 0
		self.tabs = []
		self.tab_obj = []

		# New chat button
		self.newBtnWidget = QWidget()
		self.newBtnLayout = QHBoxLayout()
		self.addTabButton = QPushButton("New Chat")
		self.newBtnWidget.setLayout(self.newBtnLayout)
		self.newBtnLayout.addWidget(self.addTabButton)

		self.addTabButton.clicked.connect(self.AddTab)

		# set main view
		self.container = QWidget()
		self.container.layout = QStackedLayout()
		self.container.setLayout(self.container.layout)

		self.layout.addWidget(self.tab_bar)
		self.layout.addWidget(self.newBtnWidget)
		self.layout.addWidget(self.container)

		self.AddTab()

		self.setLayout(self.layout)



	def send_msg(self):
		tab_id = self.tab_bar.currentIndex()
		print(tab_id)
		
		tab = self.tab_obj[tab_id]

		address = tab.address.text()
		port = int(tab.port.text())
		print("Address: " + address)
		print("Port: " + str(port))
		msg = tab.message.toPlainText()
		tab.chat_screen.addWidget(QLabel("Me->" + msg))
		tab.message.setPlainText("")

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.connect((address, port))
		sock.send(bytes(msg, 'utf-8'))


		# while True:
		# 	ack = sock.recv(1024)
		# 	if not ack:
		# 		break 
			# self.chat_v_layout.addWidget(QLabel(str(ack, "utf-8")))


	def update_gui(self, data):
		print("Updating gui with " + data)
		self.chat_v_layout.addWidget(QLabel(data))


	def CloseTab(self, i):
		self.tab_bar.removeTab(i)


	def AddTab(self):
		i = self.tab_count

		self.tabs.append(QWidget())
		self.tabs[i].layout = QVBoxLayout()
		self.tabs[i].setObjectName("tab" + str(i))

		# Open webview
		self.tabs[i].content = self.CreateTabContent()

		# Add webview to tabs layout
		self.tabs[i].layout.addWidget(self.tabs[i].content)

		# Set top level tab from [] to layout
		self.tabs[i].setLayout(self.tabs[i].layout)

		# Add tab to top level stackedwidget
		self.container.layout.addWidget(self.tabs[i])
		self.container.layout.setCurrentWidget(self.tabs[i])

		# Set the tab at top of screen
		self.tab_bar.addTab("New Tab")
		self.tab_bar.setTabData(i, "tab" + str(i))
		self.tab_bar.setCurrentIndex(i)

		self.tab_obj.append(Tab(i, self.address_line, 
			self.port_line, self.message_line, 
			self.chat_v_layout))

		self.tab_count += 1


	def SwitchTab(self, i):
		tab_data = self.tab_bar.tabData(i)
		tab_content = self.findChild(QWidget, tab_data)
		self.container.layout.setCurrentWidget(tab_content)


	def CreateTabContent(self):
		# Create Widget
		self.tab_content = QWidget()
		self.tab_content.layout = QGridLayout()
		self.tab_content.setLayout(self.tab_content.layout)

		# Create chat history area
		self.chat_v_layout = QGridLayout()
		self.chat_v_layout.setRowStretch(50, 50)
		chat_box = QGroupBox("Chat Area")
		chat_box.setLayout(self.chat_v_layout)
		msg_scroll = QScrollArea()
		msg_scroll.setWidget(chat_box)
		msg_scroll.setWidgetResizable(True)
		msg_scroll.setFixedHeight(400)
		
		# Create address, port, message inputs
		address_label = QLabel("Enter Address: ")
		port_label = QLabel("Enter port: ")
		message_label = QLabel("Enter message: ")
		self.address_line = QLineEdit()
		self.port_line = QLineEdit()
		self.message_line = QPlainTextEdit()

		# Create Send button
		self.button = QPushButton("Send")
		self.button.clicked.connect(self.send_msg)

		# Populate Widget
		row = 0

		self.tab_content.layout.addWidget(address_label, row, 0, 1, 1)
		self.tab_content.layout.addWidget(self.address_line, row, 1, 1, 2)
		row += 1
		
		self.tab_content.layout.addWidget(port_label, row, 0, 1, 1)
		self.tab_content.layout.addWidget(self.port_line, row, 1, 1, 2)
		row += 1

		self.tab_content.layout.addWidget(msg_scroll, row, 0, 1, 3)
		row += 1

		self.tab_content.layout.addWidget(message_label, row, 0, 1, 1)
		self.tab_content.layout.addWidget(self.message_line, row, 1, 1, 2)
		row += 1

		self.tab_content.layout.addWidget(self.button, row, 0, 1, 3)

		return self.tab_content


class Tab:
	def __init__(self, id, address, port, message, chat_screen):
		self.id = id
		self.address = address
		self.port = port
		self.message = message
		self.chat_screen = chat_screen





if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = Application(sys.argv[1])
	window.setGeometry(1500, 1000, 300, 300)
	sys.exit(app.exec_())

