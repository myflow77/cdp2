from threading import Thread
from socket import gethostbyname, gethostname

class RegisterInfo(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.daemon = True

	def run(self):
        my_ip = 
        
        stream_addr = my_ip + ':15000/?action=stream/frame.mjpg'