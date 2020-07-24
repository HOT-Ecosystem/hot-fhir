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
    def match_label_by_name(cls, tx, name, label=None):
        val = f'.*{name}.*'
        label = ':' + label if label is not None else ''
        cql = f"MATCH (n{label}) WHERE n.name =~ $val RETURN n LIMIT 20"
        result = tx.run(cql, val=val)
        return list(result)

    @classmethod
    def delete_label_by_identifier(cls, tx, identifier, label=None):
        label = ':' + label if label is not None else ''
        cql = f"MATCH (n{label}) WHERE n.identifier=$identifier DELETE n;"
        tx.run(cql, identifier=identifier)

    @classmethod
    def create_naming_system(cls, tx, data):
        cql = ("CREATE (:NamingSystem {"
               " identifier: $identifier,"
               " name: $name,"
               " kind: 'codesystem',"
               " status: $status,"
               " publisher: $publisher,"
               " type: $type,"
               " usage: $usage,"
               " unique_id: $unique_id"
               " })")
        tx.run(cql,
               identifier=data.get('identifier', None),
               name=data.get('name', None),
               kind=data.get('kind', None),
               status=data.get('status', None),
               type=data.get('type', None),
               usage=data.get('$usage', None),
               publisher=data.get('publisher', None),
               unique_id=data.get('unique_id', None))

    @classmethod
    def match_naming_system_by_name(cls, tx, name):
        @classmethod
        def match_terminology_service_by_name(cls, tx, name):
            val = f'.*{name}.*'
            cql = "MATCH (n1:NamingSystem) WHERE n1.name =~ $val RETURN n1 LIMIT 20;"
            result = tx.run(cql, val=val)
            return list(result)


