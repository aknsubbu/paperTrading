import os
import pymongo
from dotenv import load_dotenv
from datetime import datetime

class WatchList:
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
        self.collection = db.get_collection('watchlist')

    def create_watchlist(self):
        # Check if watchlist already exists
        watchlist = self.collection.find_one({'user_id': self.user_id})
        if watchlist:
            print("Watchlist already exists")
            return watchlist
        

        watchlist = {
            'user_id': self.user_id,
            'symbols': [],
            'created_at': datetime.utcnow().isoformat() + 'Z'
        }
        self.collection.insert_one(watchlist)
        return self.collection.find_one({'user_id': self.user_id})
    
    def add_symbols(self, symbols):
        watchlist_items = [
            {"symbol": symbol, "created_at": datetime.utcnow().isoformat() + "Z"} 
            for symbol in symbols
        ]
        query = {'user_id': self.user_id}
        update_data = {'$push': {'symbols': {'$each': watchlist_items}}}
        self.collection.update_one(query, update_data, upsert=True)
        return self.collection.find_one({'user_id': self.user_id})

    def read_symbols(self):
        watchlist = self.collection.find_one({'user_id': self.user_id}, {'symbols': 1})
        if watchlist:
            return watchlist['symbols']
        else:
            return []

    def delete_symbol(self, symbol):
        query = {'user_id': self.user_id}
        update_data = {'$pull': {'symbols': {'symbol': symbol}}}
        self.collection.update_one(query, update_data)
        return self.collection.find_one({'user_id': self.user_id})

# Example usage
watchlist = WatchList('user_000')
# print(watchlist.create_watchlist())
# print(watchlist.add_symbols(['AAPL', 'GOOGL']))
print(watchlist.read_symbols())
# print(watchlist.delete_symbol('AAPL'))
# print(watchlist.read_symbols())
