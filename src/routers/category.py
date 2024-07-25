from fastapi import FastAPI, HTTPException, APIRouter, Depends
from database.database import Sessionlocal
from src.schemas.category import Allcategories,Partialcategories
from src.models.category import Category
import uuid
from logs.log_config import logger
from typing import List

category = APIRouter(tags=["Category"])
db = Sessionlocal()



#____________________create_categories______________


@category.post("/create_categories", response_model=Allcategories)
def create_category(category: Allcategories):
    logger.info("Creating new category with name: ", category.name)
    new_category = Category(
        id=str(uuid.uuid4()),
        name=category.name,
        description=category.description,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    logger.info("Category created with id: %s", new_category.id)
    return new_category



#_________________get_category_________________


@category.get("/get_category", response_model=Allcategories)
def get_category(id: str):
    logger.info("Fetching category with id:", id)
    db_category = db.query(Category).filter(Category.id == id, Category.is_active == True, Category.is_deleted == False).first()
    if db_category is None:
        logger.error("Category not found with id:", id)
        raise HTTPException(status_code=404, detail="category not found")
    logger.info("Category fetched with id:", id)
    return db_category



#_________________get_all_category_______________


@category.get("/get_all_category", response_model=List[Allcategories])
def get_all_category():
    logger.info("Fetching all active and non-deleted categories")
    db_category = db.query(Category).filter(Category.is_active == True, Category.is_deleted == False).all()
    if not db_category:
        logger.error("No categories found")
        raise HTTPException(status_code=404, detail="category not found")
    logger.info("Fetched all categories")
    return db_category


#_____________update_category_by_patch__________________


@category.patch("/update_category_by_patch", response_model=Allcategories)
def update_category_patch(categorys: Partialcategories, id: str):
    logger.info("Updating category with id: ", id)
    db_category = db.query(Category).filter(Category.id == id, Category.is_active == True, Category.is_deleted == False).first()
    if db_category is None:
        logger.error("Category not found with id: ", id)
        raise HTTPException(status_code=404, detail="category not found")

    for field_name, value in categorys.dict().items():
        if value is not None:
            setattr(db_category, field_name, value)

    db.commit()
    db.refresh(db_category)
    logger.info("Category updated with id: ", id)
    return db_category


#____________delete_category_________________


@category.delete("/delete_category")
def delete_category(id: str):
    logger.info("Deleting category with id: ", id)
    db_category = db.query(Category).filter(Category.id == id, Category.is_active == True, Category.is_deleted == False).first()
    if db_category is None:
        logger.error("Category not found with id: ", id)
        raise HTTPException(status_code=404, detail="category not found")
    db_category.is_active = False
    db_category.is_deleted = True
    db.commit()
    logger.info("Category deleted with id: ", id)
    return {"message": "category deleted successfully"}