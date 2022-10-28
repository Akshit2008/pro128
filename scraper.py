from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import csv

START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

browser = webdriver.Chrome("C:/Users/kulka/Desktop/c128-main/chromedriver.exe")
browser.get(START_URL)

time.sleep(20)

stars_data = []
headers = ["name", "Distance","Mass","Radius","hyperlink","magnitude"]

def scrape():
    for i in range(1,5):
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")


        for th_tag in soup.find_all("th", attrs={"class", "exoplanet"}):
            tr_tags = th_tag.find_all("tr")
            temp_list = []
            for index, tr_tag in enumerate(tr_tags):
                if index == 0:
                    temp_list.append(tr_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(tr_tag.contents[0])
                    except:
                        temp_list.append("")

            # Get Hyperlink Tag
            hyperlink_tr_tag = tr_tags[0]

            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            
            star_data.append(temp_list)

        browser.find_element(By.XPATH, value='//*[@id="mw-content-text"]/div[1]/table[4]/tbody/tr[1]/td[1]/a').click()

scrape()

new_stars_data = []

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
      
        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("tr"):
            td_tags = tr_tag.find_all("td")
          
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div"))
                except:
                    temp_list.append("")
                    
        new_stars_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

#Calling method

for index, data in enumerate(stars_data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

print(new_stars_data[0:10])

final_star_data = []

for index, data in enumerate(stars_data):
    new_star_data_element = new_stars_data[index]
    new_star_data_element = [elem.replace("\n", "") for elem in new_star_data_element]
    new_star_data_element = new_star_data_element[:7]
    final_star_data.append(data + new_star_data_element)

with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_star_data)

