from bs4 import BeautifulSoup
import requests

htmltext = requests.get("https://foodpro.students.vt.edu/menus/label.aspx?locationNum=15&dtdate=01%2f21%2f2025&RecNumAndPort=212031*1").text
soup = BeautifulSoup(htmltext, "lxml") #intialize the parser

carbs = soup.find("div", class_="col-lg-12 daily_value total_carbohydrates").text.strip()
carbs = carbs.split()[2]

protein = soup.find("div", class_="col-lg-12 daily_value protein").text.strip()
protein = protein.split()[1]

print(type(protein))