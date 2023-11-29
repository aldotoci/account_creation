from pymongo import MongoClient
db = MongoClient('mongodb+srv://adminuser:1z61K4f0YDHvdduU@cluster0.3yv1h.mongodb.net/?retryWrites=true&w=majority').users


OFACCCollection = db.ofigaccs
