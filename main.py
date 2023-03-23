from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Tuple
import mysql.connector

app= FastAPI()

def get_db():
    db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sql@8057",
        database="products")
    return db

class products(BaseModel):
    product_id: int
    product_name: str
    qnt: str
    mfc_date: str
    exp_date: str

@app.get("/")
def get_all_products():
    db= get_db()
    cursor= db.cursor()
    query= "SELECT * FROM market_products"
    cursor.execute(query)
    result= cursor.fetchall()
    db.close()
    return result
    

@app.get('/products/{product_name}')
def get_product(product_name: str):
    db= get_db()
    cursor= db.cursor()
    query= f"SELECT * FROM market_products WHERE product_name= '{product_name}'"
    cursor.execute(query)
    result=cursor.fetchall()
    db.close()
    return result

@app.post('/products')
def create_product(product: products):
    db= get_db()
    products = product.dict()
    cursor= db.cursor()
    query= f"""INSERT INTO market_products (product_id,product_name,qnt,mfc_date,exp_date) 
            VALUES('{products["product_id"]}','{products["product_name"]}','{products["qnt"]}','{products["mfc_date"]}','{products["exp_date"]}')"""
    cursor.execute(query)
    db.commit()
    db.close()
    return{"message":"New product is added in record"}


@app.put('/product/{product_id}')
def update_product(product_id: int, product:products):
    db= get_db()
    products = product.dict()
    cursor = db.cursor()
    query = """UPDATE market_products SET product_id = %s, product_name = %s, qnt = %s, mfc_date = %s, exp_date = %s 
                WHERE product_id = %s"""
    values = (products["product_id"], products["product_name"], products["qnt"], products["mfc_date"], products["exp_date"], product_id)
    cursor.execute(query,values)
    db.commit()
    db.close()
    return {"message": "product updated successfully"}


@app.delete('/product/{product_id}')
def delete_product(product_id: int):
    db= get_db()
    cursor = db.cursor()
    query = f"DELETE FROM market_products WHERE product_id = '{product_id}'"
    cursor.execute(query)
    db.commit()
    db.close()
    return {"message": f"product with product_id:{product_id} was deleted"}







