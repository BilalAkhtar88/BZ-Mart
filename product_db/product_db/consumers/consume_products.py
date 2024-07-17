import json
import logging

from product_db.consumers.consumer import create_consumer
from product_db.models import ProductConsumer, ProductStore
from product_db.db import engine
from product_db.setting import KAFKA_PRODUCT_CONSUMER_GROUP_ID, KAFKA_PRODUCT_TOPIC
from sqlmodel import Session, select


logging.basicConfig(level= logging.INFO)
logger = logging.getLogger(__name__)


async def consume_products():
    consumer = await create_consumer(KAFKA_PRODUCT_TOPIC, KAFKA_PRODUCT_CONSUMER_GROUP_ID)
    if not consumer:
        logger.error("Failed to create kafka product consumer")
        return

    try:
        async for msg in consumer:
            try:
                # Parse the JSON message
                product = json.loads(msg.value)
                logger.info(f"Received Message: {product}")

                with Session(engine) as session:
                    logger.info(f"Session has started!")
                    if product.get("operation") in ["CREATE", "Create", "create"]:
                        logger.info(f"Create command received and updating Database now!")
                        # Your code to handle the CREATE operation                        
                        new_product = ProductStore(
                            name=product.get("name"),
                            product_id=product.get("product_id"),
                            description=product.get("description"),
                            price=product.get("price"),
                            category=product.get("category")
                        )
                        session.add(new_product)
                        session.commit()
                        session.refresh(new_product)
                        logger.info(f'Product added to db: {new_product}')
                    
                    elif product.get("operation") in ["UPDATE", "Update", "update"]:
                        existing_product = session.exec(select(ProductStore).where(ProductStore.id == product.get("id") and ProductStore.name == product.get("name"))).first()
                        if existing_product:
                            existing_product.name = product.get("name")
                            existing_product.product_id = product.get("product_id")
                            existing_product.description = product.get("description")
                            existing_product.price = product.get("price")
                            existing_product.category = product.get("category")
                            session.add(existing_product)
                            session.commit()
                            session.refresh(existing_product)
                            logger.info(f'Product updated in db: {existing_product}')
                        else:
                            logger.warning(f"Product with ID {product.id} and name {product.name} not found")

                    elif product.get("operation") in ["DELETE", "Delete", "delete"]:
                        existing_product = session.exec(select(ProductStore).where(ProductStore.id == product.get("id"))).first()
                        if existing_product:
                            session.delete(existing_product)
                            session.commit()
                            logger.info(f"Product with ID {product.id} successfully deleted")
                        else:
                            logger.warning(f"Product with ID {product.id} not found for deletion")

            except Exception as e:
                logger.error(f"Error processing message: {e}")

    finally:
        await consumer.stop()
        logger.info("Consumer stopped")
    return