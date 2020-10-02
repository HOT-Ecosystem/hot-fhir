FROM fhirbase/fhirbase:latest
WORKDIR /fhirbase

USER postgres

RUN PGDATA=/pgdata /docker-entrypoint.sh postgres  & \
    until psql -U postgres -c '\q'; do \
        >&2 echo "Postgres is starting up..."; \
        sleep 5; \
    done && \
    psql -U postgres -c 'drop database fhirbase;' && \
    psql -U postgres -c 'create database fhirbase;' && \
    fhirbase -d fhirbase --fhir=4.0.0 init && \
    pg_ctl -D /pgdata stop

CMD pg_ctl -D /pgdata start && until psql -U postgres -c '\q'; do \
        >&2 echo "Postgres is starting up..."; \
        sleep 5; \
    done && \
    exec fhirbase -d fhirbase web