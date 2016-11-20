# -*- coding:utf-8 -*-
import os
from bs4 import BeautifulSoup
import requests
from PIL import Image
import re

session = requests.Session()
headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36",
        "Host": "accounts.douban.com",
        "Referer": 'https://accounts.douban.com/login',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

def login(account,password):
    url = "https://accounts.douban.com/login"
    redirUrl = 'https://www.douban.com/'
    req=session.get(url,headers=headers)
    bsObj=BeautifulSoup(req.text)
    captcha_image=bsObj.find('img',{'id':'captcha_image'})
    params = {'source': 'None', 'redir': redirUrl, 'form_email': account, 'form_password': password, 'login': '登录'}
    if captcha_image != None:
        params['captcha-solution']=captchaSolution(captcha_image['src'])
        params['captcha-id']=captchaId(captcha_image['src'])+':en'
    req = session.post(url, headers=headers,data=params)
    response = session.get(redirUrl, cookies = req.cookies, headers = headers)
    bsObj=BeautifulSoup(response.text)
    if len(bsObj.findAll('a',{'id':'edloc'}))!=0:
        print '登录成功！'
    else:
        print '登录失败！'

def captchaSolution(imageUrl):
    r = session.get(imageUrl, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    im = Image.open('captcha.jpg')
    im.show()
    im.close()
    captcha = raw_input("please input the captcha:")
    return captcha

def captchaId(imageUrl):
    pattern=re.compile(r'(?<=id\=)\w+')
    return pattern.findall(imageUrl)[0]

if __name__ == '__main__':
    account = raw_input('请输入你的用户名:')
    password = raw_input("请输入你的密码:")
    login(account,password)