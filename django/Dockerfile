# Start from a lightweight Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install PostgreSQL client tools
RUN apt-get update && apt-get install -y postgresql-client

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the startup scripts and make them executable
COPY wait-for-db.sh /wait-for-db.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /wait-for-db.sh /entrypoint.sh

# Copy the entire Django project into the container
COPY . /app/

# Make sure entrypoint.sh is executable
RUN chmod +x /entrypoint.sh /wait-for-db.sh

# Set entrypoint to ensure the container starts with entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Expose the Django port
EXPOSE 8000
