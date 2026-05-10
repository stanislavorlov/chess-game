FROM python:3.13.2-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /predictapp

# Install build dependencies, then clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    gcc \
    musl-dev && \
    rm -rf /var/lib/apt/lists/*

COPY predictapp/requirements.txt /predictapp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY predictapp/ /predictapp/predictapp/
# Reference to chessengine removed as per user instruction; integrated into predictapp

CMD ["python3", "predictapp/interface/main.py"]