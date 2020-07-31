from fhirclient.models.namingsystem import NamingSystem
from fhirclient.models.extension import Extension
from flask_on_fhir import DataEngine
from flask_on_fhir.restful_resources import FHIRResource

from hot_fhir.data.neo4j import Neo4jModels
from neo4j.graph import Node
from typing import List, Union
from importlib import import_module


def node_to_fhir_resource(node: Node) -> Union[FHIRResource, None]:
    for label in node.labels:
        try:
            module_path = f'fhirclient.models.{label.lower()}'
            module = import_module(module_path)
            klass = getattr(module, label)
            resource: label = klass(strict=False)
        except ModuleNotFoundError as ex:
            ...
    if resource is None:
        return None
    extensions = []
    for key in node.keys():
        if hasattr(resource, key):
            setattr(resource, key, node.get(key))
        else:
            ext = Extension()
            ext.url = key
            ext.value = node.get(key)
            extensions.append(ext)
    resource.extension = extensions
    return resource


class Neo4jDataEngine(DataEngine):
    def __init__(self, neo4j: Neo4jModels):
        self.neo4j = neo4j

    def close(self):
        if self.neo4j:
            self.neo4j.close()

    def get_fhir_resource(self, resource: str, *args, **kwargs):
        if 'resource_id' in kwargs:
            return self.get_fhir_resource_by_identifier(resource, kwargs['resource_id'], *args, **kwargs)
        else:
            return self.get_fhir_resource_in_bundle(resource, *args, **kwargs)

    def get_fhir_resource_in_bundle(self, resource_type: str, *args, **kwargs):
        with self.neo4j.driver.session() as session:
            node: Node = session.read_transaction(self.neo4j.match_by_identifier, '', resource_type)
        if node is None:
            return None
        return node_to_fhir_resource(node)

    def get_fhir_resource_by_identifier(self, resource_type: str, identifier: str, *args, **kwargs):
        with self.neo4j.driver.session() as session:
            node: Node = session.read_transaction(self.neo4j.match_by_identifier, identifier, resource_type)
        if node is None:
            return None
        return node_to_fhir_resource(node)


