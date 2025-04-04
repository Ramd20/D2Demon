from bs4 import BeautifulSoup
import requests
from foodClass import Food

import json
import os


CACHE_FILE = "D2Cache.json"



htmltext = requests.get("https://foodpro.students.vt.edu/menus/MenuAtLocation.aspx?locationNum=15&naFlag=1&myaction=read&dtdate=3%2f27%2f2025").text
soup = BeautifulSoup(htmltext, "lxml")

nutritionurl = "https://foodpro.students.vt.edu/menus/"



def getNutrition(item, link):
    nutritionLabel = requests.get(link).text
    parser = BeautifulSoup(nutritionLabel, "lxml")

    numberCalorie = parser.find("div", id="calories_container").text.strip()
    numberCalorie = (" ".join(numberCalorie.split())).split()[-1]

    carbs = parser.find("div", class_="col-lg-12 daily_value total_carbohydrates").text.strip()
    carbs = carbs.split()[2]

    protein = parser.find("div", class_="col-lg-12 daily_value protein").text.strip()
    protein = protein.split()[1]

    return Food(item, numberCalorie, protein, carbs)





def getMenu(meal):

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)

    else:
        cache = {}

    output = ""
    idString = "meal_" + str(meal) + "_content" #gets the meal page
    menu = soup.find("div", id=idString)
    cards = menu.find_all("div", class_ = "card")

    output += "**********************************\n"
    output += f"MEAL {meal}\n"
    output += "**********************************\n"

    for card in cards:
        output += f"[{card.find("div", class_ = "card-header").text.strip()}]\n"

        foods = card.find_all("div", class_ = "recipe_title")
        for food in foods:
            item = food.text.strip()
            if item in cache:
                output += cache[item] + "\n"
            else:
                link = nutritionurl + (food.find("a")["href"])
                cache[item] = getNutrition(item, link).__str__()
                output += cache[item] + "\n"



    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)


    return output


string = getMenu(1)
print(string)
lst = [1,2,3,1,4,5]
start = 0
done = False
while not done:

    indexOne = string.index("[", start)
    indexTwo = string.index("[", indexOne + 1)
    start = indexTwo + 1
    print(string[indexOne:indexTwo])
    if "[" not in string[start:]:
        print(string[indexTwo:len(string)])
        done = True






