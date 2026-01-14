import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_kullanici_olusturma_entegrasyon(client: AsyncClient):
    # Başarılı kullanıcı oluşturma senaryosu (HTTP 201)
    response = await client.post("/api/users/", json={
        "username": "deneme_kullanici",
        "email": "deneme@test.com",
        "password": "sifre"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "deneme_kullanici"

@pytest.mark.asyncio
async def test_ayni_kullanici_hatasi_entegrasyon(client: AsyncClient):
    # Mükerrer kayıt girişimi kontrolü (HTTP 400)
    await client.post("/api/users/", json={
        "username": "user1",
        "email": "ayni@test.com",
        "password": "p"
    })
    response = await client.post("/api/users/", json={
        "username": "user2",
        "email": "ayni@test.com",
        "password": "p"
    })
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_kullanici_silme_entegrasyon(client: AsyncClient):
    # Kullanıcı silme işlemi ve doğrulama (HTTP 204)
    resp = await client.post("/api/users/", json={
        "username": "silinecek",
        "email": "sil@test.com",
        "password": "p"
    })
    uid = resp.json()["id"]
    
    del_resp = await client.delete(f"/api/users/{uid}")
    assert del_resp.status_code == 204
