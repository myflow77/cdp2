import json
import os

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