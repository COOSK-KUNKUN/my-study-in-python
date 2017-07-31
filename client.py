# -*- coding: UTF-8 -*-

import socket

s = socket.socket()
host = socket.gethostname()
port = 8080

s.connect((host, port))
print s.recv(1024)
s.close()