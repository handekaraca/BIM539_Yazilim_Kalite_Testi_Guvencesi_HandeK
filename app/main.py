from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine, Base
from .routers import users, products, categories, orders, reviews, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Veritabanı tablolarının oluşturulması
    yield
    # Uygulama kapatma işlemleri

app = FastAPI(
    title="BIM539 Final Projesi API",
    description="Yazılım Kalite Güvencesi ve Testi Dersi Projesi",
    version="1.0.0",
    lifespan=lifespan
)

# Yönlendiricilerin (Routers) sisteme dahil edilmesi
app.include_router(users.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(orders.router)
app.include_router(reviews.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    """Kök dizin erişim kontrolü."""
    return {"message": "API Aktif Durumda"}



