import threading
import sys
import random
import time

free_row = 0

def randomMatrix(size):
	matrix = [[random.randint(0, 1) for x in range(size)] for y in range(size)]
	return matrix

def multiplyThreaded(first, second, size, numOfThreads):
	lock = threading.Lock()
	result = [[0 for x in range(size)] for y in range(size)]
	threads = []
	def processRow(r, size):
		for column in range(size):
			sum = 0
			for num in range(size):
				sum = sum or (first[r][num] and second[num][column])
				if sum == 1:
					break
			result[r][column] = sum
			
	def threadTarget():
		global free_row
		while free_row < size:
			r = free_row
			lock.acquire()
			free_row += 1
			lock.release()
			processRow(r, size)
			
	for n in range(numOfThreads):
		threads.append(threading.Thread(target=threadTarget))
		threads[-1].start()
	
	for thread in threads:
		thread.join()
	
	return result
	
if __name__ == "__main__":
	size = int(sys.argv[1])
	numOfThreads = int(sys.argv[2])
	a = randomMatrix(size)
	b = randomMatrix(size)
	start = time.time()
	res1 = multiplyThreaded(a, b, size, 1)
	print("Normal calculation took",time.time() - start, "s")
	start = time.time()
	res2 = multiplyThreaded(a, b, size, numOfThreads)
	print("Threaded multiplication with",numOfThreads,"threads took",time.time() - start,"s")