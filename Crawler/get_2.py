# -*- coding: UTF-8 -*-

import requests
import bs4


def get_data(url):

    list = {}
    response = requests.get('http://www.henannu.edu.cn/8955/list')
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    for meta in soup.select('meta'):
        if meta.get('name') == 'description':
            list["content"] = meta.get('content')
    return list

if __name__ == '__main__':
    print list









