from py2neo import Graph


def db_auth() -> Graph:
    user = 'neo4j'
    pword = ''
    graph = Graph('bolt://localhost:7687', auth=(user, pword))
    return graph
