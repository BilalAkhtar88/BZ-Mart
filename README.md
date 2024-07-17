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

### Step Last: Create compose.yaml File
1. Define services and dependencies in compose.yaml.
2. Configure Docker Compose for orchestration of microservices.














### Steps I wrote earlier, to be formatted for help.


**Step to run code on Google Shell**

Step 1: Push the code to github and run google shell.

	-> docker compose build --no-cache
	-> docker compose up
	-> open a new terminal
	-> docker ps
	-> docker logs <add ID of the service> -f
	-> click on the link provided in log
	-> replace redirect after / with docs

**Product Microservice**

Step 1: No get method for fetching product details from db in this microservice, to keep this service completely delinked from database
Step 2: Post method used to create a new product and send to kafka broker
Step 3: Put method used to update an existing product and send to kafka broker
Step 4: Delete method used to delete a product and send to kafka broker


    
