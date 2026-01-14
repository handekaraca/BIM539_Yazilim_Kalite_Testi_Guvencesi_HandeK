import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_urun_ekleme_entegrasyon(client: AsyncClient):
    # Kategori oluşturup içine ürün ekleme testi
    cat_resp = await client.post("/api/categories/", json={"name": "Kagit"})
    cat_id = cat_resp.json()["id"]

    response = await client.post("/api/products/", json={
        "name": "A4 Kagit",
        "price": 100.0,
        "category_id": cat_id
    })
    assert response.status_code == 201
    assert response.json()["name"] == "A4 Kagit"

@pytest.mark.asyncio
async def test_urun_bulunamadi_hatasi_entegrasyon(client: AsyncClient):
    # Olmayan bir ürünü çekmeye çalışınca 404 vermeli
    response = await client.get("/api/products/9999")
    assert response.status_code == 404
