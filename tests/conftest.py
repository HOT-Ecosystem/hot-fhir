import pytest
from fhirclient.models.codesystem import CodeSystem
from flask import Flask
import configparser
import requests
from requests.exceptions import ConnectionError
from py2neo import Graph


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


@pytest.fixture(scope='session')
def neo4j_graph(docker_ip, docker_services):
    port = docker_services.port_for('fhir-neo4j', 7474)
    url = f'http://{docker_ip}:{port}'
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda : is_responsive(url)
    )
    bolt_port = docker_services.port_for('fhir-neo4j', 7687)
    bolt_url = f'bolt://{docker_ip}:{bolt_port}'
    graph = Graph(bolt_url, auth=('neo4j', 'password'))
    yield graph

