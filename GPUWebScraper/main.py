# Graphics Card Web Scraping Tool
# collect data from https://nftcalendar.io/events/ and input into excel sheet on local
# Libraries: BeautifulSoup and Request

from bs4 import BeautifulSoup
import requests
import re

search_term = input("What GPU do you want to search for? ")
url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131"

page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser") 

# find how many pages exist with search_term
page_text= doc.find(class_= "list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split('>')[1][:1])

# store results
items_found = {}

# loop and send a request for each page and find all relevant items
for page in range(1, int(pages) + 1):
    url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&{page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")

    # Will also include strings that contain search_term
    items = div.find_all(text=re.compile(search_term)) 

    # grab parent of all items to grab link
    for item in items:
        parent = item.parent
        #  make sure all parents have an anchor tag
        if parent.name != "a":
             continue
        
        link = parent['href']
        next_parent = item.find_parent(class_="item-container")

        # makes sure there is a strong tag
        try:
            price = next_parent.find(class_="price-current").strong.string

            # item is key, price and value is another dictionary stored as the value
            items_found[item] = {"price" : int(price.replace(",", "")), "link" : link}
        except:
            pass

# .items() returns tuple. [1] of tuple is the dictonary and we index the 'price' value to be sorted
sorted_items = sorted(items_found.items(), lambda x: x[1]['price'])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])

