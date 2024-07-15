import asyncio
from contextlib import asynccontextmanager
# from fastapi.concurrency import asynccontextmanager
import logging
from typing import Annotated, Any, AsyncGenerator
from fastapi import Depends, FastAPI

# I will store in json format, therefore does not require the proto file
# from product_svc.proto import product_pb2, operation_pb2
import json

from product_svc.models import Product, ProductUpdate
from product_svc.settings import BOOTSTRAP_SERVER, KAFKA_PRODUCT_TOPIC
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

MAX_RETRIES = 5
RETRY_INTERVAL = 10

async def create_topic():
    admin_client = AIOKafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVER)

    retries = 0

    while retries < MAX_RETRIES:
    # while True:
        try:
            await admin_client.start()
            topic_list = [NewTopic(name=KAFKA_PRODUCT_TOPIC,
                                num_partitions=2, 
                                replication_factor=1)]
            try:
                await admin_client.create_topics(new_topics=topic_list, validate_only=False)
                print(f"Topic '{KAFKA_PRODUCT_TOPIC}' created successfully")
            except Exception as e:
                print(f"Failed to create topic '{KAFKA_PRODUCT_TOPIC}': {e}")
            finally:
                await admin_client.close()
            return
        
        except KafkaConnectionError:
            retries += 1 
            print(f"Kafka connection failed. Retrying {retries}/{MAX_RETRIES}...")
            await asyncio.sleep(RETRY_INTERVAL)
        
    raise Exception("Failed to connect to kafka broker after several retries")

async def kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_topic()
    yield

app = FastAPI(lifespan=lifespan, title="Product Service", version='1.0.0')

@app.get('/')
async def root() -> Any:
    return {"message": "Welcome to Products Producer Service"}

logging.basicConfig(level= logging.INFO)
logger = logging.getLogger(__name__)

@app.post('/products/')
# Try following instead of above when returning something in response_model=Product
# @app.post('/products/', response_model=Product)
async def create_product(
    product: Product,
    producer: Annotated[AIOKafkaProducer, Depends(kafka_producer)]
):
    serialized_product = json.dumps(product.__dict__).encode('utf-8')
    # serialized_product.operation = "CREATE"

    logger.info(f"Received Message: {serialized_product}")

    await producer.send_and_wait(KAFKA_PRODUCT_TOPIC, serialized_product)

    return {"message" : "Created product successfully!"}

@app.put('/products/{id}')
async def edit_product(id: int, 
                       product: ProductUpdate,
                       producer: Annotated[AIOKafkaProducer, Depends(kafka_producer)]
                       ):
    
    logger.info(f"Received product data for update: {product}")

    serialized_product = json.dumps(product.__dict__).encode('utf-8')
    serialized_product.operation = "UPDATE"
    serialized_product.id = id
    # serialized_product.product_id = product.product_id
    # serialized_product.name = product.name
    # serialized_product.price = product.price
    # serialized_product.category = product.category
    # serialized_product.description = product.description
    # serialized_product.operation = "UPDATE"
        
    # serialized_product = product_proto.SerializeToString()
    await producer.send_and_wait(KAFKA_PRODUCT_TOPIC, serialized_product)

    return {"message": "Product updated successfully!"}