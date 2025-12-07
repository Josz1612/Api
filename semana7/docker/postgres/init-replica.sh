#!/bin/bash
set -e

echo "Waiting for primary to be ready..."
until pg_isready -h pg_primary -p 5432 -U postgres; do
    echo "Waiting for primary..."
    sleep 2
done

echo "Cleaning data directory..."
rm -rf /var/lib/postgresql/data/*
chmod 0700 /var/lib/postgresql/data

echo "Starting base backup..."
pg_basebackup -h pg_primary -p 5432 -U replicator -D /var/lib/postgresql/data -Fp -Xs -P -R

echo "Backup completed. Starting Postgres..."
exec docker-entrypoint.sh postgres