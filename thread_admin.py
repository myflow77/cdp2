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

Servers = []
queue = Queue()

class Manager(threading.Thread):
	def __init__(self, name, port, queue):
		threading.Thread.__init__(self)
		self.NAME = name
		self.PORT = port
		self.QUEUE = queue
		self.MESSAGE = ''

	def run(self):
		HOST = ''
		PORT = self.PORT  # 관리자 포트
		BUFSIZE = 1024
		ADDR = (HOST, PORT)

		serverSocket = socket(AF_INET, SOCK_STREAM)  # 1.소켓을 생성한다.

		serverSocket.bind(ADDR)  # 2.소켓 주소 정보 할당

		#print(self.NAME, 'bind')

		serverSocket.listen(100)  # 3.연결 수신 대기 상태

		#print(self.NAME, 'listen')

		clientSocket, addr_info = serverSocket.accept()  # 4.연결 수락

		print(self.NAME, 'accept')
		
		'''
		class Send(threading.Thread):
			def __init__(self, queue):
				threading.Thread.__init__(self)
				self.QUEUE = queue

			def run(self):
				# 하위 프로세스(기능)에서 수신된 메세지를 디바이스에 전달
				while(True):
					if not self.QUEUE.empty():
						# 메세지 전송
						temp = queue.get()
						if temp != '':
							clientSocket.send(temp.encode('utf-8'))
							print(temp)
					time.sleep(0.1)
		'''
		class Send(threading.Thread):
			def run(self):
				self.alive = True
				# 하위 프로세스(기능)에서 수신된 메세지를 디바이스에 전달
				while(self.alive):
					if not queue.empty():
						# 메세지 전송
						temp = queue.get()
						if temp != '':
							clientSocket.send(temp.encode('utf-8'))
							print(temp)
					time.sleep(0.1)
			def stop(self):
				self.alive = False
				self.join()

		send = Send()
		send.daemon = True
		send.start()

		while(True):
			time.sleep(1)
			while(True):
				# 디바이스에서 메세지 수신
				json_str = clientSocket.recv(BUFSIZE).decode('utf-8')
				# 수신한 메세지를 파싱
				json_data = json.loads(json_str)
				target = json_data['target']
				message = json_data['message']
				# 목표 프로세스에 메세지 전달
				for i in range(len(Servers)):
					if target == 'all' or target == Servers[i].NAME:
						Servers[i].MESSAGE = message
				if message == 'quit':
					print(self.NAME, "stopping")
					#send.stop()
					sys.exit(0)
					print(self.NAME, 'closed')
					break

		# 소켓 종료
		clientSocket.close()
		serverSocket.close()

		print(self.NAME, 'closed')

class Receiver(threading.Thread):
	def __init__(self, name, port, queue):
		threading.Thread.__init__(self)
		self.NAME = name
		self.PORT = port
		self.QUEUE = queue
		self.MESSAGE = ''

	def run(self):
		HOST = ''
		PORT = self.PORT  # 관리자 포트
		BUFSIZE = 1024
		ADDR = (HOST, PORT)

		serverSocket = socket(AF_INET, SOCK_STREAM)  # 1.소켓을 생성한다.

		serverSocket.bind(ADDR)  # 2.소켓 주소 정보 할당

		#print(self.NAME, 'bind')

		serverSocket.listen(100)  # 3.연결 수신 대기 상태

		#print(self.NAME, 'listen')

		clientSocket, addr_info = serverSocket.accept()  # 4.연결 수락

		print(self.NAME, 'accept')

		while(True):
			# message 확인
			if self.MESSAGE != '':
				message = self.MESSAGE
				self.MESSAGE = ''
				# 메세지 전송
				clientSocket.send(message.encode('utf-8'))
				if (message == 'quit'):
					break

				# 결과 수신
				message = clientSocket.recv(BUFSIZE).decode('utf-8')
				if (message == 'quit'):
					break
				elif (message != ''):
					self.QUEUE.put(message)

		# 소켓 종료
		clientSocket.close()
		serverSocket.close()

		print(self.NAME, 'closed')

# [START] main
if __name__ == "__main__":
	manager = Manager("manager", 11110, Queue)
	manager.start()

	#Servers = []
	#queue = Queue()
	
	face_detection = Receiver("face detection", 11111, queue)
	#Servers[0] = face_detection
	Servers.append(face_detection)
	face_detection.start()

	notification = Receiver("notification", 11112, queue)
	#Servers[1] = notification
	Servers.append(notification)
	notification.start()

	sound = Receiver("sound", 11113, queue)
	#Servers[2] = sound
	Servers.append(sound)
	sound.start()

	# join
	manager.join()
	face_detection.join()
	notification.join()
	sound.join()
# [END] main
