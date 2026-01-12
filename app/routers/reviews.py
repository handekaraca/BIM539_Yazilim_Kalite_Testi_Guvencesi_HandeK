from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


@router.post("/{user_id}", response_model=schemas.ReviewResponse, status_code=201)
async def create_review(user_id: int, review: schemas.ReviewCreate, db: AsyncSession = Depends(get_db)):
    user = await db.get(models.User, user_id)
    product = await db.get(models.Product, review.product_id)

    if not user or not product:
        raise HTTPException(status_code=404, detail="Kullanıcı veya Ürün bulunamadı")

    new_review = models.Review(
        user_id=user_id,
        product_id=review.product_id,
        comment=review.comment,
        rating=review.rating
    )
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review


@router.get("/", response_model=List[schemas.ReviewResponse])
async def read_reviews(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Review))
    return result.scalars().all()

@router.get("/{review_id}", response_model=schemas.ReviewResponse)
async def read_review(review_id: int, db: AsyncSession = Depends(get_db)):
    review = await db.get(models.Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Değerlendirme bulunamadı")
    return review

@router.put("/{review_id}", response_model=schemas.ReviewResponse)
async def update_review(review_id: int, review_update: schemas.ReviewUpdate, db: AsyncSession = Depends(get_db)):
    review = await db.get(models.Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Değerlendirme bulunamadı")
    
    update_data = review_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)
    
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review

@router.delete("/{review_id}", status_code=204)
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db)):
    review = await db.get(models.Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Değerlendirme bulunamadı")
    
    await db.delete(review)
    await db.commit()
    return None