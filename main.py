from dataclasses import dataclass
from math import prod
from fastapi import FastAPI
import psycopg2
from psycopg2 import sql
from pydantic import BaseModel

app = FastAPI()
import uuid

# Generate a UUID based on the current timestamp and MAC address
unique_id = uuid.uuid1()

print("Generated UUID:", unique_id)
# Get all products
# Get single product
# Delete a single product
# Delete all product at once
# Add a product


# Schema
# id
# name
# image
# price
# quantity


class Product(BaseModel):
    id: str
    name: str
    image: str
    price: int
    qunatity: int


connection = psycopg2.connect(
    host="localhost",
    database="products",
    user="postgres",
    password="18218910p",
    port=5432,
)

try:
    print("Data base connected")
except psycopg2.Error as e:
    print("Error connecting to the database:", e)

cursor = connection.cursor()

table_name = "productTable"


def closeCursorConnection():
    cursor.close()
    connection.close()


# check table is created Already
def isTableAlreadyCreated():
    check_table_query = sql.SQL(
        """
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = %s
    )
    """
    )
    cursor.execute(check_table_query, (table_name,))
    # Fetch the result
    table_exists = cursor.fetchone()[0]
    return table_exists


def addProductToTable(product: Product):
    # create_script = """
    #     CREATE TABLE IF NOT EXISTS productTable (
    #     id VARCHAR PRIMARY KEY,
    #     name VARCHAR,
    #     image VARCHAR,
    #     price int,
    #     qunatity int
    #     )
    # """
    # cursor.execute(create_script)

    insert_script = sql.SQL(
        """
        INSERT INTO productTable (id, name, image, price, qunatity)
        VALUES (%s, %s, %s, %s, %s)
            """
    ).format(sql.Identifier(table_name))
    data_to_insert = (
        str(unique_id),
        product["name"],
        product["image"],
        product["price"],
        product["qunatity"],
    )
    cursor.execute(insert_script, data_to_insert)
    connection.commit()
    #closeCursorConnection()

    return product


# Fast API's
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


@app.post("/app-product", response_model=Product)
async def add_product(product: Product):
    addProductToTable(product.dict())
    return product
