import pymongo
from dotenv import load_dotenv
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

class Portfolio:
    def __init__(self, user_id):
        self.user_id = user_id
        load_dotenv()

        uri = os.getenv('MONGO_URI')
        
        client = pymongo.MongoClient(uri, ssl=True)
        try:
            client.admin.command('ping')
            logging.info("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            logging.info(e)

        db = client.get_database('papertrading')
        self.collection = db.get_collection('portfolio')

    def get_portfolio(self):
        logging.info('Getting portfolio for user_id: ' + self.user_id)
        #get the stocks and return only stocks where sold? is False
        return self.collection.find({'user_id': self.user_id}, {'stocks': {'$elemMatch': {'sold?': False}}})

    def add_stock(self, symbol, quantity, avg_price, created_at):
        logging.info('Adding stock to portfolio for user_id: ' + self.user_id)
        # Check if stock already exists
        logging.info('Checking if stock already exists')
        stock = self.collection.find_one({'user_id': self.user_id, 'stocks.symbol': symbol})
        logging.info('Stock found: ' + str(stock))


        # If stock is found, update quantity and average price
        if stock:
            current_quantity = stock.get('quantity', 0)  # Get current quantity or default to 0
            current_avg_price = stock.get('avg_price', 0)  # Get current avg_price or default to 0

            new_quantity = current_quantity + quantity
            new_avg_price = (current_avg_price + avg_price) / 2

            stock_data = {
                'symbol': symbol,
                'quantity': new_quantity,
                'avg_price': new_avg_price,
                'created_at': stock.get('created_at', created_at),
                'updated_at': None,
                'delete_at': None,
                'sold?': False
            }

            self.collection.update_one({'user_id': self.user_id, 'stocks.symbol': symbol},
                                    {'$set': {'stocks.$': stock_data}})
        else:
            logging.info('Stock not found. Adding new stock')
            # If stock is not found, add a new stock
            stock_data = {
                'symbol': symbol,
                'quantity': quantity,
                'avg_price': avg_price,
                'created_at': created_at,
                'updated_at': None,
                'delete_at': None,
                'sold?': False
            }

            self.collection.update_one({'user_id': self.user_id},
                                    {'$push': {'stocks': stock_data}})
            
        logging.info('Stock added to portfolio')
        return self.collection.find_one({'user_id': self.user_id})
    # ! TO BE FIXED
    # def remove_stock(self, symbol, quantity, avg_price, created_at):
    #     # Reduce the number of stocks and delete the stock if the quantity is 0
    #     stock = self.collection.find_one({'user_id': self.user_id, 'stocks.symbol': symbol, 'stocks.sold?': False})
    #     if stock:
    #         current_quantity = stock.get('quantity', 0)
    #         if isinstance(current_quantity, MagicMock):
    #             current_quantity = 0  # Set current_quantity to 0 if it's a MagicMock object
    #         if current_quantity > 0:
    #             if current_quantity - quantity <= 0:
    #                 self.collection.update_one({'user_id': self.user_id}, {'$pull': {'stocks': {'symbol': symbol}}})
    #             else:
    #                 new_quantity = current_quantity - quantity
    #                 self.collection.update_one({'user_id': self.user_id, 'stocks.symbol': symbol}, {'$set': {'stocks.$.quantity': new_quantity}})
    #             logging.info(f"Stock {symbol} removed successfully for user {self.user_id}")
    #         else:
    #             logging.warning(f"No stocks found for symbol {symbol} and user {self.user_id}")
    #     else:
    #         logging.warning(f"No stock found for symbol {symbol} and user {self.user_id}")
    #     return self.collection.find_one({'user_id': self.user_id})



    def update_stock(self, symbol, quantity, avg_price, updated_at):
        logging.info('Updating stock in portfolio for user_id: ' + self.user_id)
        query = {'user_id': self.user_id, 'stocks.symbol': symbol , 'stocks.sold?': False}
        update_data = {'$set': {'stocks.$.quantity': quantity, 'stocks.$.avg_price': avg_price, 'stocks.$.updated_at': updated_at}}
        logging.info('Updating stock')
        self.collection.update_one(query, update_data)
        return self.collection.find_one({'user_id': self.user_id})

    def get_stock(self, symbol):
        logging.info('Getting stock from portfolio for user_id: ' + self.user_id)
        return self.collection.find_one({'user_id': self.user_id, 'stocks.symbol': symbol, 'stocks.sold?':False}, {'stocks.$': 1})



# portfolio=Portfolio('user_003')
# print(portfolio.get_portfolio())
# print('\n\n\n')
# print(portfolio.add_stock('AAPL', 10, 100, '2021-05-01'))
# print('\n\n\n')
# print(portfolio.add_stock('GOOGL', 5, 200, '2021-05-01'))
# print('\n\n\n')
# print(portfolio.add_stock('AMZN', 15, 300, '2021-05-01'))
# print('\n\n\n')
# print(portfolio.remove_stock('AAPL', 5, 100, '2021-05-02'))
# print('\n\n\n')
# print(portfolio.update_stock('GOOGL', 10, 250, '2021-05-02'))
# print('\n\n\n')
# print(portfolio.get_stock('GOOGL'))
# print('\n\n\n')
# print(portfolio.get_portfolio())

