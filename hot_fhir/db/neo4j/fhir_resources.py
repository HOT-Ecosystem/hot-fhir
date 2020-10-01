from fhirclient.models.codesystem import CodeSystem
from fhirclient.models.conceptmap import ConceptMap
from fhirclient.models.valueset import ValueSet
from fhirclient.models.backboneelement import BackboneElement
from py2neo import Node


def node_to_value_set(node: Node) -> ValueSet:
    value_set = ValueSet()
    for key in node:
        value_set.__setattr__(key, node[key])
    return value_set


def node_to_concept(node: Node) -> BackboneElement:
    concept = BackboneElement()
    return concept


def node_to_code_system(node: Node) -> CodeSystem:
    pass


def node_to_concept_map(node: Node) -> ConceptMap:
    concept_map = ConceptMap()
    return concept_map


def node_to_concept_map_group(node: Node) -> BackboneElement:
    group = BackboneElement()
    return group


def add_conept(concept: BackboneElement) -> None:
    pass


def add_code_system(code_system: CodeSystem) -> None:
    concept: BackboneElement
    for concept in code_system.concept:
        add_conept(concept)
    





