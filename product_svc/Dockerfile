FROM python:3.11

WORKDIR /app

# Copy only the necessary files for the poetry installation
COPY pyproject.toml /app/
COPY poetry.lock /app/  
# Include this if you have a poetry.lock file

# Print the current directory contents
RUN ls -al /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-cache --no-interaction

# Copy the rest of the application files
COPY . /app/

# Print the current directory contents again to ensure files are copied
RUN ls -al /app

CMD ["poetry", "run", "uvicorn", "product_svc.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
