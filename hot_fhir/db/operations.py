from fhirclient.models.codesystem import CodeSystem
from fhirclient.models.conceptmap import ConceptMap
from fhirclient.models.valueset import ValueSet
from hot_fhir.db.neo4j.operations import add_value_set_to_graph
from hot_fhir.db.fhirbase.operations import add_value_set_to_fhirbase




def add_value_set(value_set: ValueSet) -> bool:
    if add_value_set_to_graph(value_set):
        add_value_set_to_fhirbase(value_set)
    pass


def add_code_system(code_system: CodeSystem) -> bool:
    # Add code system to fhirbase
    # add to neo4j
    pass


def add_concept_map(concept_map: ConceptMap) -> bool:
    # add to fhirbase
    # add to neo4j
    pass


def get_value_set():
    pass
