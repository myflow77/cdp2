from socket import *
from select import *
import numpy as np
import cv2
import time
from notification import SendNotification
import os

if __name__ == "__main__":
	cap = cv2.VideoCapture("http://127.0.0.1:8080/?action=stream/frame.mjpg")
	count = 1
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
	fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
	check_time = time.process_time()
	check_time_flag=time.process_time()
	check_flag = True

	HOST = '127.0.0.1'
	PORT = 11112
	BUFSIZE = 1024
	ADDR = (HOST, PORT)

	# 서버에 접속하기 위한 소켓을 생성
	clientSocket = socket(AF_INET, SOCK_STREAM)
	# 서버에 접속을 시도
	print('START : motion connectiong')
	clientSocket.connect(ADDR)
	print('SUCCESS : motion connected')

	# Loop
	while(True):
		# 주기적으로 아기의 표정을 검사하여 결과를 admin으로 보냄
		try:
			ret, frame = cap.read()

			fgmask = fgbg.apply(frame)
			fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

			n_white_pix = np.sum(fgmask == 255)

			if(n_white_pix > 10000 and check_flag):
				clientSocket.send('notify_motion'.encode('utf-8'))
				check_flag=False
				check_time_flag=time.process_time()
				print(n_white_pix)

			coltime = time.process_time() - check_time
			check_coltime= time.process_time() - check_time_flag

			if(check_coltime > 30 and not(check_flag)):
				check_time_flag = time.process_time()
				check_flag=True

			if(coltime > 60):
				check_time = time.process_time()
				str_name = "./pictures/in.jpg"
				print("Image file is saved")
				cv2.imwrite(str_name, frame)
				count += 1

			#cv2.imshow('frame', frame)

			k = cv2.waitKey(30) & 0xff
			if k == 27:
				break
		except Exception as e:
			print("MOTION ERROR :", e)
		# 일정 시간 휴식

	print('END : motion closed')

	cap.release()

	cv2.destroyAllWindows()
