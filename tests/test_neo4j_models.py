from ..neo4j_models import Neo4jModels
import configparser
import pytest


@pytest.fixture(scope='session')
def config():
    cfg = configparser.ConfigParser()
    cfg.read('test_config.ini')
    return cfg


def test_create_terminology_service(config):
    neo4j = config['neo4j']
    models = Neo4jModels(neo4j['uri'], neo4j['user'], neo4j['password'])
    print(models)