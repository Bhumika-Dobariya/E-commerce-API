from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.utils.token import get_token_product,decode_token_product_id
from src.schemas.products import AllProduct,PartialUpadate
from src.models.products import Product



products = APIRouter(tags=["Products"])
db = Sessionlocal()



#create product

@products.post("/create_products",response_model=AllProduct)
def create_products(product:AllProduct):
    new_product = Product(
    name  = product.name,
    description = product.description,
    price = product.price,
    category_id = product.category_id,
    stock_quantity = product.stock_quantity  
    )
    db.add(new_product)
    db.commit()
    return new_product


#get product

@products.get("/get_products",response_model=AllProduct)
def get_products(id:str):
    db_product = db.query(Product).filter(Product.id ==id,Product.is_active==True,Product.is_deleted==False).first()
    if db_product is None:
        raise HTTPException(status_code=404,detail="products not found")
    return db_product



#get all products

@products.get("/get_all_products",response_model=list[AllProduct])
def get_all_category():
    db_products = db.query(Product).filter(Product.is_active==True,Product.is_deleted==False).all()
    if db_products is None:
        raise HTTPException(status_code=404,detail ="products not found")
    return db_products



#update product

@products.patch("/update_product_by_patch", response_model=AllProduct)
def update_product_patch(product: PartialUpadate,id:str):
    
    db_products = db.query(Product).filter(Product.id == id, Product.is_active == True,Product.is_deleted==False).first()

    if  db_products  is None:
        raise HTTPException(status_code=404, detail="product not found")

    for field_name, value in product.dict().items():
        if value is not None:
            setattr( db_products , field_name, value)

    db.commit()
    return  db_products 



#delete product

@products.delete("/delete_products")
def delete_product(id:str):
    db_product = db.query(Product).filter(Product.id==id,Product.is_active==True,Product.is_deleted==False).first()
    if db_product is None:
        raise HTTPException(status_code=404,detail="products not found")
    db_product.is_active=False
    db_product.is_deleted =True
    db.commit()
    return {"message": "products deleted successfully"}



#search products by category

@products.get("/search_products_by_category_id")
def read_products_by_category(category_id: str):
    db_product = db.query(Product).filter(Product.category_id == category_id).all()
    if not db_product:
        raise HTTPException(status_code=404, detail="No products found for the given category")
    return db_product