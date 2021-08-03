#!/bin/bash
set -e

#
# Initialise the keycloak user
# Note that this will only be executed when the server executes
# with an empty datadir (i.e. only when initdb is executed).

psql -v ON_ERROR_STOP=1 \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" <<__EOD__
    CREATE ROLE keycloak ENCRYPTED PASSWORD 'keycloak' login;
    CREATE SCHEMA keycloak;
    ALTER SCHEMA keycloak OWNER TO keycloak;
    ALTER ROLE keycloak SET search_path TO keycloak;
__EOD__
