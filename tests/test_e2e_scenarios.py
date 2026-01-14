import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.asyncio
@pytest.mark.asyncio
async def test_e2e_shopping_flow(client: AsyncClient):
    # 1. Adım: Kullanıcı Kaydı
    u_resp = await client.post("/api/users/", json={"username": "shopuser", "email": "shop@ex.com", "password": "pass"})
    assert u_resp.status_code == 201
    user_id = u_resp.json()["id"]

    # 2. Adım: Kimlik Doğrulama ve Token Alımı
    login_resp = await client.post("/token", data={"username": "shopuser", "password": "pass"})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Adım: Kategori ve Ürün Tanımlama (Test verisi hazırlığı)
    c_resp = await client.post("/api/categories/", json={"name": "ShopCat"})
    cat_id = c_resp.json()["id"]
    p_resp = await client.post("/api/products/", json={"name": "Item1", "price": 100, "category_id": cat_id})
    prod_id = p_resp.json()["id"]

    # 4. Adım: Sipariş Oluşturma İsteği
    o_resp = await client.post(f"/api/orders/{user_id}", json={"status": "pending"})
    assert o_resp.status_code == 201
    order_id = o_resp.json()["id"]

    # 5. Adım: Sipariş Durumunun Doğrulanması
    get_o = await client.get(f"/api/orders/{order_id}")
    assert get_o.json()["status"] == "pending"

@pytest.mark.asyncio
async def test_e2e_review_cycle(client: AsyncClient):
    u_resp = await client.post("/api/users/", json={"username": "revuser", "email": "rev@ex.com", "password": "pass"})
    uid = u_resp.json()["id"]
    c_resp = await client.post("/api/categories/", json={"name": "RevCat"})
    cid = c_resp.json()["id"]
    p_resp = await client.post("/api/products/", json={"name": "RevItem", "price": 50, "category_id": cid})
    pid = p_resp.json()["id"]

    r_resp = await client.post(f"/api/reviews/{uid}", json={"product_id": pid, "comment": "Nice", "rating": 5})
    assert r_resp.status_code == 201
    rid = r_resp.json()["id"]

    get_r = await client.get(f"/api/reviews/{rid}")
    assert get_r.json()["comment"] == "Nice"

@pytest.mark.asyncio
async def test_e2e_product_management(client: AsyncClient):
    c_resp = await client.post("/api/categories/", json={"name": "MgmtCat"})
    cid = c_resp.json()["id"]

    p_resp = await client.post("/api/products/", json={"name": "OldProd", "price": 10, "category_id": cid})
    pid = p_resp.json()["id"]

    u_resp = await client.put(f"/api/products/{pid}", json={"name": "NewProd", "price": 20})
    assert u_resp.status_code == 200
    assert u_resp.json()["name"] == "NewProd"

    d_resp = await client.delete(f"/api/products/{pid}")
    assert d_resp.status_code == 204

    get_p = await client.get(f"/api/products/{pid}")
    assert get_p.status_code == 404

@pytest.mark.asyncio
async def test_e2e_user_lifecycle(client: AsyncClient):
    reg = await client.post("/api/users/", json={"username": "lifeuser", "email": "life@ex.com", "password": "123"})
    uid = reg.json()["id"]

    upd = await client.put(f"/api/users/{uid}", json={"email": "newlife@ex.com"})
    assert upd.status_code == 200
    assert upd.json()["email"] == "newlife@ex.com"

    dup = await client.post("/api/users/", json={"username": "other", "email": "newlife@ex.com", "password": "123"})
    assert dup.status_code == 400

@pytest.mark.asyncio
async def test_e2e_order_workflow(client: AsyncClient):
    u_resp = await client.post("/api/users/", json={"username": "ordflow", "email": "ordflow@ex.com", "password": "p"})
    uid = u_resp.json()["id"]

    o_resp = await client.post(f"/api/orders/{uid}", json={"status": "created"})
    oid = o_resp.json()["id"]

    s1 = await client.put(f"/api/orders/{oid}", json={"status": "processing"})
    assert s1.json()["status"] == "processing"

    s2 = await client.put(f"/api/orders/{oid}", json={"status": "shipped"})
    assert s2.json()["status"] == "shipped"

    dele = await client.delete(f"/api/orders/{oid}")
    assert dele.status_code == 204
