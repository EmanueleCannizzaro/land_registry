# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install poetry and uv
RUN pip install poetry uv

# Copy pyproject.toml and uv.lock to the working directory
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN poetry install --no-root --no-dev

# Copy the rest of the application code
COPY . .

# Expose the port that the service will listen on.
# Cloud Run services listen on the port defined by the PORT environment variable.
# Default to 8080 if PORT is not set.
ENV PORT 8080
EXPOSE $PORT

# Run the application using Gunicorn with Uvicorn workers
# The --chdir app argument is important because the app is inside the 'app' directory
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker app.land_registry_app:app