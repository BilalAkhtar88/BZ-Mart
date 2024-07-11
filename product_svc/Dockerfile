FROM python:3.12

LABEL maintainer="bilal-akhtar"

WORKDIR /app

# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# # Copy only the necessary files for the poetry installation
# COPY pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-cache --no-interaction

# Copy the rest of the application files
COPY . /app/
# Make port 8000 available to the world outside this container
EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "product_svc.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# Use an official Python runtime as a parent image