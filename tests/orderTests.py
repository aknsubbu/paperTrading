import unittest
from unittest.mock import patch, MagicMock
from ..orderFunctions.orderFunctions import Order

class TestOrder(unittest.TestCase):
    @patch('pymongo.MongoClient')
    @patch('orderFunctions.load_dotenv')
    def setUp(self, mock_load_dotenv, mock_mongo_client):
        self.mock_db = MagicMock()
        mock_mongo_client.return_value.get_database.return_value = self.mock_db
        self.order = Order('test_user')

    def test_get_orders(self):
        self.order.get_orders()
        self.mock_db.get_collection.assert_called_with('orders')
        self.mock_db.get_collection.return_value.find.assert_called_with({'user_id': 'test_user'})

    def test_new_order(self):
        self.order.new_order('order1', 'AAPL', 10, 150, 'buy', 'open')
        self.mock_db.get_collection.assert_called_with('orders')
        self.mock_db.get_collection.return_value.insert_one.assert_called()

    def test_update_order(self):
        self.order.update_order('order1', 'closed')
        self.mock_db.get_collection.assert_called_with('orders')
        self.mock_db.get_collection.return_value.find_one.assert_called_with({'order_id': 'order1'})
        self.mock_db.get_collection.return_value.update_one.assert_called()

if __name__ == '__main__':
    unittest.main()