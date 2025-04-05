from bs4 import BeautifulSoup
import requests
from foodClass import Food

import json
import os


CACHE_FILE = "D2Cache.json"



htmltext = requests.get("https://foodpro.students.vt.edu/menus/MenuAtLocation.aspx?locationNum=15&naFlag=1&myaction=read&dtdate=4%2f3%2f2025").text
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

#This makes it so that this code will run only if ran as current file
if __name__ == "__main__":
    string = getMenu(2)

    start = 0
    done = False
    print("hi")

    while not done:
        indexOne = string.index("[", start)

        if "[" not in string[indexOne + 1:]:
            print(string[indexOne:].strip())
            done = True
        else:
            indexTwo = string.index("[", indexOne + 1)
            print(string[indexOne:indexTwo].strip())
            start = indexTwo






