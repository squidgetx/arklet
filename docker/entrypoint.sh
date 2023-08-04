#!/usr/bin/env bash
# Getting static files for Admin panel hosting!
set -e

# White while DB is spinning up
echo "pg_isready -h $ARKLET_POSTGRES_HOST -p $ARKLET_POSTGRES_PORT"
while ! pg_isready -h $ARKLET_POSTGRES_HOST -p $ARKLET_POSTGRES_PORT; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

./manage.py migrate

if [ "$ENV" = "dev" ]; then
    ./manage.py runserver 0.0.0.0:$ARKLET_PORT
else
    ./manage.py collectstatic --noinput
    gunicorn arklet.wsgi:application --bind 0.0.0.0:$ARKLET_PORT 
fi