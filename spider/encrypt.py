# coding: utf-8
import base64
import json
import os
import platform

if platform.system() == 'Darwin':
    try:
        import crypto
        import sys

        sys.modules['Crypto'] = crypto
    except ImportError:
        pass

# https://github.com/darknessomi/musicbox/wiki/网易云音乐新版WebAPI分析
from Crypto.Cipher import AES


def aes_encrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsa_encrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text, 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def create_secretKey(size):
    data = os.urandom(size)
    # for i in data:
    #     s=hex(i)[2:]
    #     print(i)
    return ''.join(map(lambda xx: (hex(xx)[2:]), os.urandom(size)))[0:16]


def gen_data():
    text = {
        'username': '18665937537',
        'password': 'liubiaocan7537',
        'rememberLogin': 'true'
    }

    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'
    text = json.dumps(text)
    secKey = create_secretKey(16)
    encText = aes_encrypt(aes_encrypt(text, nonce).decode(), secKey)
    encSecKey = rsa_encrypt(secKey, pubKey, modulus)
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }
    return data
