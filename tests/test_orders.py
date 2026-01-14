import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_siparis_olusturma_entegrasyon(client: AsyncClient):
    # Kullanıcı oluşturup ona sipariş atama testi
    user_resp = await client.post("/api/users/", json={"username": "siparisci", "email": "s@test.com", "password": "p"})
    uid = user_resp.json()["id"]

    response = await client.post(f"/api/orders/{uid}", json={"status": "hazirlaniyor"})
    assert response.status_code == 201
    assert response.json()["status"] == "hazirlaniyor"

@pytest.mark.asyncio
async def test_siparis_silme_entegrasyon(client: AsyncClient):
    # Sipariş silme testi
    user_resp = await client.post("/api/users/", json={"username": "s2", "email": "s2@test.com", "password": "p"})
    uid = user_resp.json()["id"]
    ord_resp = await client.post(f"/api/orders/{uid}", json={"status": "iptal"})
    oid = ord_resp.json()["id"]
    
    response = await client.delete(f"/api/orders/{oid}")
    assert response.status_code == 204
