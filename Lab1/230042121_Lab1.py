from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to Server Programming!"
            
    }

@app.get("/hello/{name}")
def get_hello(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/square/{number}")
def get_square(number: int):
    return {"number": number, "square": number * number}



products = [
    {"id": 1, "name": "Laptop", "price": 75000},
    {"id": 2, "name": "Mouse", "price": 800},
    {"id": 3, "name": "Keyboard", "price": 1500},
    {"id": 4, "name": "Monitor", "price": 12000},
    {"id": 5, "name": "Headphones", "price": 2500},
    {"id": 6, "name": "Webcam", "price": 3000},
    {"id": 7, "name": "USB Cable", "price": 300},
    {"id": 8, "name": "Mouse Pad", "price": 500},
    {"id": 9, "name": "Printer", "price": 18000},
    {"id": 10, "name": "Speaker", "price": 1800},
]
@app.get("/products")
def get_products():
    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

class ProductCreate(BaseModel):
    name: str
    price: float


@app.post("/products")
def create_product(new_product: ProductCreate):
    if len(products) == 0:
        new_id = 1
    else:
        new_id = max(p["id"] for p in products) + 1

    product = {"id": new_id, "name": new_product.name, "price": new_product.price}
    products.append(product)
    return product



@app.get("/products/search")
def search_products(name: str):
    results = []
    for product in products:
        if name.lower() in product["name"].lower():
            results.append(product)
    return results
@app.get("/products/affordable")
def affordable_products(max_price: float):
    results = []
    for product in products:
        if product["price"] <= max_price:
            results.append(product)
    return results


