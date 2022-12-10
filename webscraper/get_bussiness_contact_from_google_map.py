#!/usr/bin/env python
# coding: utf-8

# import requests # 
import pandas as pd
import numpy as np
import time
import pymysql
import re
import selenium
from lxml import etree
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, ElementClickInterceptedException
# C:\Program Files (x86)
import os
driver_path = os.path.realpath(r"C:\Program Files (x86)")
driver = webdriver.Chrome(os.path.join(driver_path,"chromedriver.exe"))
companies_name_list = []
phone_number_list = []
web_url_list = []
# all_url = 'https://info.yorkbbs.ca/list/plumer'
# list_of_cities_path = '.\list_of_cities.csv'
# list_of_cities_abs_path = os.path.realpath(list_of_cities_path)
# df_cities = pd.read_csv(list_of_cities_abs_path, header=1, encoding='utf-8-sig')
# list_of_cities = df_cities.iloc[:,1].values.tolist()
list_of_cities = ['Toronto']
for city in list_of_cities:
    print(city)
    all_url = r'https://www.google.com/search?tbs=lf:1,lf_ui:14&tbm=lcl&sxsrf=ALiCzsbGR5GR67mdpB3HQLoPmOX7db9Hng:1670037699126&q=electrician+{}'.format(city)
    driver.get(all_url)
    def wait_for_available():
        try:
            time.sleep(10)
            element = WebDriverWait(driver, 50).until(
                EC.visibility_of_element_located((By.XPATH, './/div[@class="VkpGBb"]'))
            )
        except:
            print("I am quiting")
            # driver.quit()
        else:
            print("I am executing normally")
            time.sleep(1)
        finally:
            print("The wait process has done")
    wait_for_available()
    # Obtain the company session
    last_page = driver.find_elements(by=By.XPATH, value='//a[@class="fl"][last()]')  
    last_page_number = int(last_page[-1].accessible_name.removeprefix("Page "))
    # len(companies_section) # Get all the companies in the page
    # Indicator of the curruent page
    # //*[@id="rl_ist0"]/div/div[2]/div/table/tbody/tr/td[2]/text()
    for page in range(1,last_page_number+1):
        companies_section = driver.find_elements(by=By.XPATH, value='.//div[@class="VkpGBb"]')  
        print('Page {}'.format(page))
        for comany_section in companies_section:
            try: 
                company_section_info = comany_section.find_elements(By.XPATH, ".//div[@class='rllt__details']")[0].text
                companies_name_list.append(company_section_info)
            except NoSuchElementException:
                pass
            try:
                web_url = comany_section.find_elements(By.XPATH, './a[@class="yYlJEf Q7PwXb L48Cpd"]')
                print(len(web_url))
            except:
                pass
            else:
                if len(web_url) !=0:
                    web_url_list.append(web_url[0].get_property('href'))
                else:
                    web_url_list.append(np.nan)

        try:
            next_button_list = driver.find_elements(by=By.XPATH, value='//*[@id="pnnext"]/span[2]')  
            print("Button {}".format(next_button_list[0].accessible_name))
            if len(next_button_list) != 0:
                next_button_list[0].click()
        except:
            print("next button has handle errors")
        wait_for_available()

print(len(phone_number_list))
print(len(companies_name_list))
print(len(web_url_list))
df = pd.DataFrame()
# df['Phone'] = phone_number_list
df['Compay'] = companies_name_list
df['href'] = web_url_list
df.to_csv("google_electrician_toronto.csv",encoding='utf-8')
driver.quit()
