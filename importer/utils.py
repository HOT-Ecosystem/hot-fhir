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
    if 'mongodb' in cfg.sections():
        host = cfg.has_option('mongodb', 'host') and cfg.get('mongodb', 'host') or 'localhost'
        port = cfg.has_option('mongodb', 'port') and cfg.getint('mongodb', 'port') or 27017
    else:
        host = 'localhost'
        port = 27017
    mongo = MongoClient(host=host, port=port)
    return mongo.hotfhir[collection]


def neo4j_models() -> Neo4jModels:
    cfg = config()
    if 'neo4j' in cfg.sections():
        uri = cfg.has_option('neo4j', 'uri') and cfg.get('neo4j', 'uri') or 'bolt://localhost:7687'
        user = cfg.has_option('neo4j', 'user') and cfg.get('neo4j', 'user') or 'neo4j'
        password = cfg.has_option('neo4j', 'password') and cfg.get('neo4j', 'password') or 'neo4j'
    else:
        uri = 'bolt://localhost:7687'
        user = 'neo4j'
        password = 'neo4j'
    return Neo4jModels(uri, user, password)
