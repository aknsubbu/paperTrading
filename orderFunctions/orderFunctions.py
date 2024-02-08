import os
import pymongo
from dotenv import load_dotenv
from datetime import datetime
from portfolioFunctions.portfolioFunctions import Portfolio

class Order:
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
        self.collection = db.get_collection('orders')

        #portfolio connection
        self.portfolio = Portfolio(self.user_id)

    
    def get_orders(self):
        return self.collection.find({'user_id': self.user_id})
    
    def new_order(self,order_id, symbol, quantity, price, type,status,takeProfit:int=None,stopLoss:int=None):

        order_data = {
            'order_id': order_id,
            'user_id': self.user_id,
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'type': type,
            'created_at': datetime.utcnow().isoformat() + 'Z',
            'updated_at': None,
            'status': status,
            'takeProfit': takeProfit,
            'stopLoss': stopLoss

        }

        if type == 'buy':
            self.portfolio.add_stock(symbol, quantity, price, order_data['created_at'])
        
        elif type == 'sell':
            self.portfolio.update_stock(symbol, quantity, price, order_data['created_at'])
    

        self.collection.insert_one(order_data)
        return self.collection.find_one({'order_id': order_id})
    
    def update_order(self, order_id, status):
        order = self.collection.find_one({'order_id': order_id})
        if order:
            order_data = {
                'status': status,
                'updated_at': datetime.utcnow().isoformat() + 'Z'
            }
            self.collection.update_one({'order_id': order_id}, {'$set': order_data})
            return self.collection.find_one({'order_id': order_id})
        return None




 