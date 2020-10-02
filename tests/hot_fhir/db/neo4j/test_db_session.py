from hot_fhir.db.neo4j.db_session import db_auth


def test_db_auth():
    graph = db_auth()
    assert graph is not None
