# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements-refactored.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-refactored.txt

# Copy application code
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Command to run the application
CMD ["streamlit", "run", "ui/streamlit/app.py", "--server.port=8501", "--server.address=0.0.0.0"]