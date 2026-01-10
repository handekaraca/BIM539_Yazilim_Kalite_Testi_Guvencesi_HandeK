from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/categories", tags=["Categories"])

@router.post("/", response_model=schemas.CategoryResponse, status_code=201)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    new_category = models.Category(name=category.name)
    db.add(new_category)
    try:
        await db.commit()
        await db.refresh(new_category)
        return new_category
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Kategori zaten mevcut olabilir.")

@router.get("/", response_model=List[schemas.CategoryResponse])
async def read_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Category))
    return result.scalars().all()

@router.get("/{category_id}", response_model=schemas.CategoryResponse)
async def read_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await db.get(models.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    return category

@router.put("/{category_id}", response_model=schemas.CategoryResponse)
async def update_category(category_id: int, category_update: schemas.CategoryUpdate, db: AsyncSession = Depends(get_db)):
    category = await db.get(models.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    
    update_data = category_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    
    db.add(category)
    try:
        await db.commit()
        await db.refresh(category)
        return category
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Kategori adı zaten mevcut")

@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await db.get(models.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")

    try:
        await db.delete(category)
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Kategori silinemedi (kullanımda olabilir)")
    return None