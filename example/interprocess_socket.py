from socket import *
from select import *
import sys
from time import ctime
import threading



class Receiver(threading.Thread):
	def run(self):
		HOST = ''
		PORT = 11114
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
			message = clientSocket.recv(BUFSIZE).decode('utf-8')
			if (message == 'quit'):
				break
			elif (message != ''):
				print(message)

		clientSocket.close()  # 소켓 종료
		serverSocket.close()

		print('Receiver closed')
		

class Sender(threading.Thread):
	def run(self):
		#HOST = '211.202.32.174'
		HOST = '127.0.0.1'
		PORT = 11114
		BUFSIZE = 1024
		ADDR = (HOST, PORT)

		clientSocket = socket(AF_INET, SOCK_STREAM)  # 1 서버에 접속하기 위한 소켓을 생성한다.

		try:
			clientSocket.connect(ADDR)  # 2. 서버에 접속을 시도한다.
			print('connect is success')
			while(True):
				message = input("Message : ")
				clientSocket.send(message.encode('utf-8'))
				if (message == 'quit'):
					break
			print('Sender closed')
		except Exception as e:
			print('%s:%s' % ADDR)
			sys.exit()


if __name__ == "__main__":
	receiver = Receiver()
	sender = Sender()

	receiver.start()
	sender.start()

	receiver.join()
	sender.join()