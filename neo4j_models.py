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
               identifier=data['identifier'],
               url=data['url'],
               name=data['name'],
               type=data['type'],
               description=data['description'],
               publisher=data['publisher'],
               rest_endpoint=data['rest_endpoint'],
               sparql_endpoint=data['sparql_endpoint'],
               storage=data['storage'])

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


