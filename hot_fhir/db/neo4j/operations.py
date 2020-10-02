from fhirclient.models.codesystem import CodeSystem
from fhirclient.models.conceptmap import ConceptMap
from fhirclient.models.valueset import ValueSet
from fhirclient.models.backboneelement import BackboneElement
from py2neo import Node, Graph, NodeMatcher


def add_node_to_graph(node: Node, graph: Graph) -> bool:
    try:
        tx = graph.begin()
        tx.create(node)
        return tx.commit()
    except TypeError:
        return None


def delete_node_by_id(node_id: str, graph: Graph) -> bool:
    tx = graph.begin()
    node = NodeMatcher(graph).get(node_id)
    tx.delete(node)
    tx.commit()


def add_value_set_to_graph(value_set: ValueSet, graph: Graph) -> Node:
    node: Node = value_set_to_node(value_set)
    if add_node_to_graph(node, graph):
        return node
    else:
        return None


def delete_value_set(value_set: ValueSet, graph: Graph) -> bool:
    nodes = NodeMatcher(graph)
    node = nodes.match('ValueSet', id=value_set.id).first()
    tx = graph.begin()
    tx.delete(node)
    tx.commit()


def add_code_system_to_graph(code_system: CodeSystem, graph: Graph) -> bool:
    pass


def node_to_value_set(node: Node) -> ValueSet:
    value_set = ValueSet()
    for key in node:
        value_set.__setattr__(key, node[key])
    return value_set


def value_set_to_node(value_set: ValueSet) -> Node:
    node = Node("ValueSet", id=value_set.id, version=value_set.version, name=value_set.name)
    return node


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
    





