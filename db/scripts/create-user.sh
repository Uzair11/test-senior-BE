#!/bin/bash
set -e
POSTGRES="psql --username ${POSTGRES_USER}"

echo "Creating database role: test_user with password $POSTGRES_PASSWORD"
$POSTGRES <<-EOSQL
CREATE USER test_user WITH ENCRYPTED PASSWORD '$POSTGRES_PASSWORD';
CREATE DATABASE test_db;
GRANT ALL PRIVILEGES ON DATABASE test_user TO test_db;
EOSQL
echo "Created role: test_user with password $POSTGRES_PASSWORD"