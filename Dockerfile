FROM --platform=linux/amd64 python:3.10-slim-bullseye

WORKDIR /app

ENV HF_HOME=/app/huggingface_cache

RUN apt-get update && apt-get install -y --no-install-recommends build-essential pkg-config python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install torch --no-cache-dir --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_md

COPY src/ .
RUN python download_models.py

CMD ["/bin/sh", "-c", "HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python main.py"]
