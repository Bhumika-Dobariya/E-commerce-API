from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.schemas.review import ProductReviewCreate,ProductReviewUpdate,ProductStar
from src.models.review import ProductReview
import uuid

Reviews = APIRouter(tags=["user rating and review"])
db = Sessionlocal()


#create review

@Reviews.post("/create_reviews", response_model=ProductReviewCreate)
def create_review(review: ProductReviewCreate):
    customer_review = ProductReview(
        id=str(uuid.uuid4()), 
        user_id = review.user_id,
        product_id=review.product_id,  
        description=review.description,
        stars=review.stars
    )
    db.add(customer_review) 
    db.commit() 
    return customer_review




#read review

@Reviews.get("/read_reviews", response_model=ProductReviewCreate)
def read_review(id: str):
    review = db.query(ProductReview).filter(ProductReview.id == id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review



#get all review

@Reviews.get("/get_all_review",response_model=list[ProductReviewCreate])
def get_all_review():
    db_reviews = db.query(ProductReview).filter(ProductReview.is_active==True,ProductReview.is_deleted==False).all()
    if db_reviews is None:
        raise HTTPException(status_code=404,detail ="review not found")
    return db_reviews



#update review

@Reviews.patch("/update_review", response_model=ProductReviewCreate)
def update_review(Reviews: ProductReviewUpdate,id:str):
    
    db_review = db.query(ProductReview).filter(ProductReview.id == id, ProductReview.is_active,ProductReview.is_deleted==False).first()

    if  db_review  is None:
        raise HTTPException(status_code=404, detail="product not found")

    for field_name, value in Reviews.dict().items():
        if value is not None:
            setattr( db_review , field_name, value)

    db.commit()
    return  db_review 



#delete review

@Reviews.delete("/delete_review")
def delete_review(id:str):
    db_review = db.query(ProductReview).filter(ProductReview.id==id,ProductReview.is_active==True,ProductReview.is_deleted==False).first()
    if db_review is None:
        raise HTTPException(status_code=404,detail="review not found")
    db_review.is_active=False
    db_review.is_deleted =True
    db.commit()
    return {"message": "review deleted successfully"}



#count all review

@Reviews.get("/reviews_count")
def count_reviews():
    total_reviews = db.query(ProductReview).filter(ProductReview.is_active == True, ProductReview.is_deleted == False).count()
    return total_reviews


"""@Reviews.get("/count_reviews_of_product")
def count_reviews(product_id:str):
    product_reviews = db.query(ProductReview).filter(ProductReview.id==product_id,ProductReview.is_active == True, ProductReview.is_deleted == False).count()
    if product_reviews is None:
            raise HTTPException(status_code=404, detail="No reviews found for this product")
    return  {"product_id": product_id, "review_count": product_reviews}"""