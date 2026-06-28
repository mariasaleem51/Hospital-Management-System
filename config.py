from pymongo import MongoClient

class Config:
    SECRET_KEY = "super_secret_hospital_key_change_this"
    # Connects to local MongoDB, database named 'hospital_db'
    MONGO_URI = "mongodb://localhost:27017/"
    
client = MongoClient(Config.MONGO_URI)
db = client['hospital_db']