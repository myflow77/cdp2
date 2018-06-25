# -*- coding: utf-8 -*-

import json
import os
from firebase import firebase
import socket

json_str = '{"files":[{"name":"filename1"},{"name":"filename2"},{"name":"filename3"}]}'
json_data = json.loads(json_str)

print(json_data['files'][0])

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

print(json_str)
print("\n\n#######################################################################")
print("#######################################################################")
print("#######################################################################\n\n")

#
# FIREBASE
#

fb = firebase.FirebaseApplication("https://smart-baby-monitor-250da.firebaseio.com/", None)

'''
# get의 두번째 arg에 None을 넣으면 테이블 전체를 받는다
try:
	result = fb.get('/users', None)
	print(result)
except Exception as e:
	print(e)
'''
'''
# get의 두번째 arg는 첫번째 arg 테이블에 있는 데이터의 id를 의미한다.
try:
	result = fb.get('/users', '1')
	print(result)
except Exception as e:
	print(e)
'''
'''
# 이렇게 검색할 수 있다는데...
try:
	result = fb.get('/users', None, {'print' : 'pretty'}, {'email': 'saykjh94@naver.com', 'raspberry': '000000009712121e', 'token': 'fnQBILcNX-k:APA91bFquRzansHyrYKfv3YPtGZDi1gp00zIxsaTeCI8EWA5QEluIlD0KzjTi0FZNlzOiNchZhBstKDXGzGhzj3q93vxBDrCsfLZ86bLUo0nxmgfwgwokMWNuPwuEbF0SsGb_YdzDajt'})
	print(result)
except Exception as e:
	print(e)
'''
'''
# put, post ==> 자원의 전체를 교체
try:
	result = fb.put('/users', {'id' : {'email' : 'teakan7179@gmail.com', 'raspberry' : '??', 'token' : '??', 'etc' : '??'}})
	print(result)
	result = fb.get('/users', None)
	print(result)
except Exception as e:
	print(e)
'''

'''
# patch ==> 자원의 일부를 교체
try:
	result = fb.patch('/users', {'id' : {'email' : 'teakan7179@gmail.com', 'raspberry' : '??', 'token' : '??', 'etc' : '??'}})
	print(result)
	result = fb.get('/users', None)
	print(result)
except Exception as e:
	print(e)
'''

'''
# delete
try:
	fb.delete('/users', 'email')
	result = fb.get('/users', None)
	print(result)
except Exception as e:
	print(e)
'''

def print_firebase():
	fb_dic = fb.get('/users', None)
	fb_list = fb_dic.items()
	for item in fb_list:
		#print(item)
		print("\nID : {0}".format(item[0])) # 각 row의 [0]은 key를 의미
		print("CONTENT : {0}\n".format(item[1])) # 각 row의 [1]은 value dic을 의미

'''
# 업데이트를 시도해보자
try:
	result = fb.patch('/users', {'ir' : {'raspberry' : '12345'}})
	print(result)
	print_firebase()
except Exception as e:
	print(e)
'''
'''
# 시리얼 번호로 나를 찾고 정보를 수정해보자
target_users = fb.get("/users", None)
listToken = []
for key, value in target_users.items():
	#if value["raspberry"] == '000000009712121e':
	#	listToken.append(v["token"])
	if key == 'id':
		#target_users[key] = {'email' : 'gildong1234@gmail.com', 'raspberry' : '987654321', 'token' : 'aaa000bbb111ccc222'}
		target_users[key]['token'] = 'ddd333eee444fff555'
		result = fb.patch('/users', {key : target_users[key]})
		print(result)
print_firebase()
'''
#211.202.32.174
def get_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('gmail.com', 80))
	r = s.getsockname()[0]
	s.close()
	return r
my_addr = get_address()
print(my_addr)