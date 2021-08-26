import requests
from bs4 import BeautifulSoup
NUM_COLUMNS = 4
from typing import List
from CITY_TO_STATE import city_to_state
URL = "https://www.craigslist.org/about/sites"
KEYWORDS = ["multi", "multi%20family",  "multi%20unit",  "multi-family", "multi-unit", "multifamily", "multiunit"]
UNIT_AMOUNT = [str(i) + " " + "unit" for i in range(251)]
SEARCH_TERMS = KEYWORDS


def generate_location_urls() -> List[str]:
    main_page = requests.get(URL)
    soup = BeautifulSoup(main_page.content, 'html.parser')
    state_columns = []
    all_cities_hyperlinks = []
    for i in range(NUM_COLUMNS):
        state_columns.append(soup.find(class_=f"box box_{i + 1}"))
    
    # Find all the <li> elements on the html page and append them
    # state columns
    for element in state_columns:
        all_cities_hyperlinks.extend(element.find_all('li'))

    #Change all the enteries in <all_cities_hyperlinks> into actual urls
    for j in range(len(all_cities_hyperlinks)):
        all_cities_hyperlinks[j] = str(all_cities_hyperlinks[j]).split("\"")[1]
    
    return all_cities_hyperlinks


def generate_queries_per_area(all_cities_hyperlinks: List[str], today=True) -> List[str]:
    query_list= []
    if not today:
        for city in all_cities_hyperlinks:
            for term in SEARCH_TERMS:
                query_list.append(city + f"search/reo?query={term}")
    if today:
        for city in all_cities_hyperlinks:
            for term in SEARCH_TERMS:
                query_list.append(city +
                            f"search/reo?query={term}&searchNearby=0&bundleDuplicates=1&postedToday=1")
    return query_list


def filter_out_empty_enteries(query_list: List[str]) -> List[str]:
    list_to_email = []
    for query in query_list:
        result = BeautifulSoup(requests.get(query).content, 'html.parser').find_all("span", class_="button pagenum")
        if result != [] and str(result[0]) != "<span class=\"button pagenum\">no results</span>" and str(result[1]) != "<span class=\"button pagenum\">no results</span>":
            list_to_email.append(query)
    return list_to_email


def map_state_to_deals(list_to_email: List[str]) -> str:
    d= {}
    s = ""
    for url in list_to_email:
        location = url.split(".")[0][8:]
        d.setdefault(city_to_state[location], [])
        d[city_to_state[location]].append(url)

    s = ""
    for state, urls in d.items():
        s += "<br>"
        s += f"<T>{state}</T>"
        for i in range(len(urls)):
            if i == len(urls) - 1:
                s += "</ul>"
                s += "<br>"
            elif i == 0:
                s += "<ul>"
            else:
                s += f"<li>{urls[i]}"
    return s


def data(daily: bool) -> str:
    if daily:
            return map_state_to_deals(filter_out_empty_enteries(generate_queries_per_area(generate_location_urls(),today=True)))
    else:
        return map_state_to_deals(filter_out_empty_enteries(generate_queries_per_area(generate_location_urls(),today=False)))
