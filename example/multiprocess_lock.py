from multiprocessing import Process, Lock


def f(lock, i):
	# lock이 unlock 상태가 될 때까지 block
	lock.acquire()

	# 처리 순번 출력
	print('{0}번째 프로세스 실행 중'.format(i))

	# lock 해제
	lock.release()


def main():
	# lock 객체
	lock = Lock()

	for i in range(3):
		p = Process(target=f, args=(lock, i))
		p.start()
	p.join()


if __name__ == "__main__":
	main()
