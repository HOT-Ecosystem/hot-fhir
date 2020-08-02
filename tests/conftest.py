import pytest
from fhirclient.models.codesystem import CodeSystem
from flask import Flask
from flask_on_fhir import FHIR, DataEngine
import configparser
from hot_fhir.data.neo4j import Neo4jModels


@pytest.fixture
def app():
    app = Flask(__name__)
    return app


@pytest.fixture
def data_engine():
    class TestDataEngine(DataEngine):
        def get_fhir_resource(self, resource: str, *args, **kwargs):
            if resource == 'CodeSystem':
                cs = CodeSystem()
                cs.name = '_Test Code System'
                cs.id = '_1234'
                cs.status = 'active'
                cs.content = 'not-present'
                return cs
    return TestDataEngine()


@pytest.fixture(scope='session')
def config():
    cfg = configparser.ConfigParser()
    cfg.read('test_config.ini')
    return cfg['neo4j']


@pytest.fixture(scope='session')
def neo4j(config):
    neo4j = Neo4jModels(config['uri'], config['user'], config['password'])
    yield neo4j
    neo4j.close()


@pytest.fixture
def fhir(app, data_engine):
    fhir = FHIR(app, data_engine)
    return fhir
