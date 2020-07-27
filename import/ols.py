import configparser
import neo4j_models
import requests


def config():
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    return cfg


def import_bioportal():
    cfg = config()
    neo4j_config = cfg['neo4j']
    neo4j = neo4j_models.Neo4jModels(neo4j_config['uri'], neo4j_config['user'], neo4j_config['password'])

    import requests

    url = "http://www.ebi.ac.uk/ols/api/ontologies"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text.encode('utf8'))


if __name__ == '__main__':
    import_bioportal()
