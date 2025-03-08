import requests
import pandas as pd
import requests 


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

#Create a list to store dictionary of event details 
def get_events_list(url):
    data = read_json(url)
    # List comprehension to extract event details
    events_list = [
        {
            "Event Id": event["event"]["event_id"],
            "Restaurant Id": restaurant["R"]["res_id"],
            "Restaurant Name": restaurant["name"],
            "Photo URL": restaurant["photos_url"],
            "Event Title": event["event"]["title"],
            "Event Start Date": event["event"]["start_date"],
            "Event End Date": event["event"]["end_date"]
        }
        for item in data
        for restaurant in (d["restaurant"] for d in item.get("restaurants", []))
        for event in restaurant.get("zomato_events", [])
    ]

    print(f"Extracted details for {len(events_list)} events")
    return events_list

