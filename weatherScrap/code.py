import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "https://forecast.weather.gov/MapClick.php?lat=40.7146&lon=-74.0071#.XabNClUzbZ4"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.find_all('img'))
week = soup.find(id = 'seven-day-forecast-body')
#print(week)
#print(week.find_all('li'))
#print(week.find_all(class_='tombstone-container'))
items = week.find_all(class_='tombstone-container')
#print(items[0])
#print(items[0].find(class_='period-name').get_text())
#print(items[0].find(class_='short-desc').get_text())
#print(items[0].find(class_='temp').get_text())

period_name = [item.find(class_="period-name").get_text() for item in items]
short_description = [item.find(class_="short-desc").get_text() for item in items]
temperatures = [item.find(class_="temp").get_text() for item in items]
#print(period_name)
#print(short_description)
#print(temperatures)
for item in items:
    item = tuple(item)
    print(item[1])
    print(item[2])
    #print(item[3])
    print(item[4])
    print(item[5])

weather_stuff = pd.DataFrame({
    'Period': period_name,
    'Short_Description': short_description,
    'temperatures': temperatures
})
#print(weather_stuff)
weather_stuff.to_csv('weatherNewYork.csv')