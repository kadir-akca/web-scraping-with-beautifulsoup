from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests

my_url = "https://www.wollplatz.de/wolle/herstellers/"


# get the link of the researched brand
def get_link_brand(brand):
    my_link = ""
    try:
        req = requests.get(my_url)
        soup = BeautifulSoup(req.text, "html.parser")
        for a_href in soup.find_all("a", href=True):
            if brand in str(a_href).lower():
                my_link = a_href["href"]
                break
        return my_link
    except:
        print("URL is not correct")
        return


# get the link of the researched model
def get_link_model_in_brand(brand, model): #func
    my_link = ""
    for i in range(10):
        req = requests.get(get_link_brand(brand) + "?page=" + str(i))
        soup = BeautifulSoup(req.text, "html.parser")
        for a_href in soup.find_all("a", href=True):
            if model in str(a_href).lower() != -1:
                my_link = a_href["href"]
                break
    return my_link


# get every properties that we are looking for
def get_details(brand, model):
    req = requests.get(get_link_model_in_brand(brand, model))
    soup = BeautifulSoup(req.text, "html.parser")

    # get price
    my_price = soup.find("span", class_="product-price-amount").text

    # get delivery status
    my_delivery_statue = soup.find("div", id="ContentPlaceHolder1_upStockInfoDescription").find("span").text

    # get composition
    my_composition = ""
    temp = soup.find("div", id="pdetailTableSpecs").find_all("td")
    for comp in temp:
        if "Zusammenstellung" in comp:
            my_composition = temp[temp.index(comp) + 1].text
            break

    # get needle size
    my_needle_size = ""
    temp = soup.find("div", id="pdetailTableSpecs").find_all("td")
    for comp in temp:
        if "Nadelstärke" in comp:
            my_needle_size = temp[temp.index(comp) + 1].text
            break

    return np.array([brand + " " + model, my_price, my_delivery_statue, my_composition, my_needle_size])


def create_data():
    arr = []
    for i in search_list:
        try:
            arr.append(get_details(i[0].lower(), i[1].lower()))
        except:
            print(f"Item {i[0]} {i[1]} not found")
    df = pd.DataFrame(data=arr, columns=["Product", "Price", "Delivery", "Composition", "Needle Size"])
    df.to_csv('products.csv', index=True)
    print(df)


search_list = []
search_list.append(["DMc", "Natura xL"])
search_list.append(["drops", "safran"])
search_list.append(["DROPS", "baby merino mix"])
search_list.append(["hahn", "alpacca speciale"])
search_list.append(["stylecraf", "special double knit"])
search_list.append(["lana grossa", "coton"])
search_list.append(["drops", "saafraan"])

create_data()
