import pytest
from fhirclient.models.codesystem import CodeSystem
from flask import Flask
from flask_on_fhir import FHIR, DataEngine
import configparser
from hot_fhir.data.neo4j import Neo4jModels, Neo4jDataEngine


@pytest.fixture
def app():
    app = Flask(__name__)
    return app


@pytest.fixture
def config():
    cfg = configparser.ConfigParser()
    cfg.read('test_config.ini')
    return cfg['neo4j']


@pytest.fixture
def neo4j(config):
    neo4j = Neo4jModels(config['uri'], config['user'], config['password'])
    yield neo4j
    neo4j.close()


@pytest.fixture
def data_engine(neo4j) -> Neo4jDataEngine:
    engine = Neo4jDataEngine(neo4j)
    yield engine
    engine.close()


@pytest.fixture
def fhir(app, data_engine):
    fhir = FHIR(app, data_engine)
    return fhir
