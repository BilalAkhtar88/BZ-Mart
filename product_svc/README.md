# Product Microservice

The `product_svc` microservice is responsible for handling the creation, updating, and deletion of product details. This microservice uses FastAPI to expose REST endpoints and Kafka to send messages to other services in the system. This service does not directly interact with the database, ensuring a decoupled architecture.

## Features

- **Post Method**: Creates a new product and sends the details to the Kafka broker.
- **Put Method**: Updates an existing product and sends the updated details to the Kafka broker.
- **Delete Method**: Deletes a product and sends the delete request to the Kafka broker.

## Steps Followed in This Project

### Step 1: Create the Product Microservice

1. **Create Project Structure**:
   - Run `poetry new product_svc` to create a new project.
   - Navigate to the project directory using `cd product_svc`.

2. **Initialize Dependencies**:
   - Copy the necessary dependencies into `pyproject.toml`.
   - Run `poetry install` to install the dependencies.

3. **Create Dockerfile**:
   - Create a `Dockerfile` inside the `product_svc` directory for production.

4. **Create Environment and Ignore Files**:
   - Create a `.env` file for environment variables.
   - Create a `.dockerignore` file to ignore unnecessary files during Docker build.

5. **Configure Application Settings**:
   - Create a `settings.py` file inside the `product_svc` directory to manage configuration settings.

6. **Define Data Models**:
   - Create a `models.py` file inside the `product_svc` directory.
   - Define data models using `BaseModel` from Pydantic in `models.py`. We use `BaseModel` because we are not creating any table and thus not using `SQLModel`.

7. **Implement Business Logic**:
   - Create a `main.py` file inside the `product_svc` directory containing all the business logic and API endpoints.

## API Endpoints

### 1. Create Product (POST /products/)
- **Description**: This endpoint creates a new product and sends the product details to the Kafka broker.
- **Request Body**:
  ```json
  {
    "product_id": "string",
    "name": "string",
    "description": "string",
    "price": 0.0,
    "quantity": 0
  }
