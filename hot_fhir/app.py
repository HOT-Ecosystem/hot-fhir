from flask import Flask
from flask_on_fhir import FHIR
from flask_on_fhir.restful_resources import NamingSystemResource
from hot_fhir import Neo4jDataEngine

app = Flask(__name__)
fhir = FHIR(app)
fhir.add_fhir_resource(NamingSystemResource)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
