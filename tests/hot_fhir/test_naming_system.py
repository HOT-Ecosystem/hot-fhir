from flask_on_fhir import FHIR
from flask_on_fhir.restful_resources import NamingSystemResource


def test_nameing_system(fhir: FHIR):
    fhir.add_fhir_resource(NamingSystemResource)
    # Insert a record
    # Test retrieving the record
    # Test retrieving the bundle
    # delete the record
