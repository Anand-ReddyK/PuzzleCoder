# FROM python:3.8

# RUN apt-get update && \
#     apt-get install -y openjdk-11-jdk nodejs npm && \
#     apt-get clean

# WORKDIR /app

# COPY . .

# RUN pip install --no-cache-dir -r requirements.txt

# ENTRYPOINT [ "python", "worker.py" ]


# Use an official base image with a lightweight Linux distribution
FROM ubuntu:22.04

# Install common dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg2 \
    software-properties-common \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Java (OpenJDK 11)
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "worker.py" ]