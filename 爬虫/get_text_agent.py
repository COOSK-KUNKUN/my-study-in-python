import urllib
import urllib 2

url = 'https://www.zhihu.com/'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

value = {'usename': 'cpc', 'password': 'xxxx'}

header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' , 'Referer':'http://www.zhihu.com/articles'}

data = urllib.urlencode(value)

enable_proxy = True

proxy_handler = urllib2.ProxyHandler({'http': 'http://some-proxy.com:8080'})

null_proxy_handler = urllib2.ProxyHandler({})
    if enable_proxy:
        opener = urllib2.bulid_opener(proxy_handler)
    else :
        opener = urllib2.bulid_opener(null_proxy_handler)
        pass
urllib2.install_opener(opener)
# Proxy（代理）的设置
# 每隔一段时间换一个代理

request = urllib2.Request(url, data, header)

reponse = urllib2.urlopen(request)

page = reponse.read()

