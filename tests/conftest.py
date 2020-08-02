import pytest
from fhirclient.models.codesystem import CodeSystem
from flask import Flask
from flask_on_fhir import FHIR, DataEngine
import configparser
from hot_fhir.data.neo4j import Neo4jModels, Neo4jDataEngine
import requests
from requests.exceptions import ConnectionError


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture
def app():
    app = Flask(__name__)
    return app


@pytest.fixture(scope="session")
def neo4j(docker_ip, docker_services):
    """ Ensure neo4j is up and responsive"""
    port = docker_services.port_for("fhir-neo4j", 7474)
    url = f'http://{docker_ip}:{port}'
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    bolt_port = docker_services.port_for('fhir-neo4j', 7687)
    bolt_url = f'bolt://{docker_ip}:{bolt_port}'
    neo4j = Neo4jModels(bolt_url, 'neo4j', 'password')
    yield neo4j
    neo4j.close()


@pytest.fixture(scope="session")
def data_engine(neo4j) -> Neo4jDataEngine:
    engine = Neo4jDataEngine(neo4j)
    yield engine
    engine.close()


@pytest.fixture
def fhir(app, data_engine):
    fhir = FHIR(app, data_engine)
    return fhir
