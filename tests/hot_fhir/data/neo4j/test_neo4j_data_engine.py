from neo4j.graph import Node
from fhirclient.models.namingsystem import NamingSystem
from hot_fhir.data.neo4j.neo4j_data_engine import node_to_fhir_resource, Neo4jDataEngine
from .test_neo4j_models import config, neo4j
import pytest


@pytest.fixture(scope='function')
def node(neo4j) -> Node:
    data = {
        'identifier': '_ncit',
        'name': '_NCI Thesaurus',
        'publisher': 'National Cancer Institute (NCI)',
        'kind': 'codesystem',
        'preferred_prefix': '_ncit',
    }
    with neo4j.driver.session() as session:
        session.write_transaction(neo4j.create_naming_system, data)
        n = session.read_transaction(neo4j.match_by_identifier, '_ncit', 'NamingSystem')
        yield n
        session.write_transaction(neo4j.delete_by_identifier, '_ncit', 'NamingSystem')

@pytest.fixture(scope='session')
def engine(neo4j) -> Neo4jDataEngine:
    engine = Neo4jDataEngine(neo4j)
    yield engine
    engine.close()


def test_node_to_fhir_resource(node):
    r = node_to_fhir_resource(node)
    assert type(r) is NamingSystem


def test_invalid_node_to_fhir_resource(node):
    res = node_to_fhir_resource(node)
    assert type(res) is NamingSystem
    assert getattr(res, 'name') == '_NCI Thesaurus'


def test_get_fhir_resource_by_identifier(engine, node):
    res = engine.get_fhir_resource_by_identifier('NamingSystem', '_ncit')
    print(res)
    assert type(res) is NamingSystem
    assert getattr(res, 'name') == '_NCI Thesaurus'
    assert len(getattr(res, 'extension')) == 2
