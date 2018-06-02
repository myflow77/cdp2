# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM
import sys
import threading
import time
from playsound import playsound


class Sender(threading.Thread):
	def run(self):
		#HOST = '211.202.32.174'
		HOST = '127.0.0.1'
		PORT = 11113
		BUFSIZE = 1024
		ADDR = (HOST, PORT)

		# 서버에 접속하기 위한 소켓을 생성
		clientSocket = socket(AF_INET, SOCK_STREAM)
		print('sound connecting')
		# 서버에 접속을 시도한다.
		clientSocket.connect(ADDR)  
		print('sound connected!!!')
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
		print('Sender closed')


def play_sound(filename):
	try:
		'''sound = pyglet.resource.media('resources/' + 'ChillingMusic.wav')
		sound.play()
		pyglet.app.run()'''
		playsound('resources/' + 'ChillingMusic.wav')
		print("Sound played!")
		return True
	except Exception as e:
		print(e)
		return False


if __name__ == "__main__":
	'''
	receiver = Receiver()
	receiver.start()
	receiver.join()
	'''

	sender = Sender()
	sender.start()
	sender.join()
