#!/bin/bash -e

until psql -h "$DB_HOST" -U "$DB_USER" -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

exec "$@"
