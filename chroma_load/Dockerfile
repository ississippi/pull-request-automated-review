# Use a lightweight base image with Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files into the container
COPY load_chroma.py .
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV DOCKER_VOLUME_MOUNTED=true

# Run the script
CMD ["python", "load_chroma.py"]

