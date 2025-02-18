#!/bin/bash

# Install dependencies (just in case)
pip install --no-cache-dir -r requirements.txt

# Run database migrations
python3 -m alembic upgrade head  

# Start FastAPI with Uvicorn
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 10000
