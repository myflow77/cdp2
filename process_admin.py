# -*- coding: utf-8 -*-


from socket import *
from select import *
import sys
from time import ctime
import threading
import time
from queue import Queue
import json
import os
import socketserver


Servers = []
queue = Queue()


# [START] 디바이스와 통신하고 하위 프로세스들을 관리하는 서버 클래스
class Manager():
	def __init__(self, name, port, queue):
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

		serverSocket.listen(100)  # 3.연결 수신 대기 상태

		clientSocket, addr_info = serverSocket.accept()  # 4.연결 수락

		print(self.NAME, 'accept')

		# 메시지를 디바이스로 보내주는 스레드 생성
		send = Send(clientSocket)
		send.daemon = True
		send.start()

		# 디바이스의 메세지 전송 처리함(반복)
		while(True):
			try:
				# 디바이스에서 메세지 수신
				print("Waiting message")
				json_str = clientSocket.recv(BUFSIZE).decode('utf-8')
				print('RECEIVE :', json_str)
				# 수신한 메세지를 파싱하여 결과 실행
				json_data = json.loads(json_str)
				message = json_data['message']
				if message == 'quit':
					print(self.NAME, "stopping")
					for i in range(len(Servers)):
						Servers[i].MESSAGE = message
					break
				elif message == 'list':
					self.get_filelist(json_data)
				elif message == 'delete':
					self.delete_file(json_data)
				elif message == 'play':
					self.play_music(json_data)
				elif message == 'upload':
					self.receive_file(json_data)
			except Exception as e:
				print(e)
				exit(0)

		# 스레드 종료
		print("Start to wait thread")
		send.alive = False
		send.join()
		print("End waiting thread")

		# 소켓 종료
		clientSocket.close()
		serverSocket.close()

		# 프로그램 종료
		#sys.exit(0)

		print(self.NAME, 'closed')
	
	def get_filelist(self, json_data):
		# 파일 리스트 획득
		current_dir = os.getcwd()
		sounds_list = os.listdir(current_dir + '/sounds')
		# 얻은 파일 리스트를 통해 json 데이터 생성
		files = []
		for i in range(len(sounds_list)):
			temp_dic = {'name' : sounds_list[i]}
			files.append(temp_dic)
		dic = {}
		dic['files'] = files
		json_str = json.dumps(dic)
		queue.put(json_str)
	

	def delete_file(self, json_data):
		# 파일 리스트 획득
		os.remove('sounds/' + json_data['filename'])
		print("Successfully remove", json_data['filename'])
		print(os.listdir(os.getcwd() + '/sounds'))


	def play_music(self, json_data):
		for i in range(len(Servers)):
			if Servers[i].NAME == 'sound':
				Servers[i].MESSAGE = json_data['filename']
		print("Successfully play music")

	def receive_file(self, json_data):
		filename = json_data['filename']
		filesize = json_data['size']
		BUFFERSIZE = 4096
		downloaded = BUFFERSIZE
		print("Start File Server")
		try:
			HOST = ''
			PORT = 10000
			s = socket()
			s.bind((HOST, PORT))
			f = open(filename, 'wb')
			s.listen(100)
			
			queue.put('ok')

			c, addr = s.accept()
			l = c.recv(BUFFERSIZE)
			
			count = 0

			while (l):
				if count == 100:
					processed = float(downloaded / filesize) * 100
					print("Process : {0:.2f}%".format(processed))
					count = 0
				f.write(l)
				l = c.recv(BUFFERSIZE)
				downloaded += BUFFERSIZE
				count += 1
			f.close()
			c.close()
		except Exception as e:
			print(e)
			print("OUT!!!!")

# [START] 큐에 쌓인 메시지를 디바이스로 전송해주는 클래스
class Send(threading.Thread):
	def __init__(self, clientSocket):
		threading.Thread.__init__(self)
		self.clientSocket = clientSocket

	def run(self):
		self.alive = True
		# 반복적으로 큐를 확인
		while(self.alive):
			if not queue.empty():
				# 큐에 쌓인 메세지를 회수
				temp = queue.get()
				temp += '\n'
				# 메세지를 디바이스로 전송
				if temp != '':
					self.clientSocket.send(temp.encode('utf-8'))
					print("SUCCESS :", temp)
			time.sleep(0.1)

	def stop(self):
		self.alive = False
		self.join()
# [END] 큐에 쌓인 메시지를 디바이스로 전송해주는 클래스


# [START] 하위 프로세스들과 통신하는 서버 클래스
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

		serverSocket.listen(100)  # 3.연결 수신 대기 상태

		clientSocket, addr_info = serverSocket.accept()  # 4.연결 수락

		print(self.NAME, 'accept')

		while(True):
			# message 확인
			if self.MESSAGE != '':
				message = self.MESSAGE
				self.MESSAGE = ''
				# 하위 프로세스에 메세지 전송
				clientSocket.send(message.encode('utf-8'))
				if (message == 'quit'):
					break

				# 결과 수신
				message = clientSocket.recv(BUFSIZE).decode('utf-8')
				if (message == 'quit'):
					break
				# 수신된 메세지를 출력
				elif (message != ''):
					print(message)
				'''
				# 수신된 메세지를 큐에 추가
				elif (message != ''):
					self.QUEUE.put(message)
				'''

		# 소켓 종료
		clientSocket.close()
		serverSocket.close()

		print(self.NAME, 'closed')
# [END] 하위 프로세스들과 통신하는 서버 클래스


# [START] main
if __name__ == "__main__":
	# face detection 프로세스와 통신하는 서버 클래스 생성
	face_detection = Receiver("face detection", 11111, queue)
	Servers.append(face_detection)
	face_detection.daemon = True
	face_detection.start()

	# notification 프로세스와 통신하는 서버 클래스 생성
	notification = Receiver("notification", 11112, queue)
	Servers.append(notification)
	notification.daemon = True
	notification.start()

	# sound 프로세스와 통신하는 서버 클래스 생성
	sound = Receiver("sound", 11113, queue)
	Servers.append(sound)
	sound.daemon = True
	sound.start()

	# 디바이스 통신 서버 생성
	manager = Manager("manager", 9999, Queue)
	manager.run()

	# join
	print("Start to join other process")
	face_detection.join()
	notification.join()
	sound.join()
# [END] main
