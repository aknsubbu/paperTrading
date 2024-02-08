import unittest
from unittest.mock import patch, MagicMock
from portfolioFunctions import Portfolio

class TestPortfolio(unittest.TestCase):
    @patch('pymongo.MongoClient')
    @patch('portfolioFunctions.load_dotenv')
    def setUp(self, mock_load_dotenv, mock_mongo_client):
        self.mock_db = MagicMock()
        self.mock_collection = MagicMock()
        self.mock_db.get_collection.return_value = self.mock_collection
        mock_mongo_client.return_value = self.mock_db
        self.portfolio = Portfolio('test_user')

    def test_get_portfolio(self):
        # Mock the find method to return dummy data
        dummy_data = [{'symbol': 'AAPL', 'quantity': 10, 'avg_price': 150, 'created_at': '2022-01-01', 'updated_at': None, 'delete_at': None, 'sold?': False}]
        self.mock_collection.find.return_value = dummy_data

        # Call the method
        result = self.portfolio.get_portfolio()

        # Assert the mock method calls
        self.mock_db.get_collection.assert_called_with('portfolio')
        self.mock_collection.find.assert_called_with({'user_id': 'test_user'}, {'stocks': {'$elemMatch': {'sold?': False}}})

        # Assert the result
        self.assertEqual(result, dummy_data)

    def test_add_stock(self):
        # Call the method
        result = self.portfolio.add_stock('AAPL', 10, 150, '2022-01-01')

        # Assert the mock method calls
        self.mock_db.get_collection.assert_called_with('portfolio')
        self.mock_collection.find_one.assert_called()
        self.mock_collection.update_one.assert_called()

        # Assert the result
        self.assertIsNotNone(result)  # Adjust this assertion based on the expected return value

    def test_remove_stock(self):
        # Call the method
        result = self.portfolio.remove_stock('AAPL', 10, 150, '2022-01-01')

        # Assert the mock method calls
        self.mock_db.get_collection.assert_called_with('portfolio')
        self.mock_collection.find_one.assert_called()
        self.mock_collection.update_one.assert_called()

        # Assert the result
        self.assertIsNotNone(result)  # Adjust this assertion based on the expected return value

    def test_update_stock(self):
        # Call the method
        result = self.portfolio.update_stock('AAPL', 10, 150, '2022-01-01')

        # Assert the mock method calls
        self.mock_db.get_collection.assert_called_with('portfolio')
        self.mock_collection.find_one.assert_called()
        self.mock_collection.update_one.assert_called()

        # Assert the result
        self.assertIsNotNone(result)  # Adjust this assertion based on the expected return value

if __name__ == '__main__':
    unittest.main()
