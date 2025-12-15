# 1. The Base Layer: A lightweight Linux with Python 3.10 installed
FROM python:3.10-slim

# 2. The Setup: Create a folder inside the container
WORKDIR /app

# 3. The Prerequisites: Copy just the requirements first
# (We do this before copying code so Docker can cache the installation)
COPY requirements.txt .

# 4. The Installation: Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 5. The Copy: Copy your actual source code into the container
COPY . .

# 6. The Launch Command: Start the API server
# --host 0.0.0.0 is required for Docker to expose the network
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]