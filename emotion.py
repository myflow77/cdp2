# -*- coding: utf-8 -*-

#!/usr/bin/env python

# Copyright 2015 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
from socket import *
from select import *
import sys
from time import ctime
import threading
import json
import time
import notification


# [START def_detect_face]
def detect_face(face_file, max_results=4):
	"""Uses the Vision API to detect faces in the given file.

	Args:
		face_file: A file-like object containing an image with faces.

	Returns:
		An array of Face objects with information about the picture.
	"""
	# [START get_vision_service]
	client = vision.ImageAnnotatorClient()
	# [END get_vision_service]

	content = face_file.read()
	image = types.Image(content=content)

	response = client.face_detection(image=image)

	faces = response.face_annotations

	return faces
# [END def_detect_face]

# [START def_highlight_faces]
def highlight_faces(image, faces, output_filename):
	"""Draws a polygon around the faces, then saves to output_filename.

	Args:
	image: a file containing the image with the faces.
	faces: a list of faces found in the file. This should be in the format
		returned by the Vision API.
	output_filename: the name of the image file to be created, where the
		faces have polygons drawn around them.
	"""
	im = Image.open(image)
	draw = ImageDraw.Draw(im)

	count = 1
	result = {}

	for face in faces:
		box = [(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices]
		draw.line(box + [box[0]], width=5, fill='#00ff00')

		result['number'] = count
		result['joy'] = face.joy_likelihood
		result['sorrow'] = face.sorrow_likelihood
		result['anger'] = face.anger_likelihood
		result['surprise'] = face.surprise_likelihood
		count += 1
		break

	print(result)

	im.save(output_filename)

	return result
# [END def_highlight_faces]

# [START] emotion_recognition
def emotion_recognition(input_filename, output_filename, max_results):
	with open(input_filename, 'rb') as image:
		faces = detect_face(image, max_results)
		#print('Found {} face{}'.format(len(faces), '' if len(faces) == 1 else 's'))

		#print('Writing to file {}'.format(output_filename))
		# Reset the file pointer, so we can read the file again
		image.seek(0)
		result_string = highlight_faces(image, faces, output_filename)

		return result_string
# [END] emotion_recognition

# [START] main
if __name__ == "__main__":
	HOST = '127.0.0.1'
	PORT = 11111
	BUFSIZE = 1024
	ADDR = (HOST, PORT)

	# 서버에 접속하기 위한 소켓을 생성
	clientSocket = socket(AF_INET, SOCK_STREAM)
	# 서버에 접속을 시도
	print('START : face detection connectiong')
	clientSocket.connect(ADDR)
	print('SUCCESS : face detection connected')
	while(True):
		'''
		try:
			message = clientSocket.recv(BUFSIZE).decode('utf-8')

			if (message == 'quit'):
				break
			elif (message != ''):
				message = emotion_recognition(message, 'out.jpg', 4)
				clientSocket.send(message.encode('utf-8'))
		except Exception as e:
			print(e)
		'''
		# 주기적으로 아기의 표정을 검사하여 결과를 admin으로 보냄
		try:
			result = emotion_recognition('pictures/in.jpg', 'pictures/out.jpg', 4)

			if result['sorrow'] > 2 or result['anger'] > 2 or result['surprise'] > 2:
				clientSocket.send('notify_emotion'.encode('utf-8'))
		except Exception as e:
			print("EMOTION ERROR :", e)
		# 일정 시간 휴식
		time.sleep(30)

	print('END : Face_Detection closed')
# [END] main
