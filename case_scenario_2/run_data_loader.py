import pandas as pd
import requests
import re


#format real time carpark details data into a dataframe 
def fetch_real_time_data():
    url = "https://api.data.gov.sg/v1/transport/carpark-availability"
    response = requests.get(url)
    data = response.json()
    carpark_data = data['items'][0]['carpark_data']
    #[carpark_dict['carpark_number']:  for carpark_dict in carpark_data]
    d1 = {carpark_dict['carpark_number']: 

        {
            d['lot_type'] : 
            {
                'is_available': int(d['lots_available']) > 0, 
                'total_lots': d['total_lots'], 
                'lots_available' : d['lots_available'],
                'update_datetime': carpark_dict['update_datetime']
            }
                
        for d in carpark_dict['carpark_info']
        }
        for carpark_dict in carpark_data}

    return d1


def fetch_carpark_data(df):
    res2 = dict(zip(df.values[:,0], df.values[:, 1:].tolist()))
    res2

    filtered_carpark_data_dict = {k: dict(zip(df.columns[1:], v)) for k, v in res2.items()}
    return filtered_carpark_data_dict
    

def load_carpark_data():
    df_carpark_details = pd.read_csv("../datasets/HDBCarparkInformation.csv")
    return standardize_address(df_carpark_details)


def standardize_address(df):
    """
    Standardizes the address column in a DataFrame.

    This function:
    - Replaces "BLOCK" or "BLKS" with "BLK".
    - Replaces "TO" in numeric ranges with "-".
    - Ensures "TO" in alphanumeric ranges is also replaced with "-".
    - Replaces "&" with "," for multiple block numbers.

    Parameters:
    df (DataFrame): The input DataFrame with an 'address' column.

    Returns:
    DataFrame: A DataFrame with standardized address formatting.
    """
    original_addresses = df['address'].copy()

    # Replace "BLOCK" or "BLKS" with "BLK"
    df['address'] = df['address'].str.replace(r'\b(BLOCK|BLKS)\b', 'BLK', regex=True)

    # Replace "TO" in numeric ranges (e.g., "123 TO 456" → "123-456", "998A TO 998B" → "998A-998B")
    df['address'] = df['address'].str.replace(r'(?<=\d)\sTO\s(?=\d)', '-', regex=True)
    df['address'] = df['address'].str.replace(r'(?<=\w)\sTO\s(?=\w)', '-', regex=True)

    # Replace "&" with "," (e.g., "123 & 124" → "123,124")
    df['address'] = df['address'].str.replace(r'&', ',', regex=True)

    # Count number of changed entries
    changed_entries = (original_addresses != df['address']).sum()
    print(f"Number of entries with address naming conventions changed: {changed_entries}")

    return df


