#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_pass';
    CREATE DATABASE ecomarket_shard_0;
    CREATE DATABASE ecomarket_shard_1;
EOSQL

echo "host replication replicator all md5" >> "$PGDATA/pg_hba.conf"