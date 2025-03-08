from helper_functions import save_to_csv, get_month_events, get_events_list
from run_res_func import get_restaurant_details
#generating restaurant_details.csv file
restaurants_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"

restaurants_df = get_restaurant_details(restaurants_url)
print(restaurants_df.head())
print(restaurants_df.info())
save_to_csv(restaurants_df, "restaurant_details.csv")

events_df = get_month_events(get_events_list(restaurants_url), 2019, 4)
print(events_df.head())
print(events_df.info())
save_to_csv(events_df, "event_details.csv")




