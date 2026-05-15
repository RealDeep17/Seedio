# STAGE 1: Builder
FROM python:3.12-alpine AS builder
WORKDIR /app
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    g++ \
    make

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# STAGE 2: Runtime
FROM python:3.12-alpine
WORKDIR /app

# Minimal runtime dependencies
# Handbrake removed to save ~200MB (only used for optional transcoding)
RUN apk add --no-cache \
    py3-libtorrent-rasterbar \
    py3-lxml \
    py3-bcrypt \
    aria2 \
    rsync \
    libpq-dev \
    libxml2 \
    libxslt

# Copy installed python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/usr/lib/python3.12/site-packages:${PYTHONPATH}

COPY . .
# Use sh instead of bash
CMD ["/bin/sh", "-c", "chmod +x entrypoint.sh && ./entrypoint.sh"]