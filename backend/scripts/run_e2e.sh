#!/bin/bash

echo "Starting FastAPI server in the background..."
uvicorn chessapp.interface.main:app &
UVICORN_PID=$!

echo "Starting Angular frontend in the background..."
cd ../frontend && npm start &
ANGULAR_PID=$!

echo "Waiting for services to start..."
sleep 10 # Give Node and Python both some time to start up

cd ../backend

echo "Running integration tests..."
PYTHONPATH=. pytest chessapp/tests/integration/test_game_e2e.py
TEST_EXIT_CODE=$?

echo "Stopping Angular frontend (PID: $ANGULAR_PID)..."
kill $ANGULAR_PID

echo "Stopping FastAPI server (PID: $UVICORN_PID)..."
kill $UVICORN_PID

exit $TEST_EXIT_CODE
