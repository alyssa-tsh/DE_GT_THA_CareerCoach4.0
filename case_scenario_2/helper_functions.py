import pandas as pd
import re
from fuzzywuzzy import process
import requests
from run_data_loader import fetch_real_time_data, fetch_carpark_data

def merge_data(df, carpark_no):
    info_details_dict = fetch_real_time_data().get(carpark_no)
    carpark_details_dict = fetch_carpark_data(df)
   
    merged_dict = {
        'carpark_no': carpark_no,
        **carpark_details_dict,
        'availability' : info_details_dict
    }
    
    return merged_dict



def standardize_address_for_search(address):
    """
    Standardizes the address to make it easier to compare.
    It handles ranges (e.g., 514-519) and ignores extra spaces and commas.
    
    Parameters:
    address (str): The input address string.
    
    Returns:
    str: The standardized address for comparison.
    """
    # Remove any trailing spaces and commas, and normalize the range
    address = address.strip().replace(", ", " ")  # Remove trailing spaces for commas
    address = re.sub(r'(\d+)([A-Za-z]+)-(\d+)([A-Za-z]+)', r'\1-\3\4', address)  # Normalize ranges like 514A-519A
    address = address.replace(" ", "")  # Remove spaces for easier matching
    return address

def extract_town_block(address):
    """
    Extracts the block number and town from an address string.
    
    Parameters:
    address (str): The input address in the format "BLK <block_number> <town_name>".

    Returns:
    tuple: (block_number, town_name) where block_number is a string and town_name is the remaining part of the address.
    """
    match = re.match(r'BLK\s+(\S+)\s+(.+)', address, re.IGNORECASE)
    if match:
        block_number = match.group(1)  # Extracts the block number
        town_street = match.group(2)  # Extracts the remaining town name
        return town_street, block_number
    return None, None  # Return None if the format is incorrect


def filter_address_by_input(df, user_input):
    """
    Filters the DataFrame based on the user input and the address naming convention.
    
    Parameters:
    df (DataFrame): The dataframe containing the carpark data.
    user_input (str): The user input address or address part.
    
    Returns:
    DataFrame: A filtered dataframe containing rows that match the user input.
    """
    # Standardize user input for comparison
    standardized_input = standardize_address_for_search(user_input)

    # Filter the DataFrame based on the standardized user input
    filtered_df = df[df['address'].str.replace(" ", "").str.contains(standardized_input, case=False, na=False)]
    return filtered_df 
        
    
def display_carpark_info(merged_dict, carpark_no):
    # Check if the carpark number exists in the merged dictionary
    if carpark_no not in merged_dict:
        print(f"No information found for carpark number: {carpark_no}")
        return

    # Extract carpark details
    carpark_data = merged_dict[carpark_no]
    availability_data = merged_dict['availability']
    print(f"Carpark Information for Carpark: {carpark_no}")
    print()

    # Address and Location Details
    print("1. Address and Location Details:")
    print(f"   {carpark_data.get('address', 'N/A')}")
    print()

    # Parking System Information
    print("2. Parking System Information:")
    print(f"   Carpark Type: {carpark_data.get('car_park_type', 'N/A')} with {carpark_data.get('type_of_parking_system', 'N/A')}") 
    print(f"   Carpark Basement: {'No' if carpark_data.get('car_park_basement') == 'N' else 'YES'}, {carpark_data.get('car_park_decks', 'N/A')} carpark decks")
    print(f"   Gantry Height: {carpark_data.get('gantry_height', 'N/A')}")
    print()

    # Capacity and Availability
    print("3. Capacity and Availability:")
    for lot_type, details in availability_data.items():
        print(f"   Lot Type {lot_type} is {'AVAILABLE' if details.get('is_available', 'N/A') == True else 'UNAVAILABLE'}, {details.get('lots_available')} AVAILABLE slots out of {details.get('total_lots', 'N/A')} TOTAL slots, last updated  {details.get('update_datetime', 'N/A')}")
    print()

    # Operating Hours and Rules
    print("4. Operating Hours and Rules:")
    print(f"   Short Term Parking: {carpark_data.get('short_term_parking', 'N/A')}")
    print(f"   Free Parking: {carpark_data.get('free_parking', 'N/A')}")
    print(f"   Night Parking: {carpark_data.get('night_parking', 'N/A')}")
    print()

    # Coordinates
    print("5. Coordinates:")
    print(f"   X Coordinate: {carpark_data.get('x_coord', 'N/A')}")
    print(f"   Y Coordinate: {carpark_data.get('y_coord', 'N/A')}")



def filter_address_by_block_and_town(df, town, block):
    """
    Filters the DataFrame based on both the block number and the town name together.
    Both the block and town must be present in the address for a match.

    Parameters:
    df (DataFrame): The dataframe containing the carpark data.
    block (str): The block number (e.g., '123'). If None or empty, only filters by town.
    town (str): The town or road name in uppercase.

    Returns:
    DataFrame: A filtered dataframe containing only rows matching both the block and town.
    """
    # Ensure town is not empty
    if not town:
        raise ValueError("Town name cannot be empty.")

    
    block_number = None
    block_number = block.strip() if block and block.strip() else None

    # Filter by town (case-insensitive)
    filtered_df = df[df['address'].str.contains(town, case=False, na=False)]
    
    if filtered_df.empty:
        print("Town or road name does not exist or checking spelling")

    # If block is provided and valid, filter by block or block range
    if block_number is not None:
        def block_matches(address):
            # Check if block is explicitly in the address
            if re.search(rf'\b{block_number}\b', address, re.IGNORECASE):
                return True

            # Check if block falls within a detected block range
            block_range = extract_block_range(address)
            if block_range:
                start_block, end_block = block_range
                block_numeric = int(''.join(filter(str.isdigit, block_number)))
                return start_block <= block_numeric <= end_block

            return False

        # Apply the block matching function
        filtered_df = filtered_df[filtered_df['address'].apply(block_matches)]
        
    if filtered_df.empty:
        print("Invalid block number, RESTART search")
        #return an empty data frame
        return pd.DataFrame()

    return filtered_df


def extract_block_range(address):
    """
    Extracts the block numbers from an address containing a block range like '781-783' or '781 - 783',
    even if there are slight variations in spacing or dashes.

    Parameters:
    address (str): The input address string.

    Returns:
    tuple: A tuple with the start and end block numbers (as integers), or None if no range is found.
    """
    # Standardize the format using fuzzy matching
    standardized_address = process.extractOne(address, [re.sub(r'\s*-\s*', '-', address)])[0]
    
    # Regular expression to match block number ranges
    match = re.search(r'(\d+)-(\d+)', standardized_address)
    
    if match:
        start_block = int(match.group(1))
        end_block = int(match.group(2))
        return start_block, end_block
    return None
    


