#!/bin/bash
source ./docker/env.prod && psql -U "$ARKLET_POSTGRES_USER" -d "$ARKLET_POSTGRES_NAME" -c "COPY (SELECT ark FROM ark_ark order by random() limit 50) TO STDOUT WITH CSV HEADER";
