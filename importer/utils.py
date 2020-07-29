import configparser
from pymongo import MongoClient
from pymongo.collection import Collection


def config() -> dict:
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    return cfg


def mongo_collection(collection: str) -> Collection:
    cfg = config()
    if 'mongodb' in cfg.sections():
        host = cfg.has_option('mongodb', 'host') and cfg.get('mongodb', 'host') or 'localhost'
        port = cfg.has_option('mongodb', 'port') and cfg.getint('mongodb', 'port') or 27017
    else:
        host = 'localhost'
        port = 27017
    mongo = MongoClient(host=host, port=port)
    return mongo.hotfhir[collection]