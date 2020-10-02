hot-fhir
==

## Setup

To install all the pip packages with pipenv, run 

```
pipenv install
```

If it fails to install the package `psycopg2`, try the following: 

``` 
env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pipenv install psycopg2
```

## Tests

Docker is used to bring up database containers to be used in the pytest-based tests. 

In the `tests` directory, there is a `docker-compose.yml` file. Don't run this file
from command line. When you run the tests, the docker containers will be started 
automatially by the `pytest-docker` fixtures. 

