FROM python:3.11

WORKDIR /app

# Copy only the necessary files for the poetry installation
COPY pyproject.toml /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-cache --no-interaction

# Copy the rest of the application files
COPY . /app/

CMD ["poetry", "run", "uvicorn", "product_svc.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
