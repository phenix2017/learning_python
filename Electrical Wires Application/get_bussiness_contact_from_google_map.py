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
file_absolute_path_name = os.path.dirname(__file__)
# file_path = r"C:\Users\yubin\Documents\GitHubRepository\Electrical Wires Application"
file_path = file_absolute_path_name
list_of_cities_path = 'list_of_cities.csv'
list_of_cities_abs_path = os.path.join(file_path,list_of_cities_path)
print("The city list is in {}", list_of_cities_abs_path)
driver_path = os.path.realpath(r"C:\Program Files (x86)")
driver = webdriver.Chrome(os.path.join(driver_path,"chromedriver.exe"))
companies_name_list = []
phone_number_list = []
web_url_list = []
df_cities = pd.read_csv(list_of_cities_abs_path, header=1, encoding='utf-8-sig')
list_of_cities = df_cities.iloc[:,3].values.tolist() # The column includes "City,Province"
def get_google_map_data(list_of_cities, keyword,companies_name_list, phone_number_list, web_url_list):
    for city in list_of_cities:
        print("Obtain data of the {} city".format(city))
        keyword1 = "\""+ keyword +"\""
        keyword2 = "\""+city+".\""
        all_url = r'https://www.google.com/search?tbs=lf:1,lf_ui:14&tbm=lcl&sxsrf=ALiCzsbGR5GR67mdpB3HQLoPmOX7db9Hng:1670037699126&q={}+{}'.format(keyword1,keyword2)
        # all_url = r'https://www.google.com/maps/search/{}+{}'.format("Electrical Supply Store",city)
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
        if len(last_page) != 0:
            last_page_number = int(last_page[-1].accessible_name.removeprefix("Page "))
        else:
            last_page_number = 1
        for page in range(1,last_page_number+1):
            # Get the company section on the google map search 
            companies_section = driver.find_elements(by=By.XPATH, value='.//div[@class="VkpGBb"]')  
            print('Page {}'.format(page))
            # Deep into the company section to retrieve information from the company
            for comany_section in companies_section:
                try: 
                    first_layer_element_in_compay_session = comany_section.find_elements(By.XPATH, ".//div[@class='rllt__details']")[0].find_elements(By.XPATH,"./div")
                    company_name=""
                    company_phone=""
                    for company_info_item in first_layer_element_in_compay_session:
                        if company_info_item.get_attribute("class") == "dbg0pd":
                            company_name = company_info_item.text
                            continue
                        company_phone_candidate = company_info_item.text
                        if company_phone_candidate.lower().find("open") != -1: # Means it is the telephone line 
                            company_phone = company_phone_candidate.split("·")[-1].strip()
                            if sum(c.isalnum() for c in company_phone) != 10:
                                company_phone = np.nan
                    company_section_info = [company_name,company_phone]
                    companies_name_list.append(company_name)
                    phone_number_list.append(company_phone)
                except NoSuchElementException:
                    pass
                try:
                    web_url = comany_section.find_elements(By.XPATH, './a[@class="yYlJEf Q7PwXb L48Cpd"]')
                    if len(web_url) == 0:
                        print("No website avaialbe")
                except:
                    pass
                else:
                    if len(web_url) !=0:
                        web_url_list.append(web_url[0].get_property('href'))
                    else:
                        web_url_list.append(np.nan)

            try:
                next_button_list = driver.find_elements(by=By.XPATH, value='//*[@id="pnnext"]/span[2]')  
                print("pressed next button {}".format(next_button_list[0].text))
                if len(next_button_list) != 0:
                    next_button_list[0].click()
            except:
                print("next button has handle errors")
            wait_for_available()

keywords = ["Electrical Supply Store", "Lighting Store"]
for keyword in keywords:
    get_google_map_data(list_of_cities, keyword, companies_name_list, phone_number_list, web_url_list)
df = pd.DataFrame()
df['Compay'] = companies_name_list
df['Phone'] = phone_number_list
df['href'] = web_url_list
electrical_store_file = "google_electrical_store_cities.csv"
df.to_csv(electrical_store_file,encoding='utf-8')
driver.quit()
