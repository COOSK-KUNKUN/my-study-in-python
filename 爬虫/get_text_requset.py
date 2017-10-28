import urllib

request = urllib2.Request('http：//www.baidu.com')

request = urllib2.urlopen(request)

print response.read()