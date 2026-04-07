#!/bin/sh

echo "Starting backend..."

# Wait for Ollama (external service)
echo "Waiting for Ollama..."
until curl -s http://ollama:11434/api/tags > /dev/null; do
  sleep 2
done

echo "Ollama is ready!"

#  Start FastAPI ONLY
uvicorn main:app --host 0.0.0.0 --port 8000