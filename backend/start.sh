#!/bin/sh

echo "Starting backend..."

# Wait for Ollama
echo "Waiting for Ollama..."
until curl -s http://ollama:11434/api/tags > /dev/null; do
  sleep 2
done

echo "Ollama is ready!"

# Start FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000

echo "Ollama is ready!"
# Pull the phi3:mini model
ollama pull phi3:mini

# Bring the Ollama server process to the foreground so the container stays running
wait $!
