# -*- coding: utf-8 -*-

# Socket
from socket import *
from select import *
import sys
from time import ctime
# Multiprocess
import threading
from multiprocessing import Process, Queue

class Receiver():
	def __init__(self, name, port, queue):
		self.NAME = name
		self.PORT = port
		self.QUEUE = queue

	def run(self):
		HOST = ''
		PORT = self.PORT  # 관리자 포트
		BUFSIZE = 1024
		ADDR = (HOST, PORT)

		serverSocket = socket(AF_INET, SOCK_STREAM)  # 1.소켓을 생성한다.

		serverSocket.bind(ADDR)  # 2.소켓 주소 정보 할당

		print(self.NAME, 'bind')

		serverSocket.listen(100)  # 3.연결 수신 대기 상태

		print(self.NAME, 'listen')

		clientSocket, addr_info = serverSocket.accept()  # 4.연결 수락

		print(self.NAME, 'accept')

		while(True):
			message = input("Message : ")
			clientSocket.send(message.encode('utf-8'))
			if (message == 'quit'):
				break

			message = clientSocket.recv(BUFSIZE).decode('utf-8')
			if (message == 'quit'):
				break
			elif (message != ''):
				print(message)

		# 소켓 종료
		clientSocket.close()
		serverSocket.close()

		print(self.NAME, ' closed')


def face_detection(queue):
	Receiver("Face Detection", 11111, queue)

def notification(queue):
	Receiver("Notification", 11112, queue)

def sound(queue):
	Receiver("Sound", 11113, queue)


if __name__ == "__main__":
	#queues = {}
	#queues['face_detection'] = Queue
	#queues['notification'] = Queue
	#queues['sound'] = Queue

	queues = []
	queues[0] = Queue
	queues[1] = Queue
	queues[2] = Queue
	
	p = []
	p[0] = Process(target=face_detection, args=(queues[0]))
	p[0].start()
	p[1] = Process(target=face_detection, args=(queues[1]))
	p[1].start()
	p[2] = Process(target=face_detection, args=(queues[2]))
	p[2].start()

'''
Queue
	target : 큐의 데이터가 전달되어야 할 타겟
	message : 전달될 메세지
'''
