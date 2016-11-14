import requests
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
