import requests
import pandas as pd
import os

def read_json(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        return []
    return response.json()

#Create a list to store dictionary of restaurants details 
def get_restaurant_list(url):
    data = read_json(url)
    restaurants_list = [
        {
            "Restaurant Id": restaurant["R"]["res_id"],
            "Restaurant Name": restaurant["name"],
            "Country Code": restaurant["location"]["city_id"],
            "City": restaurant["location"]["city"],
            "User Rating Votes": restaurant["user_rating"]["votes"],
            "User Aggregate Rating": float(restaurant["user_rating"]["aggregate_rating"]),
            "Cuisines": restaurant["cuisines"],
            "Event Date": restaurant["zomato_events"][0]["event"]["start_date"] 
            if restaurant.get("zomato_events") else "NA"
        }   
        #loop through list of restaurant results to obtain the restaurant dictionaries
        for item in data
        for restaurant in (d["restaurant"] for d in item.get("restaurants", []))
    ]

    print(f"Extracted details for {len(restaurants_list)} restaurants")   
    return restaurants_list


#fomats the restaurant details into a dataframe containing the county name in the Country Column
def get_restaurant_details(url):
    df_countries = pd.read_excel("datasets/Country-Code.xlsx")
    #convert to a pd dataframe
    df_main = pd.DataFrame(get_restaurant_list(url))
    #merge on countries excel file to obtain country name
    df_main = df_main.merge(df_countries, on = "Country Code", how = "left")
    #drop country code column
    df_main.drop(columns=["Country Code"], inplace = True)
    return df_main