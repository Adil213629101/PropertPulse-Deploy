# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the FastAPI application code
COPY ./src/api /app/api

# Install any needed dependencies specified in requirements.txt
COPY ./requirements.txt /app/api
RUN pip install --no-cache-dir -r /app/api/requirements.txt

# Expose port 80 to the outside world
EXPOSE 80

# Define environment variable
ENV PYTHONUNBUFFERED 1

# Command to run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
