# -*- coding: UTF-8 -*-

import threading
import time

exitFlag = 0
#  exitflag参数中的数字：0、到达最大迭代次数或到达函数评价

class mythread(threading.Thread):
	"""docstring for mythread"""
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__( self )
		# 如果有参数，可以封装在类里面 
		self.threadID = threadID
		self.name = name
		self.counter = counter
        # 参数
        # self在定义时需要定义，但是在调用时会自动传入
        # self的名字并不是规定死的，this=self ,但是最好还是按照约定是用self
        # self总是指调用时的类的实例
        # 参考 http://python.jobbole.com/81921/

	def run(self):
		# #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
		print 'staring ' + self.name
		print_time(self.name, self.counter, 5)
		print 'exiting ' + self.name
		pass

def print_time(threadName, delay, counter):
	while counter:
		if exitFlag:
			thread.exit()
			time.sleep(delay)
			print 'the time is %s: %s' % (threadName,time.ctime(time.time()))
			counter -= 1
			pass
		pass
				

# 创建新线程
thread1 = mythread(1, "Thread-1", 1)
thread2 = mythread(2, "Thread-2", 2)

# 开启线程
thread1.start()
thread2.start()

print "\nExiting Main Thread"