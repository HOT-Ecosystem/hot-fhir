from neo4j.graph import Node
from fhirclient.models.namingsystem import NamingSystem
from hot_fhir.data.neo4j.neo4j_data_engine import node_to_fhir_resource
from .test_neo4j_models import config, neo4j
import pytest


@pytest.fixture(scope='function')
def node(neo4j) -> Node:
    data = {
        'identifier': '_ncit',
        'name': '_NCI Thesaurus',
        'publisher': 'National Cancer Institute (NCI)',
        'kind': 'codesystem'
    }
    with neo4j.driver.session() as session:
        session.write_transaction(neo4j.create_naming_system, data)
        n = session.read_transaction(neo4j.match_label_by_identifier, '_ncit', 'NamingSystem')
        yield n
        session.write_transaction(neo4j.delete_label_by_identifier, '_ncit', 'NamingSystem')


def test_node_to_fhir_resource(node):
    r = node_to_fhir_resource(node)
    assert type(r) is NamingSystem
