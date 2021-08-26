import requests
from bs4 import BeautifulSoup
NUM_COLUMNS = 4
from typing import *
import smtplib, ssl
from email.mime.text import MIMEText
from getpass import getpass
from email.mime.multipart import MIMEMultipart
URL = "https://www.craigslist.org/about/sites"

def generate_location_urls() -> Dict:
    main_page = requests.get(URL)
    soup = BeautifulSoup(main_page.content, 'html.parser')
    state_columns = []
    all_cities_hyperlinks = []
    all_states = []
    d = {}
    g = {}
    for i in range(NUM_COLUMNS):
        state_columns.append(soup.find(class_=f"box box_{i + 1}"))
    
    # Find all the <li> elements on the html page and append them
    # state columns
    for element in state_columns:
        all_cities_hyperlinks.append(element.find_all('ul'))
        all_states.append(element.find_all('h4'))

    for i in range(len(all_states)):
        for j in range(len(all_states[i])):
            all_states[i][j] = str(all_states[i][j]).replace("<h4>","").replace("</h4>","")
    
    for m in range(len(all_cities_hyperlinks)):
        for n in range(len(all_cities_hyperlinks[m])):
            item = str(all_cities_hyperlinks[m][n]).replace("<li><a href=\"https://", "").replace("<ul>", "").replace("</ul>", "").replace(".craigslist.org", "").replace("/\">", " ").replace("</a></li>", "").split("\n")[1:-1]
            for x in range(len(item)):
                item[x] = item[x].split(" ")[0]
            all_cities_hyperlinks[m][n] = item

    
    for t in range(len(all_cities_hyperlinks)):
        for l in range(len(all_cities_hyperlinks[i])):
            d[all_states[t][l]] = all_cities_hyperlinks[t][l]

    
    for state, city_list in d.items():
        for city in city_list:
            g[city] = state
    
    return g

city_to_state = generate_location_urls()

if __name__ == '__main__':
    print(city_to_state)
    print("HELLO")
