# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the configuration file into the container
# COPY api_config.yaml /app/api_config.yaml

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 4501

# Define the command to run the application
CMD ["python", "mock_api.py"]