#!/bin/bash
set -e

#
# Initialise the mpaf user
# Note that this will only be executed when the server executes
# with an empty datadir (i.e. only when initdb is executed).

psql -v ON_ERROR_STOP=1 \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" <<__EOD__
    CREATE ROLE mpaf ENCRYPTED PASSWORD 'mpaf' login;
    CREATE SCHEMA mpaf;
    ALTER SCHEMA mpaf OWNER TO mpaf;
    ALTER ROLE mpaf SET search_path TO mpaf;
__EOD__
