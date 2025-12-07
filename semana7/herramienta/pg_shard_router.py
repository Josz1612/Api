"""pg_shard_router.py
Simple sharding router that sends writes to primary and reads to replicas.
Sharding: hash(key) % 2 -> selects shard 0 or 1 (databases: ecomarket_shard_0/1)
Reads: round-robin among replicas.

Usage: set environment variables or edit the CONNECTIONS dict below.
Requires: psycopg2-binary
"""
import os
import hashlib
import threading
import random
from typing import TYPE_CHECKING, List, Tuple, Optional

import importlib

_psycopg2_import_error = None
psycopg2 = None
if TYPE_CHECKING:
    # allow type checkers to see psycopg2 symbols without requiring it at runtime
    import psycopg2  # type: ignore
else:
    try:
        psycopg2 = importlib.import_module('psycopg2')
    except Exception as e:
        psycopg2 = None
        _psycopg2_import_error = e

# Configuration: hosts and ports for primary and replicas
PRIMARY = {
    'host': os.getenv('PG_PRIMARY_HOST', 'localhost'),
    'port': int(os.getenv('PG_PRIMARY_PORT', '5432')),
    'user': os.getenv('PG_PRIMARY_USER', 'postgres'),
    'password': os.getenv('PG_PRIMARY_PASSWORD', 'postgres'),
}
REPLICAS = [
    {
        'host': os.getenv('PG_REPLICA1_HOST', 'localhost'),
        'port': int(os.getenv('PG_REPLICA1_PORT', '5433')),
        'user': os.getenv('PG_REPLICA1_USER', 'postgres'),
        'password': os.getenv('PG_REPLICA1_PASSWORD', 'postgres'),
    },
    {
        'host': os.getenv('PG_REPLICA2_HOST', 'localhost'),
        'port': int(os.getenv('PG_REPLICA2_PORT', '5434')),
        'user': os.getenv('PG_REPLICA2_USER', 'postgres'),
        'password': os.getenv('PG_REPLICA2_PASSWORD', 'postgres'),
    }
]

_shard_lock = threading.Lock()
_replica_index = 0


def _get_shard(key: str) -> int:
    h = hashlib.md5(key.encode()).hexdigest()
    return int(h, 16) % 2


def _get_replica() -> dict:
    global _replica_index
    with _shard_lock:
        idx = _replica_index % len(REPLICAS)
        _replica_index += 1
    return REPLICAS[idx]


def _connect(cfg: dict, dbname: str):
    if psycopg2 is None:
        raise RuntimeError(f"psycopg2 is required but failed to import: {_psycopg2_import_error}")
    return psycopg2.connect(host=cfg['host'], port=cfg['port'], user=cfg['user'], password=cfg['password'], dbname=dbname)


class PGRouter:
    def __init__(self, primary_cfg=PRIMARY, replicas=REPLICAS):
        self.primary = primary_cfg
        self.replicas = replicas

    def write(self, table: str, key: str, values: Tuple):
        """Write to primary; chooses shard by key."""
        shard = _get_shard(key)
        dbname = f'ecomarket_shard_{shard}'
        conn = _connect(self.primary, dbname)
        try:
            with conn:
                with conn.cursor() as cur:
                    # naive insert - user should adapt columns/order
                    placeholders = ','.join(['%s'] * len(values))
                    sql = f"INSERT INTO {table} VALUES ({placeholders})"
                    cur.execute(sql, values)
        finally:
            conn.close()

    def read(self, query: str, key: Optional[str] = None):
        """Read using a replica (round-robin). If key provided, shard by key to select DB name."""
        replica = _get_replica()
        if key is None:
            # random shard if no key
            shard = random.randint(0, 1)
        else:
            shard = _get_shard(key)
        dbname = f'ecomarket_shard_{shard}'
        conn = _connect(replica, dbname)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    return cur.fetchall()
        finally:
            conn.close()


if __name__ == '__main__':
    print('PGRouter example. Set env vars and import PGRouter in your scripts.')