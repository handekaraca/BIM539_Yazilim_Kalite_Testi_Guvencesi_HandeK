# BIM539 Final Projesi - E-Ticaret API

![CI Status](https://github.com/handekaraca/BIM539_Yazilim_Kalite_Testi_Guvencesi_HandeK/actions/workflows/ci.yml/badge.svg)

Bu proje, **Yazılım Kalite Güvencesi ve Testi** dersi final projesi kapsamında geliştirilmiş bir RESTful API çalışmasıdır. Modern yazılım geliştirme standartlarına uygun olarak tasarlanmış, test odaklı geliştirme (TDD) süreçleri izlenmiş ve kapsamlı bir şekilde belgelenmiştir.

## Teknolojiler
*   **Programlama Dili**: Python 3.10+
*   **Web Çatısı**: FastAPI
*   **Veritabanı**: SQLite (AsyncIO destekli)
*   **ORM**: SQLAlchemy (Asenkron)
*   **Test Araçları**: Pytest, Asyncio, Httpx
*   **Sürekli Entegrasyon (CI)**: GitHub Actions

## Kurulum Talimatları

1.  **Sanal Ortamın Oluşturulması:**
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```

2.  **Bağımlılıkların Yüklenmesi:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Uygulamanın Başlatılması:**
    ```bash
    uvicorn app.main:app --reload
    ```
    API erişim adresi: `http://127.0.0.1:8000`

## Dokümantasyon

API dokümantasyonuna (OpenAPI/Swagger) aşağıdaki bağlantıdan erişilebilir:

*   **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
*   **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Temel Uç Noktalar (Endpoints)

| Metot | Yol | Açıklama |
| :--- | :--- | :--- |
| **Kimlik Doğrulama** | | |
| `POST` | `/token` | Kullanıcı girişi ve JWT token üretimi |
| **Kullanıcı İşlemleri** | | |
| `POST` | `/api/users/` | Yeni kullanıcı kaydı |
| `GET` | `/api/users/` | Kullanıcı listesi |
| **Ürün ve Kategori** | | |
| `POST` | `/api/products/` | Ürün ekleme |
| `GET` | `/api/products/` | Ürün listeleme |
| **Sipariş ve Değerlendirme** | | |
| `POST` | `/api/orders/{uid}` | Sipariş oluşturma |
| `POST` | `/api/reviews/{uid}` | Ürün değerlendirmesi ekleme |

## Test Süreçleri

Proje kapsamında **Birim (Unit)**, **Entegrasyon (Integration)** ve **Sistem/Uçtan Uca (E2E)** testleri gerçekleştirilmiştir.

Test çalıştırma komutu:
```bash
pytest
```

Kod kapsamı (Coverage) raporu oluşturma:
```bash
pytest --cov=app tests/
```

**Mevcut Test İstatistikleri:**
*   15+ Birim Test: İş mantığı ve veri doğrulama kontrolleri
*   10+ Entegrasyon Testi: API uç noktaları ve veritabanı etkileşimi
*   5 Sistem (E2E) Senaryosu: Kullanıcı akış testleri

## Sürekli Entegrasyon (CI/CD)
GitHub Actions yapılandırması (`ci.yml`) ile her kod gönderiminde (push/pull request) testler otomatik olarak çalıştırılmaktadır.

---
**Öğrenci**: Fatma Hande Karaça
**Ders**: Yazılım Kalite Güvencesi ve Testi
**Dönem**: 2025-2026 Güz Dönemi
