from fhirbase import FHIRBase
from fhirclient.models.valueset import ValueSet
from py2neo import Graph, NodeMatcher

from hot_fhir.db.hot_fhir_store import HotFhirStore
import pytest


@pytest.fixture
def hot_fhir_store(neo4j_graph: Graph, fhirbase: FHIRBase):
    yield HotFhirStore(neo4j_graph, fhirbase)


def test_add_value_set(value_set_example: ValueSet, hot_fhir_store: HotFhirStore, neo4j_graph: Graph, fhirbase: FHIRBase):
    hot_fhir_store.add_value_set(value_set_example)
    node = NodeMatcher(neo4j_graph).match('ValueSet', id=value_set_example.id).first()
    assert node is not None
    assert node['name'] == value_set_example.name
    record: dict = fhirbase.read('ValueSet', value_set_example.id)
    assert record is not None
    assert record['name'] == value_set_example.name
