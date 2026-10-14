FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . .

# Install Python dependencies (if needed)
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || true

# Make script executable
RUN chmod +x main.py

# Expose ports if needed
# EXPOSE 8080

# Run the application
CMD ["python", "main.py"]
