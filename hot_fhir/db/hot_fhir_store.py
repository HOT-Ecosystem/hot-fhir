from fhirbase import FHIRBase
from py2neo import Graph
from hot_fhir.db.neo4j.operations import *
from hot_fhir.db.fhirbase.operations import *


class HotFhirStore:
    def __init__(self, graph: Graph, fhirbase: FHIRBase):
        self.fhirbase = fhirbase
        self.graph = graph

    def add_value_set(self, value_set: ValueSet):
        if add_value_set_to_graph(value_set, self.graph) and add_value_set_to_fhirbase(value_set, self.fhirbase):
            return True
        else:
            return False

    def delete_value_set(self, value_set: ValueSet):
        if delete_value_set_from_graph(value_set, self.graph) and delete_value_set_from_fhirbase(value_set, self.fhirbase):
            return True
        else:
            return False

