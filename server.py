# -*- coding: UTF-8 -*-

# socket编程思路
# 1 创建套接字，绑定套接字到本地IP与端口
# socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.bind()
# 2 开始监听连接                           #s.listen()
# 3 进入循环，不断接受客户端的连接请求       #s.accept()
# 4 然后接收传来的数据，并发送给对方数据     #s.recv() , s.sendall()
# 5 传输完毕后，关闭套接字                  #s.close()

# 报错
# File "C:\Users\Administrator\Desktop\server.py", line 11, in <module>
# import socket
# File "C:\Users\Administrator\Desktop\socket.py", line 13, in <module>
# socketpair() -- create a pair of new socket objects [*]
# TypeError: 'module' object is not callable
import socket

import sys

s = socket.socket()             # 创建 socket 对象
host = socket.gethostname()		# 获取本地主机名
port = 8080					    # 设置端口
s.bind((host, port))			# 绑定端口 绑定地址（host,port）到套接字， 在AF_INET下,以元组（host,port）的形式表示地址

s.listen(5)                     # 等待客户端连接 开始TCP监听
while True:
    c, addr = s.accept()        # 建立客户端连接。
    print '连接地址：', addr
    c.send('coosk-kunkun.github.io')
    c.close()                   # 关闭连接

# s.accept() 被动接受TCP客户端连接,(阻塞式)等待连接的到来 即建立客户端连接
# c, addr = s.accept() 中的c接收conn，addr接收address
# conn 是新的套接字对象，可以用来接收和发送数据        