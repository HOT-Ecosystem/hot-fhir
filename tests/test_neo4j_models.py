from hot_fhir.neo4j_models import Neo4jModels
import configparser
import pytest


@pytest.fixture(scope='session')
def config():
    cfg = configparser.ConfigParser()
    cfg.read('test_config.ini')
    return cfg['neo4j']


@pytest.fixture(scope='session')
def neo4j(config):
    neo4j = Neo4jModels(config['uri'], config['user'], config['password'])
    return neo4j


def test_terminology_service(neo4j: Neo4jModels):
    data = {
        'identifier': 'bioportal',
        'name': 'BioPortal',
        'url': 'http://bioportal.bioontology.org/',
        'type': 'ontology',
        'rest_endpoint': 'https://data.bioontology.org',
        'sparql_endpoint': 'http://sparql.bioontology.org',
        'description': 'A short description',
        'storage': 'triple store',
        'publisher': 'National Center for Biomedical Ontology (NCBO)'
    }
    with neo4j.driver.session() as session:
        session.write_transaction(neo4j.create_terminology_service, data)
        ts = session.read_transaction(neo4j.match_label_by_name, 'BioPortal', 'TerminologyService')
        assert len(ts) == 1
        session.write_transaction(neo4j.delete_label_by_identifier, 'bioportal', 'TerminologyService')
        ts = session.read_transaction(neo4j.match_label_by_name, 'BioPortal', 'TerminologyService')
        assert len(ts) == 0


def test_create_terminology_service(neo4j: Neo4jModels):
    data = {
        'identifier': 'test_id',
        'name': 'test'
    }
    with neo4j.driver.session() as session:
        session.write_transaction(neo4j.create_terminology_service, data)
        ts = session.read_transaction(neo4j.match_label_by_name, 'test', 'TerminologyService')
        assert len(ts) == 1
        session.write_transaction(neo4j.delete_label_by_identifier, 'test_id', 'TerminologyService')
        ts = session.read_transaction(neo4j.match_label_by_name, 'test', 'TerminologyService')
        assert len(ts) == 0
