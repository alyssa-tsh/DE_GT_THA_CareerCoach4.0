import pandas as pd
import streamlit as st
from helper_functions import get_rating_thresholds

restaurants_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"


#after obtaining the min & max treshold values for ratings input them into a dictionary
rating_thresholds = {row["user_rating_texts"]: (row["min"], row["max"]) for _, row in get_rating_thresholds(restaurants_url).iterrows()}
#obtain min & max user_rating_aggregate 

print(rating_thresholds)
def classify_rating(rating):
    for category, (low, high) in rating_thresholds.items():
        if low <= rating <= high:
            return category
        elif rating < 2.2:
            return "No user has ever given such a low rating"
        elif rating > 4.9:
            return "No user has ever given such a high rating"
            
    return "Unknown: There is no data containing information on the texts associated with this rating score"



# Streamlit UI
st.title("Restaurant Rating Analyzer") 

rating = st.slider("Select an aggregate rating:", 0.0, 5.0, 3.0, 0.1)
category = classify_rating(rating)

st.write(f"### The rating category is: **{category}**")
