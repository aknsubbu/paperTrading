import pymongo
from dotenv import load_dotenv
import os

load_dotenv()



uri = os.getenv('MONGO_URI')

# Create a new client and connect to the server
client = pymongo.MongoClient(uri, ssl=True,)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# Create a new database
db = client.get_database['papertrading']

# Create a new collection
collection = db.get_collection['users']

