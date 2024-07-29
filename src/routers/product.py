from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.utils.token import get_token_product,decode_token_product_id
from src.schemas.products import AllProduct,PartialUpadate,ProductResponse
from src.models.products import Product
from logs.log_config import logger
from typing import List


products = APIRouter(tags=["Products"])
db = Sessionlocal()



#____________create_products____________

@products.post("/create_products", response_model=ProductResponse)
def create_products(product: AllProduct):
    logger.info("Creating a new product with name: %s", product.name)
    
    if product.discount_percent is not None:
        cal_discount = (product.product_price * product.discount_percent) / 100
        discount_price = product.product_price - cal_discount
    else:
        discount_price = product.product_price

    new_product = Product(
        name=product.name,
        description=product.description,
        product_price=product.product_price,
        discount_percent=product.discount_percent,
        discount_price=discount_price,
        category_id=product.category_id,
        quantity=product.quantity
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    logger.info("Product created with id: %s", new_product.id)
    return new_product



#___________get_products________

@products.get("/get_products", response_model=AllProduct)
def get_products(id: str):
    logger.info("Fetching product with id: %s", id)
    db_product = db.query(Product).filter(Product.id == id, Product.is_active == True, Product.is_deleted == False).first()
    if db_product is None:
        logger.error("Product not found with id: %s", id)
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product



#__________get_all_products____________

@products.get("/get_all_products", response_model=List[AllProduct])
def get_all_products():
    logger.info("Fetching all active and non-deleted products")
    db_products = db.query(Product).filter(Product.is_active == True, Product.is_deleted == False).all()
    if not db_products:
        logger.error("No products found")
        raise HTTPException(status_code=404, detail="Products not found")
    return db_products



#__________update_product_by_patch_____________

@products.patch("/update_product_by_patch", response_model=AllProduct)
def update_product_patch(product: PartialUpadate, id: str):
    logger.info("Updating product with id: %s", id)
    db_product = db.query(Product).filter(Product.id == id, Product.is_active == True, Product.is_deleted == False).first()

    if db_product is None:
        logger.error("Product not found with id: %s", id)
        raise HTTPException(status_code=404, detail="Product not found")

    for field_name, value in product.dict().items():
        if value is not None:
            setattr(db_product, field_name, value)

    db.commit()
    logger.info("Product updated with id: %s", db_product.id)
    return db_product



#_____________delete_products______________

@products.delete("/delete_products")
def delete_product(id: str):
    logger.info("Deleting product with id: %s", id)
    db_product = db.query(Product).filter(Product.id == id, Product.is_active == True, Product.is_deleted == False).first()
    if db_product is None:
        logger.error("Product not found with id: %s", id)
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.is_active = False
    db_product.is_deleted = True
    db.commit()
    logger.info("Product deleted with id: %s", db_product.id)
    return {"message": "Product deleted successfully"}



#____________search_products_by_category_id____________

@products.get("/search_products_by_category_id")
def read_products_by_category(category_id: str):
    logger.info("Searching products with category_id: %s", category_id)
    db_products = db.query(Product).filter(Product.category_id == category_id, Product.is_active == True, Product.is_deleted == False).all()
    if not db_products:
        logger.error("No products found for category_id: %s", category_id)
        raise HTTPException(status_code=404, detail="No products found for the given category")
    return db_products



#_________________filter_products_by_price________________

@products.get("/filter_products_by_price")
def filter_products_by_price(min_price: float, max_price: float):
    logger.info("Filtering products with price between: %s and %s", min_price, max_price)
    products = db.query(Product).filter(Product.product_price >= min_price, Product.product_price <= max_price, Product.is_active == True, Product.is_deleted == False).all()
    if not products:
        logger.error("No products found in the price range: %s - %s", min_price, max_price)
        raise HTTPException(status_code=404, detail="No products found in the given price range")
    return products


#__________________increase_product_quantity________________

@products.patch("/increase_product_quantity", response_model=AllProduct)
def increase_product_quantity(product_id: str, quantity: int):
    logger.info("Increasing quantity of product with id: %s by %s", product_id, quantity)
    db_product = db.query(Product).filter(Product.id == product_id, Product.is_active == True, Product.is_deleted == False).first()
    if db_product is None:
        logger.error("Product not found with id: %s", product_id)
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.quantity += quantity
    db.commit()
    db.refresh(db_product)
    logger.info("Increased quantity of product with id: %s. New quantity: %s", db_product.id, db_product.quantity)
    return db_product



#___________decrease_product_quantity_______________

@products.patch("/decrease_product_quantity", response_model=AllProduct)
def decrease_product_quantity(product_id: str, quantity: int):
    logger.info("Decreasing quantity of product with id: %s by %s", product_id, quantity)
    db_product = db.query(Product).filter(Product.id == product_id, Product.is_active == True, Product.is_deleted == False).first()
    if db_product is None:
        logger.error("Product not found with id: %s", product_id)
        raise HTTPException(status_code=404, detail="Product not found")
    
    if db_product.quantity < quantity:
        logger.error("Insufficient stock for product with id: %s. Available: %s, Requested: %s", product_id, db_product.quantity, quantity)
        raise HTTPException(status_code=400, detail="Insufficient stock")

    db_product.quantity -= quantity
    db.commit()
    db.refresh(db_product)
    logger.info("Decreased quantity of product with id: %s. New quantity: %s", db_product.id, db_product.quantity)
    return db_product
