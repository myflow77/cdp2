import array
import numpy as np
import pyaudio
import wave
from Python_Extension import *
from socket import *
from select import *
import time

# [START] main
if __name__ == "__main__":
	HOST = '127.0.0.1'
	PORT = 11113
	BUFSIZE = 1024
	ADDR = (HOST, PORT)

	# 서버에 접속하기 위한 소켓을 생성
	clientSocket = socket(AF_INET, SOCK_STREAM)
	# 서버에 접속을 시도
	print('START : face detection connectiong')
	clientSocket.connect(ADDR)
	print('SUCCESS : face detection connected')
	# hyperparameter
	rate = 16000
	record_seconds = 1.024
	chunk = 1024

	NN = Neural_Networks("model.txt")
	SP = Speech_Processing()
	SP.Load_Parameter("param.txt")
	# Loop
	while(True):
		# 주기적으로 아기의 소리를 검사하여 결과를 admin으로 보냄
		try:
			buffer = []
			frame = []

			audio = pyaudio.PyAudio()
			stream = audio.open(format=pyaudio.paInt16,
								channels=1,
								rate=rate,
								input_device_index=2,
								frames_per_buffer=chunk,
								input=True)

			for i in range(0, int(rate / chunk * record_seconds)):
				data = stream.read(chunk)
				buffer.append(data)

				if i == 0:
					frame = np.fromstring(data, dtype=np.int16)
				else:
					frame = np.append(frame, np.fromstring(data, dtype=np.int16))

			stream.stop_stream()
			stream.close()
			audio.terminate()

			frame = np.array(frame / 32768, dtype=np.float32)
			MFCC = SP.Calculate_MFCC(frame, frame.shape[0], 400, 160, 13, 26, rate)

			output = np.zeros(100, dtype=np.float32)
			NN.Test(MFCC, output, int(MFCC.shape[0] / (3 * 13)))

			result = True if output[0] + output[output.shape[0] - 1] > 1 else False
			print(result, 0.5 * (output[0] + output[output.shape[0] - 1]))
			# 아이가 울면 알림 전송
			if result == True:
				clientSocket.send('notify_crying'.encode('utf-8'))
				time.sleep(60)
		except Exception as e:
			print("VOICE ERROR :", e)

	print('END : Voice closed')
# [END] main


'''
wav = wave.open("file.wav", 'wb')
wav.setnchannels(1)
wav.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
wav.setframerate(rate)
wav.writeframes(b''.join(buffer))
wav.close()
'''
