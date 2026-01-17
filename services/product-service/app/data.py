# Mock database for products
PRODUCTS_DB = [
    {
        "id": 1,
        "name": "Laptop",
        "description": "High-performance laptop",
        "price": 1299.99,
        "stock": 10,
        "category": "Electronics",
        "rating": 4.5,
        "reviews_count": 120
    },
    {
        "id": 2,
        "name": "Wireless Mouse",
        "description": "Ergonomic wireless mouse",
        "price": 29.99,
        "stock": 50,
        "category": "Accessories",
        "rating": 4.2,
        "reviews_count": 340
    },
    {
        "id": 3,
        "name": "USB-C Cable",
        "description": "High-speed USB-C cable",
        "price": 12.99,
        "stock": 100,
        "category": "Cables",
        "rating": 4.0,
        "reviews_count": 450
    },
    {
        "id": 4,
        "name": "Mechanical Keyboard",
        "description": "RGB mechanical keyboard",
        "price": 149.99,
        "stock": 25,
        "category": "Peripherals",
        "rating": 4.7,
        "reviews_count": 280
    }
]

def get_all_products():
    return PRODUCTS_DB

def get_product_by_id(product_id: int):
    for product in PRODUCTS_DB:
        if product["id"] == product_id:
            return product
    return None

def create_product(product: dict):
    new_id = max([p["id"] for p in PRODUCTS_DB]) + 1
    product["id"] = new_id
    PRODUCTS_DB.append(product)
    return product

def update_product(product_id: int, updated_data: dict):
    for product in PRODUCTS_DB:
        if product["id"] == product_id:
            product.update(updated_data)
            return product
    return None

def delete_product(product_id: int):
    global PRODUCTS_DB
    PRODUCTS_DB = [p for p in PRODUCTS_DB if p["id"] != product_id]
    return True
