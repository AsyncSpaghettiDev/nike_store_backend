import pymongo
import certifi

con_str = "mongodb+srv://FSDI:FSDI1234@cluster0.rc1ckie.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database('nike_store')

me = {
    'name': 'Jonathan',
    'last_name': 'Mojica',
    'age': 21,
}


def hello():
    print('Hello there')
