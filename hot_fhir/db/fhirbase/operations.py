from fhirclient.models.codesystem import CodeSystem
from fhirclient.models.valueset import ValueSet
from fhirbase import FHIRBase


def add_value_set_to_fhirbase(value_set: ValueSet, fhirbase: FHIRBase) -> dict:
    row = fhirbase.create(value_set.as_json())
    return row


def delete_value_set_from_fhirbase(value_set: ValueSet, fhirbase: FHIRBase) -> dict:
    row = fhirbase.delete('ValueSet', value_set.id)
    return row


def add_code_system_to_fhirbase(code_system: CodeSystem) -> bool:
    pass


def find_value_set(field, name) -> ValueSet:
    value_set
