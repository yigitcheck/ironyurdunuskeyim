---

# All Checker Tool

All Checker Tool, Steam hesaplarını kontrol etmek için geliştirilmiş bir Python aracıdır. Bu araç, kullanıcı adı ve şifre listesi verilen hesapların giriş yapıp yapamadığını, bakiye bilgilerini, envanterlerini, oyun kütüphanelerini, profil bilgilerini ve trade URL'lerini kontrol eder. Sonuçlar JSON, CSV ve PDF formatlarında kaydedilir.

---

## Özellikler

- **Çoklu Hesap Kontrolü**: Birden fazla hesabı aynı anda kontrol eder.
- **CAPTCHA Çözme**: 2Captcha API veya OCR ile CAPTCHA çözme desteği.
- **Proxy ve VPN Desteği**: Tor, VPN veya özel proxy kullanımı.
- **Detaylı Raporlama**: Sonuçları JSON, CSV ve PDF olarak kaydeder.
- **Ekran Görüntüsü Alma**: Her hesap için ekran görüntüsü alır.
- **Özet Rapor**: PDF raporunda tüm hesapların özetini sunar.

---

## Kurulum

### Gereksinimler

- Python 3.x
- Gerekli Python kütüphaneleri

### Adımlar

1. **Python'u İndirin ve Kurun**:
   - [Python Resmi Sitesi](https://www.python.org/downloads/)'nden Python'u indirin ve kurun.

2. **Kodu İndirin**:
   - Bu projeyi GitHub'dan indirin veya klonlayın:
     ```bash
     git clone https://github.com/İbrahimsql/steam-checker-tool.git
     cd steam-checker-tool
     ```

3. **Gerekli Kütüphaneleri Kurun**:
   - Terminalde aşağıdaki komutu çalıştırın:
     ```bash
     pip install -r requirements.txt
     ```

4. **2Captcha API Anahtarı** (Opsiyonel):
   - CAPTCHA çözme özelliği için [2Captcha](https://2captcha.com/) sitesinden bir API anahtarı alın.

---

## Kullanım

### Temel Kullanım

```bash
python steam_checker.py userlist.txt
```

Bu komut, `userlist.txt` dosyasındaki hesapları kontrol eder ve sonuçları `results.json`, `results.csv` ve `results.pdf` dosyalarına kaydeder.

### Tüm Özellikleri Kullanma

```bash
python steam_checker.py userlist.txt --threads 10 --proxy http://127.0.0.1:8080 --screenshot --inventory --games --wallet --profile --trade-url --output rapor
```

Bu komut, tüm özellikleri kullanır ve sonuçları `rapor.json`, `rapor.csv` ve `rapor.pdf` dosyalarına kaydeder.

---

### Parametreler

| Parametre             | Açıklama                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `userlist_file`       | Kullanıcı listesi dosyası (txt, csv veya json formatında).               |
| `--no-color`          | Renkli çıktıyı kapatır.                                                 |
| `--threads THREADS`   | Eşzamanlı iş parçacığı sayısı (varsayılan: 5).                          |
| `--proxy PROXY`       | Proxy adresi (örn: `http://127.0.0.1:8080`).                            |
| `--tor`               | Tor ağı kullanır.                                                       |
| `--vpn`               | VPN kullanır.                                                           |
| `--captcha-api-key`   | 2Captcha API anahtarını belirtir.                                       |
| `--output OUTPUT`     | Çıktı dosyası adı (varsayılan: `results`).                              |
| `--screenshot`        | Her hesap için ekran görüntüsü alır.                                    |
| `--inventory`         | Envanter bilgilerini kontrol eder.                                      |
| `--games`             | Kütüphanedeki oyunları listeler.                                        |
| `--wallet`            | Cüzdan bakiyesini kontrol eder.                                         |
| `--profile`           | Profil bilgilerini çeker.                                               |
| `--trade-url`         | Trade URL'sini alır.                                                    |

---

## Örnek Kullanıcı Listesi

### `userlist.txt` Örneği

```
user1:password1
user2:password2
user3:password3
```

---

## Çıktılar

### `results.json` Örneği

```json
[
    {
        "username": "user1",
        "balance": "50.00 TL",
        "inventory_count": 10,
        "games": 25,
        "profile_name": "User1",
        "trade_url": "https://steamcommunity.com/tradeoffer/new/?partner=123456"
    },
    {
        "username": "user2",
        "balance": "0.00 TL",
        "inventory_count": 0,
        "games": 0,
        "profile_name": "Unknown",
        "trade_url": null
    }
]
```

### `results.csv` Örneği

```
username,balance,inventory_count,games,profile_name,trade_url
user1,50.00 TL,10,25,User1,https://steamcommunity.com/tradeoffer/new/?partner=123456
user2,0.00 TL,0,0,Unknown,
```

### `results.pdf` Örneği

PDF raporu, tüm hesapların bilgilerini içeren bir özet sunar. Örnek çıktı:

```
Steam Hesap Kontrol Raporu - İbrahimsql

Kullanıcı: user1 - Bakiye: 50.00 TL
Envanter: 10 öğe - Oyunlar: 25
Profil: User1 - Trade URL: https://steamcommunity.com/tradeoffer/new/?partner=123456

Kullanıcı: user2 - Bakiye: 0.00 TL
Envanter: 0 öğe - Oyunlar: 0
Profil: Unknown - Trade URL: 
```

---

## Katkıda Bulunma

Bu projeye katkıda bulunmak isterseniz, lütfen bir **Pull Request** gönderin. Her türlü katkı ve öneri memnuniyetle karşılanır!

---

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

## İletişim

- **Geliştirici**: İbrahimsql
- **E-posta**: ibrahimsql@proton.me
- **GitHub**: [İbrahimsql](https://github.com/İbrahimsql)

---

