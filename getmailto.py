# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
import pickle

def getinfo(driver,filelist):

	for i in filelist:
		
		url="https://www.virustotal.com/gui/file/"+i+"/content/preview"
		info=driver.get(url)
		time.sleep(2)
		a=driver.execute_script('''return document.querySelector("vt-virustotal-app").shadowRoot.querySelector("file-view").shadowRoot.querySelector("vt-ui-file-content");''')
		#print a 
		b=driver.execute_script('''return arguments[0].shadowRoot.querySelector("iframe");''',a)
		#print b
		if b==None:
			print "cannot find file address"
			continue
		c=b.get_attribute("src")
		driver.maximize_window()
		driver.get(c)
		time.sleep(10)
		filename=i+".png"
		driver.get_screenshot_as_file(filename)
		print filename
		print c
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
		chromepath=raw_input("your chromedriver.exe path:")
		driver = webdriver.Chrome(chromepath)
		driver.set_window_size(1124, 850)  # 防止得到的WebElement的状态is_displayed为False，即不可见
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
