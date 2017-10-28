import urllib2

response = urllib2.urlopen('http://www.baidu.com')
# urlopen(url, data, timeout)
# 第一个参数url即为URL.
# 第二个参数data是访问URL时要传送的数据.
# 第三个timeout是设置超时时间

# data默认为空None

# timeout默认为 socket._GLOBAL_DEFAULT_TIMEOUT
# 可以设置等待多久超时，为了解决一些网站实在响应过慢而造成的影响


print response.read()
# 返回获取到的网页内容。