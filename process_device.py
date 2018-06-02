# -*- coding: utf-8 -*-

# Socket
from socket import *
from select import *
import sys
from time import ctime
# Multiprocess
import threading
import time
from queue import Queue
# Json
import json

class Sender(threading.Thread):
	def run(self):
		#HOST = '211.202.32.174'
		HOST = '127.0.0.1'
		PORT = 11110
		BUFSIZE = 1024
		ADDR = (HOST, PORT)

		clientSocket = socket(AF_INET, SOCK_STREAM)  # 1 서버에 접속하기 위한 소켓을 생성한다.

		clientSocket.connect(ADDR)  # 2. 서버에 접속을 시도한다.
		print('connect is success')

		class Receive(threading.Thread):
			def run(self):
				self.alive = True
				# 하위 프로세스(기능)에서 수신된 메세지를 디바이스에 전달
				while(self.alive):
					message = clientSocket.recv(BUFSIZE).decode('utf-8')
					if (message == 'quit'):
						break
					elif (message != ''):
						print(message)

			def stop(self):
				self.alive = False
				self.join()

		receive = Receive()
		receive.daemon = True
		receive.start()

		while(True):
			target = input("Target : ")
			message = input("Message : ")

			dic = {}
			dic['target'] = target
			dic['message'] = message

			json_str = json.dumps(dic)

			clientSocket.send(json_str.encode('utf-8'))
			if (target == 'all' and message == 'quit'):
				print("Manager stopping")
				#receive.stop()
				sys.exit(0)
				print('Device closed')
				break

			'''
			message = clientSocket.recv(BUFSIZE).decode('utf-8')
			if (message == 'quit'):
				break
			elif (message != ''):
				print(message)
			'''
		print('Device closed')


# [START] main
if __name__ == "__main__":
	sender = Sender()
	sender.start()
	sender.join()
# [END] main
