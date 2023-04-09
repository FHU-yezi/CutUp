from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from utils.config import config


def init_db(db_name: str) -> Database:
    connection: MongoClient = MongoClient(config.db.host, config.db.port)
    return connection[db_name]


db = init_db(config.db.main_database)


def get_collection(collection_name: str) -> Collection:
    return db[collection_name]


run_log_db = db.run_log
