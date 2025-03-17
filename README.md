# DE_GT_THA_CareerCoach4.0
## Project Overview
The main objective of the modules in the repository are to process json data sources into lists/dataframes for ease of comprehension and formatting, they can also be used to merge and process real time data and csv datasets and retrieve information from both sources via command line inputs based on different prompts

## Set Up and Running the Program
Clone the repository into your local machine and just run the main.py file for each case scenario (in case_scenario1 and case_scenario_2) folders. 
Ensure that the datasets folder exists as a sub-folder in the main folder

## Case Scenario 1
1. & 2. Key design:
- The main functions get_restaurant_list and get_event_list process data from the json file provided from dictionaries into list before helper functions are called respectively on them to carry out data manipulation/transformation  and format them into dataframes for conversion into csv tables
3. Analyzer App:
- Change the working directory to the folder case_scenario_1 and Run python -m streamlit run analyzer_app.py to deploy the analyzer app (simple feature comprising of a slider to return the user rating text associated with the aggregate rating) 


## Case Scenario 2
* The program operates via a command-line interface, guiding users through prompts based on their input needs. 
- It assumes users start their search directly with a carpark number or location/address without needing prior knowledge of available carparks. 
* Users can query by carpark number, address, or last update time. 
* Address-based searches work with partial inputs (e.g., just town/road name) and match the closest relevant carparks. Users can view matching carparks before selecting one, and case/spacing errors are ignored.

### User Flow:
1. Start the program → Choose query type: 
- Query by carpark number, address, or view latest update time.
  
2. Query by carpark number → Direct input.
  
3. Query by address → Users can input the entire address (e.g., BLK 136 TECK WHYE LANE → BLK 135-138,141,142,145 TECK WHYE LANE/AVENUE)
- OR just town & block values as well as block values that are within the range in the address will also return relevant addresses
- Reformatted block ranges (e.g., BLK 123 TO 125) ensure accurate matching.
- Flexibility in input → Not case or spacing sensitive
- subsets of addresses (e.g., 616A SENJA ROAD → BLK 611A/613A/615A/616A BUKIT PANJANG RING ROAD/SENJA ROAD) still return correct results.
- Limitations:
Some non-standard address formats 
(e.g., 12 TO 14 DOVER CLOSE EAST won’t match 13 DOVER CLOSE EAST), and alphanumeric blocks recognized if they belong to a range
(i.e no exact match for that value in address).
The system must take in a town name (it cannot filter based on block number only)
If the user types an additional word it will throw an error and it cannot take in multiple inputs only 1

4. Query last updated time 

## If you would like to try out the program here are some test inputs/examples of how to inputs values :D

### Query OPTION 2
- NO --> SENJA ROAD --> 616A 
- NO --> JURONG WEST STREET --> 480
- NO --> MARINE --> 7
- NO --> BUKIT PANJANG --> NOT SURE --> follow prompts and input desired value
- YES --> 6 JALAN MINYAK
- YES --> BLK 981D BUANGKOK
- YES --> DEFU LANE 6
- YES --> BLK 28 JALAN BAHAGIA
- YES --> BLK 111A SAINT MICHAEL BUS TERMINAL
- YES --> BLK 429, 438-441 CHOA CHU KANG AVENUE 4 (DIRECTLY COPY & PASTE AN ENTIRE ENTRY)

## A demo video of how the different features work can also be found in the zip folder in my submission 
