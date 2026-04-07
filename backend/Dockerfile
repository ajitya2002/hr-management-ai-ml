FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Install dependencies required by Ollama
RUN apt-get update && apt-get install -y \
    curl \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

COPY . .

 COPY start.sh /usr/local/bin/start.sh
 RUN chmod +x /usr/local/bin/start.sh

  ENTRYPOINT ["/usr/local/bin/start.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
