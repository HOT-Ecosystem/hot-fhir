from flask_on_fhir import FHIR
from flask_on_fhir.restful_resources import NamingSystemResource
import pytest
import json
from neotime import Date
from fhirclient.models.namingsystem import NamingSystemUniqueId, NamingSystem


@pytest.fixture
def naming_system_record(neo4j_server):
    """ Insert a naming system record. Clean up after the tests are run """
    data = {
        'identifier': '_ncit',
        'name': '_NCI Thesaurus',
        'publisher': 'National Cancer Institute (NCI)',
        'kind': 'codesystem',
        'status': 'active',
        'date': Date(year=2020, month=8, day=1).iso_format()
    }
    with neo4j_server.driver.session() as session:
        session.write_transaction(neo4j_server.create_naming_system, data)
        n = session.read_transaction(neo4j_server.match_by_identifier, '_ncit', 'NamingSystem')
        yield n
        session.write_transaction(neo4j_server.delete_by_identifier, '_ncit', 'NamingSystem')


def test_naming_system(fhir: FHIR, naming_system_record, client):
    fhir.add_fhir_resource(NamingSystemResource)
    res = client.get('/NamingSystem/_ncit')
    assert res.status_code == 200
    assert res.json['resourceType'] == 'NamingSystem'
    assert res.json['name'] == '_NCI Thesaurus'
    #
    # res = client.get('/NamingSystem')
    # assert res.status_code == 200
    # assert res.json['resourceType'] == 'Bundle'


def test_naming_system_unique_id():
    unique_id_json_str = '{"type": "other", "value": "_ncit"}'
    unique_id = NamingSystemUniqueId(json.loads(unique_id_json_str))
    assert unique_id.type == 'other'
    assert unique_id.value == '_ncit'





