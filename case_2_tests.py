import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import pandas as pd

# Assuming the functions are in a module named `carpark_module`
from run_commands import query_carpark_info_by_number, query_carpark_data, query_last_update_time

class TestCarparkQueries(unittest.TestCase):
    
    # Mocking fetch_real_time_data
    @patch('run_data_loader.fetch_real_time_data')
    def test_query_last_update_time_carpark(self, mock_fetch_real_time_data):
        mock_fetch_real_time_data.return_value = {
            'A20': {'C': {'is_available': True, 'total_lots': '105', 'lots_available': '99', 'update_datetime': '2025-03-08T18:53:12'}},
            'B11': {'C': {'is_available': True, 'total_lots': '150', 'lots_available': '120', 'update_datetime': '2025-03-08T18:55:28'}},
        }

        # Test case 1: Valid carpark number input
        with patch('builtins.input', return_value='A20'):  # Mock user input
            result = query_last_update_time()
            self.assertEqual(result, '2025-03-08T16:00:24')

        # Test case 2: Invalid carpark number input
        with patch('builtins.input', return_value='INVALID'):  # Mock user input
            result = query_last_update_time()
            self.assertEqual(result, 'Carpark number INVALID not found.')
        
        # Test case 3: No carpark number (latest update overall)
        with patch('builtins.input', return_value=''):  # Mock user input for empty input (press Enter)
            result = query_last_update_time()
            self.assertEqual(result, '2025-03-08T16:05:24')  # Latest update time overall

    # Test query_carpark_info_by_number function
    @patch('helper_functions.merge_data')
    @patch('helper_functions.display_carpark_info')
    def test_query_carpark_info_by_number(self, mock_display_carpark_info, mock_merge_data):
        mock_df = pd.DataFrame({'car_park_no': ['A20', 'B12'], 'address': ['BLK 101 TAMPINES STREET 1', 'BLK 202 ANG MO KIO']})
        carpark_no = 'A20'

        # Mock merge and display functions
        mock_merge_data.return_value = mock_df.loc[mock_df['car_park_no'] == carpark_no]
        mock_display_carpark_info.return_value = None

        with patch('builtins.input', return_value=carpark_no):
            result = query_carpark_info_by_number(mock_df)
            self.assertIsNone(result)  # The function should return None after displaying info

    # Test query_carpark_data function
    @patch('helper_functions.filter_address_by_input')
    @patch('helper_functions.filter_address_by_block_and_town')
    @patch('helper_functions.merge_data')
    @patch('helper_functions.display_carpark_info')
    def test_query_carpark_data(self, mock_display_carpark_info, mock_merge_data, mock_filter_address_by_block_and_town, mock_filter_address_by_input):
        mock_df = pd.DataFrame({
            'car_park_no': ['A20', 'B12'],
            'address': ['BLK 101 TAMPINES STREET 1', 'BLK 202 ANG MO KIO']
        })

        # Mock function behavior
        mock_filter_address_by_input.return_value = mock_df[mock_df['address'] == 'BLK 101 TAMPINES STREET 1']
        mock_filter_address_by_block_and_town.return_value = mock_df[mock_df['car_park_no'] == 'A20']
        mock_merge_data.return_value = mock_df[mock_df['car_park_no'] == 'A20']
        mock_display_carpark_info.return_value = None

        with patch('builtins.input', side_effect=['YES', 'BLK 101 TAMPINES STREET 1']):
            query_carpark_data(mock_df)  # Since this will print, we do not need a return value check

    @patch('helper_functions.filter_address_by_input')
    @patch('helper_functions.filter_address_by_block_and_town')
    def test_invalid_address_input(self, mock_filter_address_by_block_and_town, mock_filter_address_by_input):
        mock_df = pd.DataFrame({
            'car_park_no': ['A20', 'B12'],
            'address': ['BLK 101 TAMPINES STREET 1', 'BLK 202 ANG MO KIO']
        })

        # Simulate an invalid address input by the user
        mock_filter_address_by_input.return_value = pd.DataFrame()
        mock_filter_address_by_block_and_town.return_value = pd.DataFrame()

        with patch('builtins.input', side_effect=['YES', 'INVALID ADDRESS']):
            with self.assertLogs(level='INFO') as log:
                query_carpark_data(mock_df)  # This should print "No matches found."
                self.assertIn('No matches found.', log.output[0])

    @patch('helper_functions.filter_address_by_input')
    @patch('helper_functions.filter_address_by_block_and_town')
    def test_no_carparks_found(self, mock_filter_address_by_block_and_town, mock_filter_address_by_input):
        mock_df = pd.DataFrame({'car_park_no': ['A20'], 'address': ['BLK 101 TAMPINES STREET 1']})

        # Mock empty return when no matching carparks
        mock_filter_address_by_input.return_value = pd.DataFrame()
        mock_filter_address_by_block_and_town.return_value = pd.DataFrame()

        with patch('builtins.input', side_effect=['NO', 'TAMPINES', '123']):
            with self.assertLogs(level='INFO') as log:
                query_carpark_data(mock_df)  # Should print "No matches found."
                self.assertIn("No matches found.", log.output[0])


if __name__ == '__main__':
    unittest.main()
