FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pygame==2.5.2

COPY . .

CMD ["python", "main.py"]