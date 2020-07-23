from neo4j import GraphDatabase


class Neo4jModels:
    driver = None

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.graph.close()

    @classmethod
    def create_terminology_service(cls, tx, data):
        cql = ("CREATE (:TerminologyService {"
               " identifier: $identifier,"
               " url: $url,"
               " name: $name,"
               " type: $type,"
               " description: $description,"
               " publisher: $publisher,"
               " rest_endpiont: $rest_endpoint,"
               " sparql_endpoint: $sparql_endpoint,"
               " storage: $storage"
               "})")
        tx.run(cql,
               identifier=data['identifier'],   # identifier is required
               url=data.get('url', None),
               name=data.get('name', None),
               type=data.get('type', None),
               description=data.get('description', None),
               publisher=data.get('publisher', None),
               rest_endpoint=data.get('rest_endpoint', None),
               sparql_endpoint=data.get('sparql_endpoint', None),
               storage=data.get('storage', None))

    @classmethod
    def match_terminology_service_by_name(cls, tx, val):
        val_regex = f'.*{val}.*'
        cql = "MATCH (n1) WHERE n1.name =~ $val RETURN n1 LIMIT 20;"
        result = tx.run(cql, val=val_regex)
        return list(result)

    @classmethod
    def delete_terminology_service(cls, tx, identifier):
        cql = f"MATCH (n1) WHERE n1.identifier=$identifier DELETE n1;"
        tx.run(cql, identifier=identifier)


