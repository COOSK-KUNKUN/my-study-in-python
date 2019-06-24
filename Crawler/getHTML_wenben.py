# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup



HEADER = {
    "Host": "http://www.henannu.edu.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0"
}

html = """

<html>
<head>
<title>
</head>
<body>
<p class="title" name="description"><b>111</b></p>
<li><!——注释——></li>
<a href="http://www.henannu.edu.cn/2017/1024/c8955a104591/page.htm">党委理论学习中心组（扩大）学习通知 </a>
</body>
</html>
"""

soup = BeautifulSoup(html,'lxml')

print soup


