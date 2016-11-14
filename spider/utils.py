# coding: utf-8
from lxml import etree

from django.conf import settings
from fake_useragent import UserAgent
import requests
import random

from spider.encrypt import gen_data

TIMEOUT = 5


def choice_proxy():
    if settings.PROXIES:
        return random.choice(settings.PROXIES)
    return ''


def get_user_agent():
    ua = UserAgent()
    return ua.random


def fetch(url, retry=0):
    s = requests.Session()
    proxies = {
        'http': choice_proxy()
    }
    s.headers.update({'user-agent': get_user_agent(),
                      'referer': 'http://music.163.com/'})

    try:
        return s.get(url, timeout=TIMEOUT, proxies=proxies)
    except requests.exceptions.RequestException:
        if retry < 3:
            return fetch(url, retry=retry + 1)
        raise


def post(url):
    headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/'
    }

    return requests.post(url, headers=headers, data=gen_data())


def get_html(url):
    result = fetch(url)
    return etree.HTML(result.text)
