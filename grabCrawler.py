#!/full/path/to/your/custom/python/executable
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import pandas as Pd
import requests
import csv

from webdriver_manager.chrome import ChromeDriverManager
restaurants=[]
latitude=[]
longitude=[]
Wdriver=webdriver.Chrome(ChromeDriverManager().install())
Wdriver.get("https://food.grab.com/sg/en/")
sleep(5)
get_location=Wdriver.find_element_by_id("location-input")
get_location.send_keys("johor bahru")
enter_button=Wdriver.find_element_by_class("ant-btn submitBtn___2roqB ant-btn-primary")
enter_button.click()
sleep(5)
load_more=Wdriver.find_element_by_class("ant-btn ant-btn-class")
for i in(0,6,1):
   load_more.click()
   sleep(2)
Spage=Wdriver.page_source
soup=BS(Spage)
for a in soup.findAll('a',href=True,attrs={'class':'ant-row-flex RestaurantListRow___1SbZY'}):
   rname=a.find('div', attrs={'class':'name___2epcT'})
   restaurants.append(rname.text)

url_elements = Wdriver.find_elements_by_xpath("//a[contains(@href, '/ph/sg/restaurant')]")
url_elements_list = []
for url_element in url_elements:
    url_elements_list.append(url_element.get_attribute("href"))
url_elements_list = url_elements_list[10:]   
for url in url_elements_list:
    url_page=requests.get(url)
    url_page = BS(url_page.text, 'html.parser')
    test_text = url_page.text.find('latlng":{')
    restaurant_latitude = url_page.text[test_text+20:test_text+30]
    restaurant_longitude = url_page.text[test_text+43:test_text+54]
    latitude.append(restaurant_latitiude.text)
    longitude.append(restaurant_logitude.text)
    
df = pd.DataFrame({'Restaurant name':restaurants,'Latitude':latitude,'Longitude':longitude}) 
df.to_csv('Restaurant_location_list.csv', index=True, encoding='utf-8')

Wdriver.close()

