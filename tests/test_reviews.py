import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_yorum_yapma_entegrasyon(client: AsyncClient):
    # Kullanıcı ve ürün oluşturup yorum yapma testi
    u = await client.post("/api/users/", json={"username": "y1", "email": "y1@t.com", "password": "p"})
    c = await client.post("/api/categories/", json={"name": "YorumCat"})
    # Bu testte her şeyi sıfırdan oluşturuyoruz (isolation)
    p = await client.post("/api/products/", json={"name": "YorumP", "price": 10, "category_id": c.json()["id"]})
    
    response = await client.post(f"/api/reviews/{u.json()['id']}", json={
        "product_id": p.json()["id"],
        "comment": "Bence guzel",
        "rating": 4
    })
    assert response.status_code == 201
    assert response.json()["comment"] == "Bence guzel"

@pytest.mark.asyncio
async def test_yorum_listeleme_entegrasyon(client: AsyncClient):
    # Kayıtlı yorumları çekme testi
    response = await client.get("/api/reviews/")
    assert response.status_code == 200
