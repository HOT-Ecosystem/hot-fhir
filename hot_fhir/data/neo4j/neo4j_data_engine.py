from fhirclient.models.namingsystem import NamingSystem
from flask_on_fhir import DataEngine
from flask_on_fhir.restful_resources import FHIRResource

from hot_fhir.data.neo4j import Neo4jModels
from neo4j.graph import Node
from fhirclient.models import *


def node_to_fhir_resource(node: Node) -> FHIRResource:
    label = list(node.labels)[0]
    klass = globals()[label]
    resource: label = klass()
    return resource


class Neo4jDataEngine(DataEngine):
    def __init__(self, url, user, password):
        self.neo4j = Neo4jModels(url, user, password)

    def close(self):
        self.neo4j.close()

    def get_fhir_resource(self, resource: str, *args, **kwargs):
        ...

    def get_naming_system_by_id(self, id: str) -> NamingSystem:
        ns: NamingSystem = NamingSystem()
        with self.neo4j.driver.session() as session:
            node: Node = session.read_transaction(self.neo4j.match_label_by_identifier, id, 'NamingSystem')
        if node is None:
            return None
        ns.name = node.get('name')


