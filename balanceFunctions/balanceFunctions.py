import os
import pymongo
from dotenv import load_dotenv
from datetime import datetime

class Balance:
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
        self.collection = db.get_collection('balance')

    def get_balance(self):
        return self.collection.find_one({'user_id': self.user_id})
    
    def add_balance(self, amount):
        balance = self.collection.find_one({'user_id': self.user_id})
        if balance:
            balance_data = {
                'balance': balance['balance'] + amount,
                'created_at': balance['created_at'],
                'updated_at': datetime.utcnow().isoformat() + 'Z'
            }
            self.collection.update_one({'user_id': self.user_id}, {'$set': balance_data})
            return self.collection.find_one({'user_id': self.user_id})
        balance_data = {
            'user_id': self.user_id,
            'balance': amount,
            'created_at': datetime.utcnow().isoformat() + 'Z',
            'updated_at': None
        }
        self.collection.insert_one(balance_data)
        return self.collection.find_one({'user_id': self.user_id})
    
    def remove_balance(self, amount):
        balance = self.collection.find_one({'user_id': self.user_id})
        if balance:
            balance_data = {
                'balance': balance['balance'] - amount,
                'created_at': balance['created_at'],
                'updated_at': datetime.utcnow().isoformat() + 'Z'
            }
            self.collection.update_one({'user_id': self.user_id}, {'$set': balance_data})
            return self.collection.find_one({'user_id': self.user_id})
        return None
    
    def delete_balance(self):
        self.collection.delete_one({'user_id': self.user_id})
        return self.collection.find_one({'user_id': self.user_id})
    

balance =  Balance('user_001')    
print(balance.get_balance())
print(balance.add_balance(10000))
print(balance.get_balance())
