# coding: utf-8
from neteasemusic.settings import PROXIES
from fake_useragent import UserAgent
import requests
import random

TIMEOUT = 5


def choice_proxy():
    if PROXIES:
        return random.choice(PROXIES)
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
    headers={
        'Cookie':'appver=1.5.0.75771;',
        'Referer':'http://music.163.com/'
    }

    return requests.post(url,headers=headers,data=)