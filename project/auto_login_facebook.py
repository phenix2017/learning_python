from selenium import webdriver

import time
from getpass import getpass 

browser = webdriver.Chrome()

browser.get("https://www.facebook.com/")
time.sleep(20)
# browser.quit()

""" Auto login """
username_box = browser.find_element_by_id('email')
user_name = input("Enter your user name")
username_box.send_keys(user_name)
time.sleep(1)
password_box = browser.find_element_by_id('pass') 
pwd = getpass("Enter your password")
password_box.send_keys(pwd) 
login_box = browser.find_element_by_id('loginbutton') 
login_box.click() 

