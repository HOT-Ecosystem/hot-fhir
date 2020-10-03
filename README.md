hot-fhir
==

![Tests](https://github.com/HOT-Ecosystem/hot-fhir/workflows/Tests/badge.svg)

## Tests

Docker is used to bring up database containers to be used in the pytest-based tests. 

In the `tests` directory, there is a `docker-compose.yml` file. Don't run this file
from command line. When you run the tests, the docker containers will be started 
automatially by the `pytest-docker` fixtures. 

