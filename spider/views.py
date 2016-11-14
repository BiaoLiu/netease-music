import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def test(request):
    data = {'userid': '11111111'}

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, compress',
               'Accept-Language': 'en-us;q=0.5,en;q=0.3',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
               }

    cookies = {'testCookies_1': 'Hello_Python3', 'testCookies_2': 'Hello_Requests'}

    s = requests.Session()
    s.headers.update(headers)

    result = s.post('http://119.29.144.39:8008/api/main/gethotquestionlist', data, cookies=cookies)

    # result = requests.post('http://119.29.144.39:8008/api/main/gethotquestionlist', data)

    data = result.json()
    data = result.content
    data = result.raw
    data = result.headers
    data = result.encoding
    data = result.status_code

    return HttpResponse('success')


def bs4_test(request):
    html_doc = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>

    <p class="story">...</p>
    """

    soup = BeautifulSoup(html_doc, 'lxml')

    data = soup.title

    return HttpResponse('success')
