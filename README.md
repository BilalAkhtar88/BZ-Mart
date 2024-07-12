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

	-> docker compose up
	-> open a new terminal
	-> docker ps
	-> docker logs <add ID of the service> -f
	-> click on the link provided in log
	-> replace redirect after / with docs

    
