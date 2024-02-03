import pymongo
from dotenv import load_dotenv
import os
from datetime import datetime

class Portfolio:
    def __init__(self, user_id):
        self.user_id = user_id
        load_dotenv()

        uri = os.getenv('MONGO_URI')
        
        client = pymongo.MongoClient(uri, ssl=True)
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        db = client.get_database('papertrading')
        self.collection = db.get_collection('portfolio')

    def get_portfolio(self):
        #get the stocks and return only stocks where sold? is False
        return self.collection.find({'user_id': self.user_id}, {'stocks': {'$elemMatch': {'sold?': False}}})

    def add_stock(self, symbol, quantity, avg_price, created_at):

        # check if stock already exists
        stock = self.collection.find_one({'user_id': self.user_id, 'stocks.symbol': symbol})

        #if stock is there we have to add the quantity and update the avg_price
        if stock:
            stock_data = {
                'symbol': symbol,
                'quantity': stock['quantity'] + quantity,
                'avg_price': (stock['avg_price'] + avg_price) / 2,
                'created_at': stock['created_at'],
                'updated_at': None,
                'delete_at': None,
                'sold?': False
            }
            self.collection.update_one({'user_id': self.user_id, 'stocks.symbol': symbol}, {'$set': {'stocks.$': stock_data}})
            return self.collection.find_one({'user_id': self.user_id})
        #if stock is not there we have to add the stock

        stock_data = {
            'symbol': symbol,
            'quantity': quantity,
            'avg_price': avg_price,
            'created_at': created_at,
            'updated_at': None,
            'delete_at': None,
            'sold?': False
        }
        self.collection.update_one({'user_id': self.user_id}, {'$push': {'stocks': stock_data}})
        return self.collection.find_one({'user_id': self.user_id})

    def remove_stock(self, symbol):
        now = datetime.utcnow().isoformat()
        update_data = {'$set': {'stocks.$.delete_at': now, 'stocks.$.sold?': True}}
        self.collection.update_one({'user_id': self.user_id, 'stocks.symbol': symbol, 'stocks.sold?':False}, update_data)
        return self.collection.find_one({'user_id': self.user_id})

    def update_stock(self, symbol, quantity, avg_price, updated_at):
        query = {'user_id': self.user_id, 'stocks.symbol': symbol , 'stocks.sold?': False}
        update_data = {'$set': {'stocks.$.quantity': quantity, 'stocks.$.avg_price': avg_price, 'stocks.$.updated_at': updated_at}}
        self.collection.update_one(query, update_data)
        return self.collection.find_one({'user_id': self.user_id})

    def get_stock(self, symbol):
        return self.collection.find_one({'user_id': self.user_id, 'stocks.symbol': symbol, 'stocks.sold?':False}, {'stocks.$': 1})



portfolio=Portfolio('user_003')
print(portfolio.get_portfolio())
print('\n\n\n')
print(portfolio.add_stock('AAPL', 10, 100, '2021-05-01'))
print('\n\n\n')
print(portfolio.add_stock('GOOGL', 5, 200, '2021-05-01'))
print('\n\n\n')
print(portfolio.add_stock('AMZN', 15, 300, '2021-05-01'))
print('\n\n\n')
print(portfolio.remove_stock('AAPL'))
print('\n\n\n')
print(portfolio.update_stock('GOOGL', 10, 250, '2021-05-02'))
print('\n\n\n')
print(portfolio.get_stock('GOOGL'))
print('\n\n\n')
print(portfolio.get_portfolio())

