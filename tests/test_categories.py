import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_kategori_ekle_oku_entegrasyon(client: AsyncClient):
    # Kategori ekleyip listeleme testi
    await client.post("/api/categories/", json={"name": "Elektronik"})
    response = await client.get("/api/categories/")
    assert response.status_code == 200
    assert any(c["name"] == "Elektronik" for c in response.json())

@pytest.mark.asyncio
async def test_kategori_guncelle_entegrasyon(client: AsyncClient):
    # Kategori ismini değiştirme testi
    resp = await client.post("/api/categories/", json={"name": "Eski Isim"})
    cid = resp.json()["id"]
    response = await client.put(f"/api/categories/{cid}", json={"name": "Yeni Isim"})
    assert response.status_code == 200
    assert response.json()["name"] == "Yeni Isim"
