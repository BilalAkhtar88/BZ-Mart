FROM python:3.11
# Use the official Python 3.11 image as the base

WORKDIR /app
# Set the working directory to /app

COPY pyproject.toml poetry.lock /app/
# Copy pyproject.toml and poetry.lock into the /app directory

RUN pip install poetry
# Install Poetry

RUN poetry config virtualenvs.create false
# Configure Poetry to not create a virtual environment

RUN poetry install --no-root --no-cache --no-interaction
# Install dependencies listed in pyproject.toml

COPY . /app/
# Copy the entire directory into /app

CMD ["poetry", "run", "uvicorn", "product_svc.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# Command to run your application
