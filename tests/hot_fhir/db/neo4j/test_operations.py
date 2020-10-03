from hot_fhir.db.neo4j.operations import *
import pytest
from py2neo import Node


@pytest.fixture(autouse=True)
def neo4j_transact(neo4j_graph):
    neo4j_graph.delete_all()
    yield
    neo4j_graph.delete_all()


@pytest.fixture(scope='function')
def value_set_node(neo4j_graph, value_set_example) -> Node:
    node = value_set_to_node(value_set_example)
    tx = neo4j_graph.begin()
    tx.create(node)
    tx.commit()
    yield node


def test_add_value_set_to_graph(neo4j_graph, value_set_example):
    # Add a value set
    node: Node = add_value_set_to_graph(value_set_example, neo4j_graph)
    assert node is not None
    assert node['name'] == value_set_example.name

    # Find the value set
    node = NodeMatcher(neo4j_graph).match('ValueSet', id=value_set_example.id).first()
    assert node is not None
    assert node['name'] == value_set_example.name


def test_delete_value_set(neo4j_graph, value_set_example):
    add_value_set_to_graph(value_set_example, neo4j_graph)
    nodes = NodeMatcher(neo4j_graph).match('ValueSet', id=value_set_example.id)
    assert len(nodes) == 1

    delete_value_set_from_graph(value_set_example, neo4j_graph)
    node = NodeMatcher(neo4j_graph).match('ValueSet', id=value_set_example.id).first()
    assert node is None


def test_value_set(value_set_node):
    assert value_set_node.identity is not None


def test_node_to_value_set(neo4j_graph):
    node = Node("ValueSet",
                name="LOINC Codes for Cholesterol in Serum/Plasma",
                experimental=True,
                contact=[{
                    "name": "FHIR project team",
                    "telecom": [
                        {
                            "system": "url",
                            "value": "http://hl7.org/fhir"
                        }
                    ]
                }])
    value_set = node_to_value_set(node)
    assert value_set.name == 'LOINC Codes for Cholesterol in Serum/Plasma'

