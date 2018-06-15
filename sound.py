# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM
import sys
from threading import Thread
import time
from playsound import playsound

class PlaySound(Thread):
	def __init__(self, filename):
		Thread.__init__(self)
		self.daemon = True
		self.filename = filename

	def run(self):
		play_sound(self.filename)


def play_sound(filename):
	try:
		playsound(filename)
		print(filename, "played")
		return True
	except Exception as e:
		print(e)
		return False


if __name__ == "__main__":
	HOST = '127.0.0.1'
	PORT = 11113
	BUFSIZE = 1024
	ADDR = (HOST, PORT)

	# 서버에 접속하기 위한 소켓을 생성
	clientSocket = socket(AF_INET, SOCK_STREAM)
	# 서버에 접속을 시도한다.
	print('START : sound connecting')
	clientSocket.connect(ADDR)  
	print('START : sound connected!!!')
	while(True):
		try:
			# 서버에서 메세지를 수신
			message = clientSocket.recv(BUFSIZE).decode('utf-8')
			if (message == 'quit'):
				break
			elif (message != ''):
				message = play_sound(message)
				clientSocket.send(str(message).encode('utf-8'))
		except Exception as e:
			print(e)
			sys.exit()
	print('Sound closed')