import configparser
from hot_fhir import neo4j_models
from pymongo import MongoClient
import requests


def config():
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    return cfg


def import_ols():
    cfg = config()
    neo4j_config = cfg['neo4j']
    neo4j = neo4j_models.Neo4jModels(neo4j_config['uri'], neo4j_config['user'], neo4j_config['password'])

    mongo_config = cfg['mongodb']
    mongo = MongoClient(mongo_config['host'], int(mongo_config['port']))
    mongo_db = mongo.hotfhir
    collection = mongo_db.ols

    url = "http://www.ebi.ac.uk/ols/api/ontologies"

    payload = {}
    headers = {}
    ontos = []
    while url is not None:
        response = requests.request("GET", url, headers=headers, data=payload)
        res_json = response.json()
        ontos.extend(res_json['_embedded']['ontologies'])
        url = res_json['_links'].get('next', {}).get('href')

    for onto in ontos:
        collection.insert_one(onto)


if __name__ == '__main__':
    import_ols()
