from neo4j import GraphDatabase


class Neo4jModels:
    graph = None

    def __init__(self, uri, user, password):
        self.graph = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.graph.close()

    @classmethod
    def create_terminology_service(cls, tx, **kwargs):
        cql = ("CREATE (:TerminologyService {"
               " identifier: $identifier"
               " url: $url"
               " name: $name"
               " type: $type"
               " description: $description"
               " publisher: $publisher"
               " rest_endpiont: $rest_endpoint"
               " sparql_endpoint: $sparql_endpoint"
               " storage: $storage"
               "})")
        tx.run(cql, kwargs)

    @classmethod
    def match_codesystem_name(cls, tx, val):
        sql = f"MATCH (n1) WHERE n1.name~='.*$val.*' RETURN n1 LIMIT 20;"
        result = tx.run(sql, val=val)
        return result
