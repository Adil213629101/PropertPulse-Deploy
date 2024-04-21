# Dockerfile

# Use the official Python image as base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the source code into the container
COPY src/ .

# Expose ports
EXPOSE 5000 8000

# Command to run the Flask and FastAPI apps
CMD ["bash", "-c", "(cd src/web && python app.py) & (cd src/api && python -m uvicorn main:app --host 0.0.0.0 --port 8000)"]