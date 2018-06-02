# -*- coding: utf-8 -*-

from firebase import firebase
from pyfcm import FCMNotification

# get raspberry serial number


def getserial():
    serial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                serial = line[10:26]
        f.close()
    except:
        serial = "ERROR000000000"
    return serial


myserial = getserial()
print(myserial)
# database
firebase = firebase.FirebaseApplication(
    "https://smart-baby-monitor-250da.firebaseio.com/", None)
#result = firebase.get('/sensor', None)

# notification
push_service = FCMNotification(
    api_key="AAAAr8ctsds:APA91bG2kqd_FDzreWEBRsSt1WPLSpqI7KvqRWUoit6Q8N9Y0qfXKr2nz--soqGuHcdCQgWE6lmksO0ph7XpKlzifSQb5RWHV23hU0Q5bkgqgNRCGfQ4DUy_um8UJU2VUS7fNxC0ofwk")

target_users = firebase.get("/users", None)
listToken = []
for k, v in target_users.items():
    if v["raspberry"] == myserial:
        listToken.append(v["token"])

message_title = "Smart Baby Monitor"
message_body = "아기가 위험해요!"
data_message = {"message_body": "Problem"}
# single notification
#registration_id="e7lDol3OjI8:APA91bGKt8JeC58vL1S8KBVXh7fRhXlYZi3xtOR0sX1wflqp2UV3qWSaVApTNjl9LJEIF3Dmqul5Bb06ByQPlDikVlFM_KpAcgJOB75w2LzFyhdNW-NHQmIT_-L20hwqhZNCrlXBBv6b"
#result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, data_message=data_message)
# multiple notification
registration_ids = listToken
result = push_service.notify_multiple_devices(
    registration_ids=registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)

print(result)
