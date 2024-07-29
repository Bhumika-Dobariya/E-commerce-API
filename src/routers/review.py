from fastapi import FastAPI, HTTPException, APIRouter
from database.database import Sessionlocal
from src.schemas.review import ProductReviewCreate,ProductReviewUpdate
from src.models.review import ProductReview
import uuid
from sqlalchemy import func
from logs.log_config import logger
from typing import List

Reviews = APIRouter(tags=["user rating and review"])
db = Sessionlocal()


# ____________Create review_______________

@Reviews.post("/create_reviews", response_model=ProductReviewCreate)
def create_review(review: ProductReviewCreate):
    logger.info("Creating a new product review")
    
    customer_review = ProductReview(
        id=str(uuid.uuid4()),
        user_id=review.user_id,
        product_id=review.product_id,
        comment=review.comment,
        rating=review.rating
    )
    
    db.add(customer_review)
    db.commit()
    
    logger.info(f"Product review created successfully with ID: {customer_review.id}")
    
    return customer_review



# _______________Read review__________________


@Reviews.get("/read_reviews", response_model=ProductReviewCreate)
def read_review(id: str):
    logger.info(f"Fetching review with ID: {id}")
    
    review = db.query(ProductReview).filter(ProductReview.id == id).first()
    
    if review is None:
        logger.warning(f"Review not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Review not found")
    
    logger.info(f"Review fetched successfully with ID: {id}")
    
    return review


# ________________Get all reviews______________

@Reviews.get("/get_all_review", response_model=List[ProductReviewCreate])
def get_all_review():
    logger.info("Fetching all active and non-deleted reviews")
    
    db_reviews = db.query(ProductReview).filter(ProductReview.is_active == True, ProductReview.is_deleted == False).all()
    
    if not db_reviews:
        logger.warning("No active and non-deleted reviews found")
        raise HTTPException(status_code=404, detail="Reviews not found")
    
    logger.info("All reviews fetched successfully")
    
    return db_reviews



# ________________Update review___________________

@Reviews.patch("/update_review", response_model=ProductReviewCreate)
def update_review(Reviews: ProductReviewUpdate, id: str):
    logger.info(f"Updating review with ID: {id}")
    
    db_review = db.query(ProductReview).filter(ProductReview.id == id, ProductReview.is_active == True, ProductReview.is_deleted == False).first()
    
    if db_review is None:
        logger.warning(f"Review not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Review not found")
    
    for field_name, value in Reviews.dict().items():
        if value is not None:
            setattr(db_review, field_name, value)
    
    db.commit()
    
    logger.info(f"Review updated successfully with ID: {id}")
    
    return db_review



# ___________Delete review______________

@Reviews.delete("/delete_review")
def delete_review(id: str):
    logger.info(f"Deleting review with ID: {id}")
    
    db_review = db.query(ProductReview).filter(ProductReview.id == id, ProductReview.is_active == True, ProductReview.is_deleted == False).first()
    
    if db_review is None:
        logger.warning(f"Review not found with ID: {id}")
        raise HTTPException(status_code=404, detail="Review not found")
    
    db_review.is_active = False
    db_review.is_deleted = True
    db.commit()
    
    logger.info(f"Review deleted successfully with ID: {id}")
    
    return {"message": "Review deleted successfully"}



# _____________Count all reviews________________

@Reviews.get("/reviews_count")
def count_reviews():
    logger.info("Counting all active and non-deleted reviews")
    
    total_reviews = db.query(ProductReview).filter(ProductReview.is_active == True, ProductReview.is_deleted == False).count()
    
    logger.info(f"Total reviews count: {total_reviews}")
    
    return total_reviews



# _____________Count reviews for a product_______________

@Reviews.get("/count_reviews_of_product")
def count_reviews(product_id: str):
    logger.info(f"Counting reviews for product with ID: {product_id}")
    
    product_reviews_count = db.query(ProductReview).filter(ProductReview.product_id == product_id, ProductReview.is_active == True, ProductReview.is_deleted == False).count()
    
    if product_reviews_count == 0:
        logger.warning(f"No reviews found for product with ID: {product_id}")
        raise HTTPException(status_code=404, detail="No reviews found for this product")
    
    logger.info(f"Reviews count for product with ID: {product_id}: {product_reviews_count}")
    
    return {"product_id": product_id, "review_count": product_reviews_count}

# Average rating
def get_qualitative_rating(avg_rating: float):
    if avg_rating >= 4.5:
        return "Excellent"
    elif avg_rating >= 4.0:
        return "Very Good"
    elif avg_rating >= 3.0:
        return "Good"
    elif avg_rating >= 2.0:
        return "Average"
    else:
        return "Poor"
    
    
    
#__________________average_rating______________

@Reviews.get("/average_rating")
def average_rating(product_id: str):
    logger.info(f"Calculating average rating for product with ID: {product_id}")
    
    average_rating = db.query(func.avg(ProductReview.rating)).filter(ProductReview.product_id == product_id).scalar()
    
    if average_rating is None:
        logger.warning(f"No reviews found for product with ID: {product_id}")
        raise HTTPException(status_code=404, detail="No reviews found for the product")
    
    avg_rating = round(float(average_rating), 2)
    qualitative_rating = get_qualitative_rating(avg_rating)
    
    logger.info(f"Average rating for product with ID: {product_id} is {avg_rating} ({qualitative_rating})")
    
    return {
        "product_id": product_id,
        "average_rating": avg_rating,
        "qualitative_rating": qualitative_rating
    }