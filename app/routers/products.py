from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.post("/", response_model=schemas.ProductResponse, status_code=201)
async def create_product(product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    # Kategori kontrolü
    category = await db.get(models.Category, product.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")

    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[schemas.ProductResponse])
async def read_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Product))
    return result.scalars().all()

@router.get("/{product_id}", response_model=schemas.ProductResponse)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return product

@router.put("/{product_id}", response_model=schemas.ProductResponse)
async def update_product(product_id: int, product_update: schemas.ProductUpdate, db: AsyncSession = Depends(get_db)):
    product = await db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    update_data = product_update.model_dump(exclude_unset=True)
    
    # Kategori kontrolü eğer category_id güncelleniyorsa
    if "category_id" in update_data:
        category = await db.get(models.Category, update_data["category_id"])
        if not category:
            raise HTTPException(status_code=400, detail="Kategori bulunamadı")

    for key, value in update_data.items():
        setattr(product, key, value)
    
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    await db.delete(product)
    await db.commit()
    return None