from neo4j.graph import Node
from fhirclient.models.namingsystem import NamingSystem
from fhirclient.models.resource import Resource
from hot_fhir.data.neo4j.neo4j_data_engine import node_to_fhir_resource, Neo4jDataEngine
import pytest
from neotime import Date


@pytest.fixture(scope='function')
def node(neo4j_server) -> Node:
    data = {
        'identifier': '_ncit',
        'name': '_NCI Thesaurus',
        'publisher': 'National Cancer Institute (NCI)',
        'kind': 'codesystem',
        'preferred_prefix': '_ncit',
        'status': 'active',
        'date': Date(year=2020, month=8, day=1).iso_format()
    }
    with neo4j_server.driver.session() as session:
        session.write_transaction(neo4j_server.create_naming_system, data)
        n = session.read_transaction(neo4j_server.match_by_identifier, '_ncit', 'NamingSystem')
        yield n
        session.write_transaction(neo4j_server.delete_by_identifier, '_ncit', 'NamingSystem')


def test_node_to_fhir_resource(node):
    r: Resource = node_to_fhir_resource(node)
    assert type(r) is NamingSystem
    assert r.as_json() is not None


def test_invalid_node_to_fhir_resource(node):
    res = node_to_fhir_resource(node)
    assert type(res) is NamingSystem
    assert getattr(res, 'name') == '_NCI Thesaurus'


def test_get_fhir_resource_by_identifier(data_engine, node):
    res = data_engine.get_fhir_resource_by_identifier('NamingSystem', '_ncit')
    print(res)
    assert type(res) is NamingSystem
    assert getattr(res, 'name') == '_NCI Thesaurus'
    assert len(getattr(res, 'extension')) == 1
