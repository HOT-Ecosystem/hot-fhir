from neo4j import GraphDatabase


class Neo4jModels:
    driver = None

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

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
               url=data.get('url'),
               name=data.get('name'),
               type=data.get('type'),
               description=data.get('description'),
               publisher=data.get('publisher'),
               rest_endpoint=data.get('rest_endpoint'),
               sparql_endpoint=data.get('sparql_endpoint'),
               storage=data.get('storage'))

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
        cql = f"MATCH (n{label}) WHERE n.identifier=$identifier DELETE n"
        tx.run(cql, identifier=identifier)

    @classmethod
    def create_naming_system(cls, tx, data):
        cql = ("CREATE (:NamingSystem {"
               " identifier: $identifier,"
               " name: $name,"
               " kind: $kind,"
               " status: $status,"
               " publisher: $publisher,"
               " usage: $usage,"
               " uri: $uri,"
               " preferred_prefix: $preferred_prefix,"
               " description: $description"
               "})")
        tx.run(cql,
               identifier=data['identifier'],   # identifier is required
               name=data.get('name'),
               kind=data.get('kind'),
               status=data.get('status'),
               publisher=data.get('publisher'),
               usage=data.get('usage'),
               uri=data.get('uri'),
               preferred_prefix=data.get('preferred_prefix'),
               description=data.get('description'))


