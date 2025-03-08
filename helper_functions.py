import requests
import pandas as pd


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

#formats event details into a dataframe and filters for event data within a specified time frame given year & month (as integers) 
def get_month_events(events_list, year = None, month = None):
    if year is not None and month is not None:
        year_month = f"{year}-{month:02d}"
        filtered_events = []
        for event in events_list:
            start_date = event["Event Start Date"]
            end_date = event["Event End Date"]
            # Check if both start and end dates contain the target "YYYY-MM" string
            if start_date.startswith(year_month) and end_date.startswith(year_month):
                filtered_events.append(event)
        print(f"Filtered {len(filtered_events)} events from {year}-{month:02d}")
    else:
        filtered_events = events_list
        print(f"Returning all {len(filtered_events)} events (no filtering applied)")
    
    return pd.DataFrame(filtered_events)

#a function to convert dataframes to csv files 
def save_to_csv(df, filename):
    df.fillna("NA", inplace = True)
    print(f"csv file {filename} saved successfully")
    return df.to_csv(filename, index = False)

#formats user rating details: aggregate ratings & text values into a dataframe
def get_user_ratings_df(url):
    data = read_json(url)
    ratings_list = [
        {
            "user_rating_value" : float(restaurant["user_rating"]["aggregate_rating"]),
            "user_rating_texts" : str(restaurant["user_rating"]["rating_text"])
        }
        #loop through list of restaurant results to obtain the restaurant dictionaries
        for item in data
        for restaurant in (d["restaurant"] for d in item.get("restaurants", []))
    ]
    
    print(f"Extracted details for {len(ratings_list)} events") 
    return pd.DataFrame(ratings_list)

# formats the descriptive statistics (min, max amd mean) aggregate rating values given by users for diff rating texts
def get_rating_thresholds(restaurants_url):
    ratings_df = pd.DataFrame(get_user_ratings_df(restaurants_url))
    
    # Sort categories in the expected order
    rating_order = ["Poor", "Average", "Good", "Very Good", "Excellent"]
    ratings_df["user_rating_texts"] = pd.Categorical(ratings_df["user_rating_texts"], categories=rating_order, ordered=True)

    thresholds = ratings_df.groupby("user_rating_texts")["user_rating_value"].agg(["min", "max", "mean"]).reset_index()
    print(thresholds)

    return thresholds

