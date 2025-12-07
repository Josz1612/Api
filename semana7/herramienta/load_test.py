"""load_test.py
Simple load test that writes users then issues reads via the router.
Usage:
  pip install psycopg2-binary
  python tools/load_test.py --writes 100 --reads 200

This script uses `tools/pg_shard_router.py` to route queries.
"""
import argparse
import time
import random
import os
import sys

# Ensure the tools directory is on sys.path so sibling imports work when running
# the script from the repository root: `python tools/load_test.py`.
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

try:
    from pg_shard_router import PGRouter
except Exception as e:
    print('Failed to import pg_shard_router (are you running from the repo root?).', e)
    raise

# Check psycopg2 availability early for clearer errors
try:
    import importlib
    importlib.import_module('psycopg2')  # dynamically import to avoid static-analysis unresolved import
except Exception as e:
    print('psycopg2 is required: install with `pip install psycopg2-binary`')
    raise


def make_user(i):
    return (i, f'user_{i}', f'user{i}@example.com')


def main(writes, reads, delay):
    router = PGRouter()

    # create table on both shards (assumes databases exist)
    for shard in (0, 1):
        dbname = f'ecomarket_shard_{shard}'
        # create table via primary connection
        conn = None
        try:
            conn = router.primary and __import__('psycopg2').connect(host=router.primary['host'], port=router.primary['port'], user=router.primary['user'], password=router.primary['password'], dbname=dbname)
            with conn:
                with conn.cursor() as cur:
                    cur.execute('CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY, name text, email text)')
        finally:
            if conn:
                conn.close()

    print('Starting writes...')
    for i in range(writes):
        user = make_user(i)
        try:
            router.write('users(id,name,email)', str(user[0]), user)
        except Exception as e:
            print('Write error:', e)
        if delay:
            time.sleep(delay)

    print('Starting reads...')
    for _ in range(reads):
        key = str(random.randint(0, max(1, writes - 1))) if writes>0 else None
        try:
            rows = router.read('SELECT id,name,email FROM users LIMIT 10', key)
            # show small sample
            if rows:
                print('Read sample:', rows[:1])
        except Exception as e:
            print('Read error:', e)
        if delay:
            time.sleep(delay)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--writes', type=int, default=100)
    p.add_argument('--reads', type=int, default=200)
    p.add_argument('--delay', type=float, default=0.0)
    args = p.parse_args()
    main(args.writes, args.reads, args.delay)