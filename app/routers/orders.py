from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.post("/{user_id}", response_model=schemas.OrderResponse, status_code=201)
async def create_order(user_id: int, order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    user = await db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    new_order = models.Order(user_id=user_id, status=order.status)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

@router.get("/", response_model=List[schemas.OrderResponse])
async def read_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Order))
    return result.scalars().all()

@router.get("/{order_id}", response_model=schemas.OrderResponse)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await db.get(models.Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    return order

@router.put("/{order_id}", response_model=schemas.OrderResponse)
async def update_order(order_id: int, order_update: schemas.OrderUpdate, db: AsyncSession = Depends(get_db)):
    order = await db.get(models.Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    
    update_data = order_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)
    
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await db.get(models.Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    
    await db.delete(order)
    await db.commit()
    return None