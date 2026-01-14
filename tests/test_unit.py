import pytest
from app import utils, schemas
from pydantic import ValidationError

# --- Yardımcı Fonksiyon Testleri ---

def test_sifre_hashleme_unit():
    # Şifre hashleme ve doğrulama testi
    sifre = "ders_projesi_123"
    hashli = utils.hash_password(sifre)
    assert hashli != sifre
    assert utils.verify_password(sifre, hashli) is True

def test_yanlis_sifre_unit():
    # Yanlış şifre girildiğinde hata vermeli
    hashli = utils.hash_password("dogru_sifre")
    assert utils.verify_password("yanlis_sifre", hashli) is False

# --- Veri Doğrulama (Schema) Testleri ---

def test_kullanici_sema_dogru_unit():
    data = {"username": "fatma_hande", "email": "hande@example.com", "password": "123"}
    user = schemas.UserCreate(**data)
    assert user.username == "fatma_hande"

def test_kullanici_sema_gecersiz_email_unit():
    # Geçersiz email formatı hatası kontrolü
    with pytest.raises(ValidationError):
        schemas.UserCreate(username="test", email="gecersiz-email", password="123")

def test_urun_sema_fiyat_unit():
    prod = schemas.ProductCreate(name="Defter", price=25.0, category_id=1)
    assert prod.price == 25.0

def test_kategori_sema_isim_unit():
    cat = schemas.CategoryCreate(name="Kırtasiye")
    assert cat.name == "Kırtasiye"

def test_siparis_varsayilan_durum_unit():
    # Sipariş durumu belirtilmezse pending olmalı
    order = schemas.OrderCreate()
    assert order.status == "pending"

def test_yorum_sema_puan_unit():
    review = schemas.ReviewCreate(product_id=1, comment="Gayet iyi", rating=5)
    assert review.rating == 5

# --- Diğer Mantıksal Testler ---

def test_kullanici_guncelleme_sema_unit():
    update = schemas.UserUpdate(username="yeni_isim")
    assert update.username == "yeni_isim"

def test_urun_guncelleme_fiyat_unit():
    update = schemas.ProductUpdate(price=99.9)
    assert update.price == 99.9

def test_kategori_guncelleme_unit():
    update = schemas.CategoryUpdate(name="Elektronik")
    assert update.name == "Elektronik"

def test_siparis_guncelleme_durum_unit():
    update = schemas.OrderUpdate(status="tamamlandi")
    assert update.status == "tamamlandi"

def test_yorum_guncelleme_unit():
    update = schemas.ReviewUpdate(comment="Fikrim değişti")
    assert update.comment == "Fikrim değişti"

def test_bos_string_temizleme_unit():
    # Girdi temizleme simülasyonu
    metin = "  deneme  "
    assert metin.strip() == "deneme"

def test_email_ayristirma_unit():
    # Email parçalama mantığı
    email = "deneme@test.com"
    parcalar = email.split("@")
    assert parcalar[0] == "deneme"
    assert parcalar[1] == "test.com"

def test_fiyat_yuvarlama_sim_unit():
    # Basit matematiksel util testi
    fiyat = 10.556
    assert round(fiyat, 2) == 10.56
