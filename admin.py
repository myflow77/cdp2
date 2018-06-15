# -*- coding: utf-8 -*-


from socket import *
from select import *
import sys
from time import ctime
from threading import Thread
import time
from queue import Queue
import json
import os
import socketserver
import notification
import sound
from notification import SendNotification
from sound import PlaySound


Servers = []
message_queue = Queue()


# [START] 하위 프로세스들과 통신하는 서버 클래스
class Receiver(Thread):
	def __init__(self, name, port):
		Thread.__init__(self)
		self.daemon = True
		self.NAME = name
		self.PORT = port
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
			'''
			# message 확인
			message = self.MESSAGE
			self.MESSAGE = ''
			
			# 하위 프로세스에 메세지 전송
			clientSocket.send(message.encode('utf-8'))
			if (message == 'quit'):
				break
			'''

			# 결과 수신
			message = clientSocket.recv(BUFSIZE).decode('utf-8')
			if (message == 'quit'):
				break
			# 수신된 메세지를 출력
			elif (message != ''):
				print("RECV FROM PROCESS :", message)
				if message == 'notify_emotion':
					thread_notify = SendNotification("아이를 확인해주세요!")
					thread_notify.start()
				elif message == 'notify_crying':
					thread_notify = SendNotification("아이를 확인해주세요!")
					thread_notify.start()
				elif message == 'notify_moving':
					thread_notify = SendNotification("아이를 확인해주세요!")
					thread_notify.start()
				else:
					message_queue.put(message)

		# 소켓 종료
		clientSocket.close()
		serverSocket.close()

		print(self.NAME, 'closed')
# [END] 하위 프로세스들과 통신하는 서버 클래스


# [START] 큐에 쌓인 메시지를 디바이스로 전송해주는 클래스(스레드)
class Sender(Thread):
	def __init__(self, clientSocket):
		Thread.__init__(self)
		self.daemon = True
		self.clientSocket = clientSocket

	def run(self):
		self.alive = True
		# 반복적으로 큐를 확인
		while(self.alive):
			if not message_queue.empty():
				# 큐에 쌓인 메세지를 회수
				temp = message_queue.get()
				temp += '\n'
				# 메세지를 디바이스로 전송
				if temp != '':
					print("QUEUE TO DEVICE : {0}".format(temp))
					self.clientSocket.send(temp.encode('utf-8'))
			time.sleep(0.1)

	def stop(self):
		self.alive = False
		self.join()
# [END] 큐에 쌓인 메시지를 디바이스로 전송해주는 클래스


# 파일 리스트 획득 및 디바이스로 전송
def get_filelist(json_data):
	current_dir = os.getcwd()
	sounds_list = os.listdir(current_dir + '/sounds')
	# 얻은 파일 리스트를 통해 json 데이터 생성
	files = []
	for i in range(len(sounds_list)):
		temp_dic = {'name': sounds_list[i]}
		files.append(temp_dic)
	dic = {}
	dic['files'] = files
	print("FILE LIST : ", files)
	json_str = json.dumps(dic)
	message_queue.put(json_str)


# 디렉토리의 파일을 삭제
def delete_file(json_data):
	try:
		os.remove('sounds/' + json_data['filename'])
		print("REMOVE SUCCESSFULLY : ", json_data['filename'])
	except Exception as e:
		print(e)


# 디렉토리의 음악을 재생
def play_music(json_data):
	'''
	for i in range(len(Servers)):
		if Servers[i].NAME == 'sound':
			Servers[i].MESSAGE = json_data['filename']
	print("Successfully play music")
	'''
	try:
		thread_sound = sound.PlaySound(json_data['filename'])
		thread_sound.start()
		print("PLAY SOUND SUCCESSFULLY : ", json_data['filename'])
	except Exception as e:
		print(e)


# 디바이스로부터 파일을 전송받음
def receive_file(json_data):
	filename = json_data['filename']
	filesize = json_data['size']
	BUFFERSIZE = 4096
	downloaded = 0
	print("Start File Server")
	print("File Size :", filesize)
	try:
		HOST = ''
		PORT = 10000
		s = socket()
		s.bind((HOST, PORT))
		s.listen(100)
		# ok 전송
		message_queue.put('ok')
		# 디바이스 파일 전송 소켓 연결
		c, addr = s.accept()
		print("File socket accepted")
		# 파일 생성
		f = open('sounds/' + filename, 'wb')
		l = c.recv(BUFFERSIZE)
		downloaded += len(l)

		count = 0

		while (l):
			if count == 100:
				float(filesize)
				processed = downloaded / filesize * 100
				print("Process : {0:.2f}% <== {1}".format(processed, len(l)))
				count = 0
			f.write(l)
			l = c.recv(BUFFERSIZE)
			downloaded += len(l)
			count += 1
		f.close()
		c.close()
	except Exception as e:
		print("FAIL TO RECEIVE FILE")
		print(e)

# [START] main
if __name__ == "__main__":
	# emotion 프로세스와 통신하는 서버 스레드 생성
	emotion = Receiver("emotion", 11111)
	Servers.append(emotion)
	emotion.start()

	'''
	# notification 프로세스와 통신하는 서버 스레드 생성
	notification = Receiver("notification", 11112)
	Servers.append(notification)
	notification.start()
	'''

	'''
	# sound 프로세스와 통신하는 서버 스레드 생성
	sound = Receiver("sound", 11113)
	Servers.append(sound)
	sound.start()
	'''

	# 디바이스 통신 서버 생성
	NAME = "manager"
	PORT = 9999
	MESSAGE = ''
	HOST = ''

	BUFSIZE = 1024
	ADDR = (HOST, PORT)

	serverSocket = socket(AF_INET, SOCK_STREAM)  # 1.소켓을 생성한다.

	serverSocket.bind(ADDR)  # 2.소켓 주소 정보 할당

	while(True):
		print("\n[ Server start to listen ]\n")
		serverSocket.listen(100)  # 3.연결 수신 대기 상태

		clientSocket, addr_info = serverSocket.accept()  # 4.연결 수락

		print(NAME, 'accept')

		# 메시지를 디바이스로 보내주는 스레드 생성
		send = Sender(clientSocket)
		send.start()

		# 디바이스의 메세지 전송 처리함(반복)
		while(True):
			try:
				# 디바이스에서 메세지 수신
				print("\n[ Waiting message ]\n")
				json_str = clientSocket.recv(BUFSIZE).decode('utf-8')
				# 소켓이 종료되면 다시 Listen 상태로 들어감
				if json_str == '':
					break
				print('RECEIVE FROM DEVICE :', json_str)
				# 수신한 메세지를 파싱하여 결과 실행
				json_data = json.loads(json_str)
				message = json_data['message']
			except Exception as e:
				print("Error on parsing json string")
				print(e)
				exit(0)
			try:
				if message == 'quit':
					print(NAME, "stopping")
					for i in range(len(Servers)):
						Servers[i].MESSAGE = message
					break
				elif message == 'list':
					get_filelist(json_data)
				elif message == 'delete':
					delete_file(json_data)
				elif message == 'play':
					play_music(json_data)
				elif message == 'upload':
					receive_file(json_data)
			except Exception as e:
				print("Error on after process")
				print(e)

		# 디바이스 전송 스레드 종료
		print("Start to wait thread")
		send.alive = False
		send.join()
		print("End to wait thread")

		# 클라이언트 소켓 종료
		clientSocket.close()
	
	# 서버 소켓 종료
	serverSocket.close()

	# 하위 프로세스 통신 스레드 join
	print("Wait to join other process")
	emotion.join()
	#notification.join()
	#sound.join()