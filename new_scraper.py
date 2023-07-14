from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service 
import requests
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
service = Service(executable_path = "C:/Users/aviji/OneDrive/Desktop/PRO-C128-Student-Boilerplate-Code-main/PRO-C128-Student-Boilerplate-Code-main/chromedriver.exe")

# Webdriver
browser = webdriver.Chrome(service = service)

time.sleep(10)

new_planets_data = []

def scrape_more_data(hyperlink):
    try: 
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temporary_list = []
        for tr_tag in soup.find_all("tr", attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try: 
                    temporary_list.append(td_tag.find_all("div", attrs={"class":"value"})[0].contents[0])
                except:
                    temporary_list.append("")
        new_planets_data.append(temporary_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)


planet_df_1 = pd.read_csv("updated_scraped_data.csv")

# Call method
for index, row in planet_df_1.iterrows():
    print(row["hyperlink"])
    scrape_more_data(row["hyperlink"])
    print(f"Data Scraping at hyperlink {index+1} completed")

print(new_planets_data[0:10])

# Remove '\n' character from the scraped data
scraped_data = []

for row in new_planets_data:
    replaced = []
    for el in row:
        el = el.replace("\n", "")
        replaced.append(el)  

    scraped_data.append(replaced)

print(scraped_data)

headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]

new_planet_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convert to CSV
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")
