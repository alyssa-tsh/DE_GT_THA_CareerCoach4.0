import pandas as pd
import re
from helper_functions import merge_data, display_carpark_info, filter_address_by_block_and_town, filter_address_by_input, extract_town_block
from run_data_loader import fetch_real_time_data
import datetime

def query_carpark_info_by_number(df):
    """
    Retrieve the details of a carpark by its unique carpark number.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing carpark data.
    

    Returns:
    pandas.Series or None: 
    The first row of the filtered DataFrame if a match is found, or None if no matching carpark number is found.
    """
    carpark_no = input("Please enter the carpark number (e.g. A20): ").strip()

    filtered_df = df[df['car_park_no'] == carpark_no]

    if filtered_df.empty:
        print("No information found for the given car park number.")
        
    merged_data = merge_data(filtered_df, carpark_no)
    display_carpark_info(merged_data, carpark_no)
    print("Successfully generated carpark information")
    return None

def query_carpark_data_by_address(df):
    while True:
        # Step 1: Ask if the user knows the entire address
        answer = input("Do you know the exact entire address? (YES/NO/RESTART/EXIT): ").strip().upper()

        if answer == "EXIT":
            print("Exiting the program. Goodbye!")
            break

        if answer == "RESTART":
            print("Restarting the process...")
            continue

        if answer == "YES":
            # User inputs the full address
            address = input("Please input the address following this convention: BLK NO ROAD NAME/STREET NAME (e.g., BLK 101/109 BUKIT PURMEI ROAD): ").strip().upper()
            
            # Filter dataframe based on address
            filtered_df = filter_address_by_input(df, address)

            if filtered_df.empty:
                town, block = extract_town_block(address)
                if town and block:
                    filtered_df = filter_address_by_block_and_town(df, town, block)
            
            if not filtered_df.empty:
                print(f"The carpark found at this address is \n{filtered_df}")
                carpark_no = filtered_df['car_park_no'].iloc[0]
                merged_data = merge_data(filtered_df, carpark_no)
                display_carpark_info(merged_data, carpark_no)
            else:
                print("No matches found. Please try typing again using the provided convention and check the spelling. SUGGESTED: Input NO to the next prompt this time and type in town followed by block number")

        elif answer == "NO":
            # Step 2: Ask for town or road name first
            town = input("What is the town or road name in full caps (e.g., ANG MO KIO)? ").strip()

            # Ask for block number (single or range)
            block = input("What is the block number (e.g., 123 or 123B)? Input NOT SURE if you do not know: ").strip()

            # If block is "NOT SURE" or empty, set it to None
            if block == "NOT SURE" or not block.strip():
                block = None

            # Filter by town and block
            filtered_df = filter_address_by_block_and_town(df, town, block)
            
            if not filtered_df.empty:
                carpark = filtered_df[['car_park_no', 'address']]
                carpark_no = filtered_df['car_park_no'].iloc[0]
                print(f"Found the following carparks based on your input:\n{carpark}")
                user_input = input(
                    "Is the carpark you are looking any of the following?"
                    "\nIf yes please input 'YES' otherwise, input 'NO' or 'RESTART' to begin search again: "
                ).strip().upper()

                if user_input == "NO":
                    print("My apologies, we do not have information for that.")
                elif user_input == "RESTART":
                    print("Restarting the process...")
                    continue
                elif user_input == "YES" and len(filtered_df) == 1:
                    filtered_df = merge_data(filtered_df, carpark_no)
                    display_carpark_info(filtered_df, carpark_no)
                else:
                    try:
                       query_carpark_info_by_number(filtered_df)
                    except ValueError:
                        print("Invalid carpark_no entered. Restarting...")
                        continue
            else:
                print("No matches found.")
        else:
            print("Invalid input. Please input 'YES', 'NO', 'RESTART', or 'EXIT'.")

def query_last_update_time():
    """
    Returns the latest update time from the entire dataframe if no carpark number is provided.
    If a carpark number is given, it returns the latest update time for that specific carpark.
    
    Parameters:
    df: the main dataframe containing the merged carpark & real-time data.
    
    Returns:
    str: The last update time.
    """
    # Prompt user for carpark number
    carpark_number = input("Please enter the carpark number (or press Enter to get the latest update overall): ").strip()
    real_time_data = fetch_real_time_data()  # Assuming this function fetches the data as expected
    
    # If a carpark number is provided
    if carpark_number:
        # Check if the carpark number exists in the data
        if carpark_number in real_time_data:
            update_datetime = real_time_data[carpark_number]['C']['update_datetime']
            return update_datetime
        else:
            return f"Carpark number {carpark_number} not found."
    
    
    
       
    









