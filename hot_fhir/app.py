from flask import Flask
from flask_on_fhir import FHIR

app = Flask(__name__)
fhir = FHIR(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
