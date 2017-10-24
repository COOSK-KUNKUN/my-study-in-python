# -*- coding: UTF-8 -*-

from flask import Flask
app = Flask(__name__)

@app.route('/') # route() 装饰器告诉 Flask 什么样的URL 能触发我们的函数
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
    # run() 函数来让应用运行在本地服务器上
