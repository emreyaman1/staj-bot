# 📧 E-posta Otomasyon Botu v3.3

Organize Sanayi Bölgeleri (OSB) ve firmalardan otomatik e-posta toplayıp, toplu mail gönderme programı.

## ✨ Özellikler

### 🔍 Akıllı Tarama
- **Çoklu Site Tarama**: Birden fazla siteyi aynı anda tara
- **Derin Tarama Modu**: Firma detay sayfalarına otomatik girerek mail topla
- **3 Tarayıcı Desteği**: Chrome, Edge, Firefox (otomatik tespit)
- **Selenium & Requests**: Hem dinamik hem statik siteler için optimize

### 📧 E-posta Yönetimi
- **Gmail Entegrasyonu**: Gmail üzerinden toplu mail gönderimi
- **PDF Eki**: CV veya diğer belgeleri otomatik ekle
- **Akıllı Tekrar Gönderim**: Belirlediğiniz gün sayısına göre otomatik kontrol
- **Gönderim Takibi**: Hangi maillere ne zaman gönderildi takip et

### 🛡️ Güvenlik & Filtreleme
- **Gelişmiş Email Validation**: Dosya uzantılarını otomatik filtrele (png, jpg, pdf, vb.)
- **Veritabanı**: SQLite ile tüm mailleri ve gönderim geçmişini kaydet
- **Yedekleme**: E-posta listesini Excel'e aktar

### 🎨 Kullanıcı Dostu Arayüz
- **Modern GUI**: Tkinter ile hazırlanmış kullanımı kolay arayüz
- **Anlık Bildirimler**: Tarama ve gönderim durumunu canlı takip et
- **Otomatik Kayıt**: Ayarlarınız otomatik kaydedilir

## 📋 Gereksinimler

### Python 3.7+
Program gerekli kütüphaneleri otomatik yükler:
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP istekleri
- `lxml` - XML/HTML parsing
- `openpyxl` - Excel dosyaları
- `selenium` - Web otomasyonu

### Tarayıcı
En az birini yüklü olmalı:
- Microsoft Edge (Önerilen - Windows'ta varsayılan)
- Google Chrome
- Mozilla Firefox

## 🚀 Kurulum

### 1. Python Kurulumu
[Python 3.7+](https://www.python.org/downloads/) indirip yükleyin.

### 2. Projeyi İndir
```bash
git clone https://github.com/KULLANICI_ADINIZ/email-bot.git
cd email-bot
```

### 3. Programı Çalıştır
```bash
python email_bot.py
```

Program ilk çalıştırmada gerekli kütüphaneleri otomatik yükleyecektir.

## 📖 Kullanım

### 1️⃣ Ayarları Yapılandır

#### Gmail Bilgileri
1. Gmail adresinizi girin
2. **Uygulama Şifresi** oluşturun:
   - Google Hesabı → Güvenlik
   - 2 Adımlı Doğrulama'yı açın
   - Uygulama şifreleri → Mail için şifre oluştur
   - Oluşturulan 16 haneli şifreyi girin

#### PDF Seç
- CV veya gönderilecek belgeyi seçin

#### Mail Metni
- Gönderilecek mesajı yazın

### 2️⃣ Site Ekle (URL Yönetimi)
1. "URL Yönetimi" sekmesine git
2. "Yeni URL Ekle" butonuna tıkla
3. Site adı ve URL'sini gir
4. Eklenecek siteyi işaretle

**Varsayılan Siteler:**
- İstanbul Anadolu Yakası OSB
- Manisa OSB

### 3️⃣ Tarama Ayarları

#### Derin Tarama
Firma detay sayfalarına otomatik girer ve mail toplar:
- ✅ **Derin Tarama**: Açık
- **Maksimum Sayfa**: 100-150 (önerilen)

**Not:** Derin tarama uzun sürer (30-60 dakika), ancak çok daha fazla mail toplar!

#### Normal Tarama
Sadece ana sayfadaki mailleri toplar:
- ❌ **Derin Tarama**: Kapalı

### 4️⃣ Taramayı Başlat
1. Taranacak siteleri seçin
2. "Taramayı Başlat" butonuna tıklayın
3. İşlemin tamamlanmasını bekleyin

### 5️⃣ Mail Gönder
1. Toplanan mailleri kontrol edin
2. "Mail Gönder" butonuna tıklayın
3. Gönderim tamamlanana kadar bekleyin

## 🎯 İpuçları

### Maksimum Verim İçin
- **Derin Tarama**: Mutlaka açın (10-20x daha fazla mail)
- **Tarayıcı**: "Auto" bırakın, program en iyi olanı seçecek
- **Tarayıcıyı Göster**: Kapalı tutun (daha hızlı)
- **Maksimum Sayfa**: 150 yapın (tüm firmaları tara)

### Mail Gönderirken
- **Gmail Limiti**: Günde maksimum 500 mail (Gmail kuralı)
- **Bekleme Süresi**: Her mail arası 2 saniye (spam önleme)
- **Test Edin**: İlk başta kendinize test maili gönderin

### Sorun Giderme
- **"Tarayıcı bulunamadı"**: Edge, Chrome veya Firefox yükleyin
- **"Gmail bağlanamadı"**: Uygulama şifresi kullandığınızdan emin olun
- **"Selenium hatası"**: Driver'lar otomatik indirilir, internet bağlantınızı kontrol edin

## 📁 Dosya Yapısı

```
email-bot/
│
├── email_bot.py              # Ana program
├── settings.json             # Ayarlar (otomatik oluşur)
├── saved_urls.json           # Kayıtlı siteler (otomatik oluşur)
├── email_bot.db              # Veritabanı (otomatik oluşur)
├── README.md                 # Bu dosya
└── .gitignore                # Git ignore dosyası
```

## 🔒 Gizlilik

**DİKKAT:** Kişisel bilgileriniz sadece yerel bilgisayarınızda saklanır!

- ✅ Gmail şifreniz şifrelenmemiş saklanır → `.gitignore` ile korunur
- ✅ Toplanan e-postalar yerel veritabanında
- ✅ Gönderim geçmişi sadece sizde

### GitHub'a Yüklemeden Önce
`.gitignore` dosyası şu dosyaları otomatik hariç tutar:
- `settings.json` (Gmail şifreniz)
- `email_bot.db` (toplanan mailler)
- `*.log` (log dosyaları)

## 🛠️ İleri Düzey

### Özel Site Eklemek
Farklı OSB sitelerinden mail toplamak için:

1. Sitenin firma listesi sayfasını bul
2. Bir firmaya tıkla ve URL yapısına bak
3. URL pattern'ini belirle (örn: `/works/`, `/firmalar/`, `/companies/`)

**Kod Düzenleme (İleri Seviye):**
```python
# email_bot.py - Satır 2088 ve 2131
# Mevcut:
if '/works/' in href:  # İAYOSB için

# Yeni site için:
if '/firmalar/' in href:  # Manisa OSB için
```

### Otomatik Tarama
Program her 30 dakikada bir otomatik tarama yapabilir:
1. "Otomatik Tarama" butonuna tıkla
2. Program arka planda çalışır
3. Yeni mailler otomatik eklenir

## 📊 İstatistikler

### İAYOSB.com Test Sonuçları
- **Toplam Firma**: 137
- **Bulunan Mail**: 120+ email adresi
- **Tarama Süresi**: ~45 dakika (derin tarama)
- **Başarı Oranı**: %95+

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add some amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## ⚠️ Yasal Uyarı

Bu program sadece **yasal ve etik kullanım** için tasarlanmıştır:

- ✅ İş başvurusu yapmak için
- ✅ Ticari teklifler göndermek için (uygun şirketlere)
- ✅ İzinli pazarlama için

- ❌ Spam göndermek için kullanmayın
- ❌ KVKK/GDPR kurallarına uymayan kullanım
- ❌ İzinsiz kişisel veri toplama

**Kullanıcı sorumluluğundadır!**

## 📞 Destek

Sorun mu yaşıyorsunuz? 
yemreyaman1@gmail.com

## 🙏 Teşekkürler

Bu programı kullandığınız için teşekkürler!

⭐ Beğendiyseniz yıldız vermeyi unutmayın!

---

**Yapımcı:** Yunus Emre Yaman  
**Versiyon:** 3.3  
**Son Güncelleme:** 2026-02-14
