# Base image python 
FROM python:3.11-slim

# Setup folder
WORKDIR /app

# Copy Library from require
COPY requirements.txt .

# Install all
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]