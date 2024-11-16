# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p uploads analysis_files

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=8080

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application using waitress
CMD ["python", "app.py"]