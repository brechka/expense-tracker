#!/usr/bin/env bash

set -e
set -x

# Wait for the database to be ready
python -c "
from sqlalchemy import create_engine, text
from src.config import DATABASE_URL
import time, sys

engine = create_engine(DATABASE_URL)
for i in range(60):
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        print('Database is ready')
        sys.exit(0)
    except Exception as e:
        print(f'Waiting for database... ({e})')
        time.sleep(1)
print('Database not available after 60s')
sys.exit(1)
"

# Run migrations
python -m alembic upgrade head

echo "Prestart complete"
