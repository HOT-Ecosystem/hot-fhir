from hot_fhir.db.fhirbase.operations import *


def test_add_value_set_to_fhirbase(value_set_example: ValueSet, fhirbase: FHIRBase):
    row: dict = add_value_set_to_fhirbase(value_set_example, fhirbase)
    assert row is not None
    assert row['id'] == value_set_example.id

    record: dict = fhirbase.read('ValueSet', value_set_example.id)
    assert record is not None

    n = len(list(fhirbase.list('SELECT * FROM valueset')))
    assert n == 1

    fhirbase.delete('ValueSet', value_set_example.id)


def test_delete_value_set(value_set_example: ValueSet, fhirbase: FHIRBase):
    add_value_set_to_fhirbase(value_set_example, fhirbase)
    n = len(list(fhirbase.list('SELECT * FROM valueset')))
    assert n == 1

    row = delete_value_set_from_fhirbase(value_set_example, fhirbase)
    assert row is not None
    assert row['id'] == value_set_example.id
    n = len(list(fhirbase.list('SELECT * FROM valueset')))
    assert n == 0
