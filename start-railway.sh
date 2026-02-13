#!/bin/bash

# Start nginx in background
nginx &

# Start FastAPI backend
cd /app/backend
python -m uvicorn api:app --host 0.0.0.0 --port 8000
