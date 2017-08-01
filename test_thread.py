# -*- coding: UTF-8 -*-

# 多线程
# Python中使用线程有两种方式：函数或者用类来包装线程对象
# 函数式：调用thread模块中的start_new_thread()函数来产生新线程。语法如下:
# thread.start_new_thread ( function, args[, kwargs] )
# function - 线程函数
# args - 传递给线程函数的参数,他必须是个tuple类型
# kwargs - 可选参数

import thread
import time

def timedata( threadName, delay):
	count = 0
	while count < 10 :
		time.sleep(delay)         # time sleep() 函数推迟调用线程的运行，可通过参数secs指秒数，表示进程挂起的时间。 
		count += 1
		print 'the time is %s:%s' % (threadName,time.ctime(time.time()))
		pass
	pass

try:
 	thread.start_new_thread( timedata,('thread-1', 2,))
 	thread.start_new_thread( timedata,('thread-2', 4,))
	pass
except :
	print 'error'

while 1:                          # 避免线程1与线程2冲突，当线程1执行完到线程2
	pass

	