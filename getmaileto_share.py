# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pickle

def getinfo(driver,filelist):
	filename='result_'+time.strftime("%Y-%m-%d",time.localtime())+'.csv'
	fileout=open(filename,'w')
	for i in filelist:
		print i
		url="https://www.virustotal.com/gui/file/"+i+"/content/strings"
		info=driver.get(url)
		time.sleep(5)
		a=driver.execute_script('''return document.querySelector("vt-virustotal-app").shadowRoot.querySelector("file-view").shadowRoot.querySelector("vt-ui-file-content");''')
		#print a 

		b=driver.execute_script('''return arguments[0].shadowRoot.querySelector("div.strings-container");''',a)

		c=driver.execute_script('''return arguments[0].querySelectorAll("a.pivotable");''',b)
		strout=i+','
		for j in c:
			str=j.text
			if str.startswith('To:')!=-1:
				str.replace('\r','').replace('\n','')
				strout+=str+';'
		fileout.write(strout)
		fileout.write('\n')
	fileout.close()
	return 1
def hashfile():
	hashlist=[]
	fileconfig=raw_input("where is sha256:")
	fileconfig=open(fileconfig,'r')
	line=fileconfig.readline()
	while line:
		hashlist.append(line.replace('\r','').replace('\n',''))
		line=fileconfig.readline()
	fileconfig.close()
	return hashlist
def login():
	loginname = ""
	password = ""
	try:
		chrome_options = Options()
		chrome_options.add_argument('window-size=1920x3000') #指定浏览器分辨率
		chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
		chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
		chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
		chromepath=raw_input("input your chromedriver path")
		driver = webdriver.Chrome(chromepath)
		driver.get("https://www.virustotal.com/gui/sign-in")
		time.sleep(2)
		#自动点击并输入用户名
		a=driver.execute_script('''return document.querySelector("vt-virustotal-app").shadowRoot.querySelector("sign-in-view")''')
		b=driver.execute_script('''return arguments[0].shadowRoot.querySelector("vt-ui-text-input#email");''',a)
		d=driver.execute_script('''return arguments[0].shadowRoot.querySelector("vt-ui-text-input#password");''',a)
		f=driver.execute_script('''return arguments[0].shadowRoot.querySelector("vt-ui-button");''',a)
		#print(a)
		c=driver.execute_script(''' return arguments[0].shadowRoot.querySelector("input");''',b)
		e=driver.execute_script(''' return arguments[0].shadowRoot.querySelector("input");''',d)
		#print(b)
		loginname=raw_input("your account:")
		password=raw_input("your password:")
		c.send_keys(loginname)
		e.send_keys(password)
		f.click()
		filelist=hashfile()
		if getinfo(driver,filelist):
			print "well done"
	except Exception as e:
		print(e)
login()
