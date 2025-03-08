import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import requests
from helper_functions import read_json, get_restaurant_list, get_restaurant_details, get_events_list, save_to_csv, get_user_ratings_df, get_rating_thresholds

class TestFunctions(unittest.TestCase):
    
    # Test for read_json function
    @patch('requests.get')
    def test_read_json_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        result = read_json('http://dummyurl.com')
        self.assertEqual(result, {"key": "value"})
    
    @patch('requests.get')
    def test_read_json_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = read_json('http://dummyurl.com')
        self.assertEqual(result, [])
    
    # Test for get_restaurant_list function
    @patch('helper_functions.read_json')
    def test_get_restaurant_list(self, mock_read_json):
        mock_data = [
            {
                "restaurants": [
                    {
                        "restaurant": {
                            "R": {"res_id": "A20"},
                            "name": "Restaurant 1",
                            "location": {"city_id": 1, "city": "City 1"},
                            "user_rating": {"votes": 100, "aggregate_rating": 4.5},
                            "cuisines": "Italian",
                            "zomato_events": [{"event": {"start_date": "2025-03-01"}}]
                        }
                    }
                ]
            }
        ]
        
        mock_read_json.return_value = mock_data
        
        url = 'http://dummyurl.com'
        result = get_restaurant_list(url)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Restaurant Name"], "Restaurant 1")
        self.assertEqual(result[0]["City"], "City 1")
    
    # Test for get_restaurant_details function
    @patch('helper_functions.get_restaurant_list')
    @patch('pandas.read_excel')
    def test_get_restaurant_details(self, mock_read_excel, mock_get_restaurant_list):
        # Mocking data
        mock_restaurant_data = [
            {
                "Restaurant Id": "A20",
                "Restaurant Name": "Restaurant 1",
                "Country Code": 1,
                "City": "City 1",
                "User Rating Votes": 100,
                "User Aggregate Rating": 4.5,
                "Cuisines": "Italian",
                "Event Date": "2025-03-01"
            }
        ]
        mock_get_restaurant_list.return_value = mock_restaurant_data

        # Mock the countries excel file
        mock_country_data = pd.DataFrame({
            'Country Code': [1],
            'Country Name': ["Country 1"]
        })
        mock_read_excel.return_value = mock_country_data
        
        url = 'http://dummyurl.com'
        result_df = get_restaurant_details(url)
        
        self.assertEqual(result_df.shape[0], 1)
        self.assertEqual(result_df['Country Name'].iloc[0], "Country 1")
        self.assertNotIn("Country Code", result_df.columns)
    
    # Test for get_events_list function
    @patch('helper_functions.read_json')
    def test_get_events_list(self, mock_read_json):
        mock_data = [
            {
                "restaurants": [
                    {
                        "restaurant": {
                            "R": {"res_id": "A20"},
                            "name": "Restaurant 1",
                            "photos_url": "http://example.com/photo.jpg",
                            "zomato_events": [
                                {
                                    "event": {
                                        "event_id": "E01",
                                        "title": "Food Festival",
                                        "start_date": "2025-03-01",
                                        "end_date": "2025-03-03"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
        
        mock_read_json.return_value = mock_data
        
        url = 'http://dummyurl.com'
        result = get_events_list(url)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Event Title"], "Food Festival")
    
    # Test for save_to_csv function
    @patch('pandas.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv):
        # Create a simple dataframe
        df = pd.DataFrame({
            'Column1': [1, 2],
            'Column2': ['A', 'B']
        })
        
        mock_to_csv.return_value = None  # Mock the return value of to_csv

        filename = 'test_output.csv'
        save_to_csv(df, filename)

        mock_to_csv.assert_called_once_with(filename, index=False)
    
    # Test for get_user_ratings_df function
    @patch('helper_functions.read_json')
    def test_get_user_ratings_df(self, mock_read_json):
        mock_data = [
            {
                "restaurants": [
                    {
                        "restaurant": {
                            "user_rating": {"aggregate_rating": 4.5, "rating_text": "Excellent"}
                        }
                    }
                ]
            }
        ]
        
        mock_read_json.return_value = mock_data
        
        url = 'http://dummyurl.com'
        result_df = get_user_ratings_df(url)
        
        self.assertEqual(len(result_df), 1)
        self.assertEqual(result_df['user_rating_value'][0], 4.5)
        self.assertEqual(result_df['user_rating_texts'][0], "Excellent")
    
    # Test for get_rating_thresholds function
    @patch('helper_functions.get_user_ratings_df')
    def test_get_rating_thresholds(self, mock_get_user_ratings_df):
        mock_ratings_data = pd.DataFrame({
            "user_rating_value": [2.5, 3.5, 4.0, 4.5, 5.0],
            "user_rating_texts": ["Poor", "Average", "Good", "Very Good", "Excellent"]
        })
        mock_get_user_ratings_df.return_value = mock_ratings_data
        
        url = 'http://dummyurl.com'
        result = get_rating_thresholds(url)
        
        self.assertEqual(result.shape[0], 5)
        self.assertEqual(result.columns.tolist(), ['user_rating_texts', 'min', 'max', 'mean'])

if __name__ == '__main__':
    unittest.main()
