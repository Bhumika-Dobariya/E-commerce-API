from fastapi import FastAPI, HTTPException, APIRouter, Depends
from database.database import Sessionlocal
from src.schemas.category import Allcategories,Partialcategories
from src.models.category import Category
import uuid

category = APIRouter(tags=["Category"])
db = Sessionlocal()


#create category

@category.post("/create_categories",response_model=Allcategories)
def create_category(category:Allcategories):
    new_category = Category(
        id=str(uuid.uuid4()),
        name= category.name,
        description=category.description,
    )
    db.add(new_category)
    db.commit()
    return new_category



#get category

@category.get("/get_category",response_model=Allcategories)
def get_category(id:str):
    db_category = db.query(Category).filter(Category.id==id,Category.is_active==True,Category.is_deleted==False).first()
    if db_category is None:
        raise HTTPException(status_code=404,detail="category not found")
    return db_category



#get all category

@category.get("/get_all_category",response_model=list[Allcategories])
def get_all_category():
    db_category = db.query(Category).filter(Category.is_active==True,Category.is_deleted==False).all()
    if db_category is None:
        raise HTTPException(status_code=404,detail ="category not found")
    return db_category



#update category

@category.patch("/update_category_by_patch", response_model=Allcategories)
def update_category_patch(categorys: Partialcategories,id:str):
    
    db_category = db.query(Category).filter(Category.id == id, Category.is_active == True,Category.is_deleted==False).first()

    if  db_category is None:
        raise HTTPException(status_code=404, detail="category not found")

    for field_name, value in categorys.dict().items():
        if value is not None:
            setattr( db_category, field_name, value)

    db.commit()
    return  db_category


#delete category

@category.delete("/delete_category")
def delete_category(id:str):
    db_category = db.query(Category).filter(Category.id==id,Category.is_active==True,Category.is_deleted==False).first()
    if db_category is None:
        raise HTTPException(status_code=404,detail="category not found")
    db_category.is_active=False
    db_category.is_deleted =True
    db.commit()
    return {"message": "category deleted successfully"}