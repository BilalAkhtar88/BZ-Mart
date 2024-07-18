# BZ-Mart

Backend using FastAPI as an assignment of PIAIC

## Project Overview

This project aims to develop an online mart API using an event-driven microservices architecture. The API will be built using FastAPI and will leverage Docker, Kafka, PostgreSQL, and Kong for API gateway management. The goal is to create a scalable, maintainable, and efficient system capable of handling high volumes of transactions and data in a distributed manner.

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs with Python.
- **Docker**: Containerization technology for consistent deployment.
- **Kafka**: Distributed event streaming platform for handling asynchronous communication.
- **PostgreSQL**: Relational database for data persistence.
- **Kong**: API Gateway and Microservices Management Layer.
- **DevContainers**: Ensures a consistent development environment.
- **GitHub Actions**: CI/CD pipeline for automated testing and deployment.

## Steps Followed in the Project

### Step 1: Create Product Microservice as Producer

1. Create `product_svc` microservice:
   ```bash
   poetry new product_svc
   cd product_svc
2. Initialize dependencies by copying from existing pyproject.toml file and install packages:
   ```bash
   poetry install
3. Create Dockerfile for production deployment.
4. Create .env file and .dockerignore file.
5. Define application settings in settings.py.
6. Define data models using `BaseModel` in `models.py` in the `product_svc` microservice because we are not creating any table and thus not using SQLModel for direct database interaction.
7. Implement business logic in main.py.

### Step Second Last: Create compose.yaml File
1. Define services and dependencies in compose.yaml.
2. Configure Docker Compose for orchestration of microservices.

### Step Last: Run Code on Google Shell
1. Push the code to GitHub and access Google Shell.
2. Build and run the Docker containers:
   ```bash
   docker compose build --no-cache
   docker compose up
3. Open a new terminal and check running containers
   ```bash
   docker ps
4. View logs of a specific service using following command by replacing the <service_id>:
   ```bash
   docker logs <service_id> -f
5. Access the API documentation:
   Click on the link provided in the logs.
   Replace /redirect with /docs in the URL.
   Change the port numbers in the URL.