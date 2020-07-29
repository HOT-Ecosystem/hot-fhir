import configparser
from pymongo import MongoClient
from pymongo.collection import Collection
from hot_fhir.neo4j_models import Neo4jModels


def config() -> dict:
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    return cfg


def mongo_collection(collection: str) -> Collection:
    cfg = config()
    host = cfg.get('mongodb', 'host', fallback='localhost')
    port = cfg.getint('mongodb', 'port', fallback=27017)
    mongo = MongoClient(host=host, port=port)
    return mongo.hotfhir[collection]


def neo4j_models() -> Neo4jModels:
    cfg = config()
    uri = cfg.get('neo4j', 'uri', fallback='bolt://localhost:7687')
    user = cfg.get('neo4j', 'user', fallback='neo4j')
    password = cfg.get('neo4j', 'password', fallback='neo4j')
    return Neo4jModels(uri, user, password)
