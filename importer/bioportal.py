import requests
from importer.utils import config, mongo_collection


def import_bioportal():
    cfg = config()
    key = cfg['bioportal']['api_key']

    name = 'bioportal'

    collection = mongo_collection(name)

    url = 'http://data.bioontology.org/ontologies'

    payload = {'apikey': key}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    res_json = response.json()

    for onto in res_json:
        collection.insert_one(onto)

    print(f'Inserted {len(res_json)} to the collection hotfhir.{name}')


if __name__ == '__main__':
    import_bioportal()
