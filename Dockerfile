# Dockerfile
FROM python:3.10-slim

# System deps (ensure lxml never blocks; also basic build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      libxml2-dev \
      libxslt1-dev \
      zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip install -r requirements.txt

# Add app
COPY . .

# Dash/Gunicorn entrypoint (matches your logs)
ENV PORT=5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "index:server"]
