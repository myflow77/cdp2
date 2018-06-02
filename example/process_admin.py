# -*- coding: utf-8 -*-

# Socket
from socket import *
from select import *
import sys
from time import ctime
# Multiprocess
import threading


class Receiver(threading.Thread):
	def run(self):
		HOST = ''
		PORT = 11111 # 관리자 포트
		BUFSIZE = 1024
		ADDR = (HOST, PORT)

		serverSocket = socket(AF_INET, SOCK_STREAM)  # 1.소켓을 생성한다.

		serverSocket.bind(ADDR)  # 2.소켓 주소 정보 할당

		print('bind')

		serverSocket.listen(100)  # 3.연결 수신 대기 상태

		print('listen')

		clientSocket, addr_info = serverSocket.accept()  # 4.연결 수락

		print('accept')

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

		print('Receiver closed')


if __name__ == "__main__":
	receiver = Receiver()
	receiver.start()
	receiver.join()
