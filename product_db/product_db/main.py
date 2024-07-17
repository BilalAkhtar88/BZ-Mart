import asyncio
from contextlib import asynccontextmanager
import logging
from typing import List, Any

from fastapi import FastAPI, HTTPException
from product_db.consumers.consume_products import consume_products
from product_db.models import ProductConsumer, ProductStore
from sqlmodel import Session, select
from product_db.db import create_tables, engine, get_session


logging.basicConfig(level= logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info('Creating Tables')
    create_tables()
    logger.info("Tables Created")

    # await create_topic()

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(consume_products())
    ]
    
    yield

    for task in tasks:
        task.cancel()
        await task


app = FastAPI(lifespan=lifespan, title="Product Consumer Service", version='1.0.0')

@app.get('/')
async def root() -> Any:
    return {"message": "Welcome to Products Consumer and Database Service"}

@app.get("/products/", response_model=List[ProductStore])
async def get_products():
    with Session(engine) as session:
        products = session.exec(select(ProductStore)).all()
        return products

@app.get("/products/{product_id}", response_model=ProductStore)
async def get_product(product_id: int):
    with Session(engine) as session:
        product = session.exec(select(ProductStore).where(ProductStore.id == product_id)).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product