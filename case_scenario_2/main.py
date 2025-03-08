from run_commands import query_carpark_data_by_address, query_last_update_time, query_carpark_info_by_number
from run_data_loader import load_carpark_data

api_url = "https://api.data.gov.sg/v1/transport/carpark-availability"



def main():
    print("Welcome to the Carpark Query System!")
    print("This tool allows you to search for carpark details and retrieve real-time updates.")
    
    df = load_carpark_data()

    while True:
        print("\nPlease select an option:")
        print("1. Query by carpark number")
        print("2. Search for carpark details based on address")
        print("3. View the latest update time")
        print("4. EXIT")
        
        choice = input("Enter the number of your choice: ").strip()
        
        if choice == "1":
            query_carpark_info_by_number(df)
            
        elif choice == "2":
            query_carpark_data_by_address(df)
        
        elif choice == "3":
            latest_update = query_last_update_time()
            print(f"\nLatest update time: {latest_update}")

        
        elif choice == "4":
            print("Exiting the system. Have a great day!")
            break
        
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()


