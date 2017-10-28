import urllib2

requset = urllib2.Request( 'http://www.baidu.com')

try:
    urllib2.urlopen(requset)
    print ('get it')
    pass
except urllib2.URLError, e:
    print e.reason

# 用try-except语句来包围并捕获相应的异常