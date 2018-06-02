from multiprocessing import Process, Pipe
import os


def sender(conn):
	# 다른 자식 프로세스로 Hello World라는 메시지를 송신
	conn.send('Hello World')
	conn.close()


def receiver(conn):
	# 다른 자식 프로세스로부터 메시지를 수신하여 표시
	msg = conn.recv()
	print('메시지 수신: {0}'.format(msg))
	conn.close()


def main():
	# 메시지를 송수신하는 파이프 생성
	parent_conn, child_conn = Pipe()

	# 메시지 송신
	p = Process(target=sender, args=(child_conn,))
	p.start()

	# 메시지 수신
	p = Process(target=receiver, args=(parent_conn, ))
	p.start()

	p.join()


if __name__ == "__main__":
	main()
