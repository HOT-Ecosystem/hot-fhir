from importer.utils import mongo_collection, neo4j_models

"""
Import data from mangodb to neo4j 
"""


def import_collection(collection):
    neo4j = neo4j_models()
    ontos = {}
    col = mongo_collection(collection)
    for item in col.find():
        onto = dict()
        onto['uri'] = item['config']['id']
        onto['name'] = item['config']['title']
        onto['kind'] = 'codesystem'
        onto['description'] = item['config']['description']
        onto['identifier'] = item['ontologyId'].lower()
        onto['preferred_prefix'] = item['config'].get('preferredPrefix', '').upper()
        ontos[onto['preferred_prefix']] = onto
    with neo4j.driver.session() as session:
        for prefix, onto in ontos.items():
            session.write_transaction(neo4j.create_naming_system, onto)
    neo4j.close()


if __name__ == '__main__':
    import_collection('ols')

#
#
#
#
#
# col = mongo_collection('bioportal')
# for item in col.find():
#     onto = dict()
#     onto['title'] = item['name']
#     onto['namespace'] = item['acronym']
#     onto['uri'] = item['@id']
#     if onto['namespace'] in ontos:
#         print(ontos[onto['namespace']])
#         print(onto)
#         duplicates.append(onto['namespace'])
#     else:
#         ontos[onto['namespace']] = onto
#
# # print(onto)
#
# duplicates.sort()
# print(duplicates)
# print(len(duplicates))