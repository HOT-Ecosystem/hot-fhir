from flask import Flask
from flask_on_fhir import FHIR
from flask_on_fhir.restful_resources import NamingSystemResource
from hot_fhir.data.neo4j import Neo4jDataEngine
from importer.utils import neo4j_models

engine = Neo4jDataEngine(neo4j_models())

app = Flask(__name__)
fhir = FHIR(app=app, data_engine=engine)
fhir.add_fhir_resource(NamingSystemResource)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
