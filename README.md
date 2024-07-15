# BZ-Mart
 Backend using FastAPI as assignment of PIAIC

**Steps followed in this project**

Step 1: Create product micro-service as producer

    ->  poetry new product_svc
    ->  thn move directory to product_svc folder using cmd `cd product_svc`
    ->  copy into pyproject.toml thn poetry install
    ->  create Dockerfile inside this folder for production
    ->  create .env file and .dockerignore file
    ->  inside product_svc folder, create settings.py file
    ->  inside product_svc folder, create models.py file using BaseModel in producer because we are not creating any table in database
    ->  inside product_svc folder, create main.py file containing all the business logic

Step Last: Create compose.yaml file accordingly

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


    
