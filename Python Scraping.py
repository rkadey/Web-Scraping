# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 09:52:10 2023

@author: User
"""
#%% Libraries

import requests
import bs4                                                               
import pandas as pd

#%% Lists

Sales_title = []
Distance = []
Price = []
Year = []
Mileage = []
Fuel_Type = []
Transmission = []
Number_Of_Doors = [] 
Colour = [] 
Doors = [] 
Engine_size = []
CO2_Emissions = []
Body_Type = []
Rating = []
Number_of_Reviews = []

#%% Request Page

page = 5    # Update this to reflect the page number
url = f"https://www.theaa.com/used-cars/displaycars?fullpostcode=SW84JD&page={page}"

response = requests.get(url, 
                    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'},
                    timeout = 10
                    )
print(response.status_code)

soup = bs4.BeautifulSoup(response.text, "html.parser")

cars = soup.find_all("div", {"class" : "vl-item clearfix"})

#%% Retrieve Data    


for car in cars:
    
    distance = car.find('div', {'class' : 'vl-location'})
    Distance.append(distance.text)
    
#%%: Collect Extra Data

base_url = "https://www.theaa.com/"

Vehicle_details_url = []

for car in cars:
    vehicle_details_url = str(base_url + car.find('a').get('href'))
    Vehicle_details_url.append(vehicle_details_url)

#%%  Retrieve Data

for link in (Vehicle_details_url):
    response2 = requests.get(link, 
                        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'},
                        timeout = 10
                        )
    soup2 = bs4.BeautifulSoup(response2.text, "html.parser")
    
    car_make = soup2.find('span', class_= 'make').text
    car_title = soup2.find('span', class_= 'variant new-transport--regular').text

    sale_title = car_make + " " + car_title
    Sales_title.append(sale_title)
    
    price = soup2.find('strong', class_= 'total-price new-transport--bold').text
    Price.append(price)
    
    mileage = soup2.find_all('span', class_='vd-spec-value')[0].text
    Mileage.append(mileage)
    
    year = soup2.find_all('span', class_='vd-spec-value')[1].text
    Year.append(year)
    
    fuel_Type = soup2.find_all('span', class_='vd-spec-value')[2].text
    Fuel_Type.append(fuel_Type)
    
    transmission = soup2.find_all('span', class_='vd-spec-value')[3].text
    Transmission.append(transmission)
    
    body_Type = soup2.find_all('span', class_='vd-spec-value')[4].text
    Body_Type.append(body_Type)
    
    colour = soup2.find_all('span', class_='vd-spec-value')[5].text
    Colour.append(colour)
    
    doors = soup2.find_all('span', {'class' : 'vd-spec-value'})[6].text
    Number_Of_Doors.append(doors)
    
    
    if len(soup2.find_all('span', {'class':'vd-spec-value'})) <= 7:
        engine_size = "None"
        Engine_size.append(engine_size)
    else:
        engine_size = soup2.find_all('span', {'class':'vd-spec-value'})[7].text
        Engine_size.append(engine_size)
       
    if len(soup2.find_all('span', {'class':'vd-spec-value'})) <= 8:
        cO2_emissions = "None"
        CO2_Emissions.append(cO2_emissions)
    else:
        cO2_emissions = soup2.find_all('span', {'class':'vd-spec-value'})[8].text
        CO2_Emissions.append(cO2_emissions)
    
    
    
    if soup2.find("div", {"itemprop" : "reviewCount"}) is None:
        review_count = "None"
        Number_of_Reviews.append(review_count)
    else:
        review_count = soup2.find("div", {"itemprop" : "reviewCount"}).get('content')
        Number_of_Reviews.append(review_count)

    
    if soup2.find("div", {"itemprop" : "ratingValue"}) is None:
        rating_value = "None"
        Rating.append(rating_value)
    else:
        rating_value = soup2.find("div", {"itemprop" : "ratingValue"}).get('content')
        Rating.append(rating_value)


# In[]: Save Data

dict = {"Sales_title" : Sales_title,
        "Distance" : Distance,
        "Price" : Price,
        "Mileage" : Mileage,
        "Year" : Year,
        "Fuel_Type" : Fuel_Type,
        "Transmission" : Transmission,
        "Body_Type" : Body_Type,
        "Colour" : Colour,
        "Doors" : Number_Of_Doors,
        "Engine_size" : Engine_size,
        "CO2_Emissions" : CO2_Emissions,
        "Rating" : Rating,
        "Number_of_Reviews" :Number_of_Reviews
        }

df = pd.DataFrame(dict)