# 📘 E-posta Bot - Detaylı Kullanım Kılavuzu

## 🎯 İçindekiler
1. [İlk Kurulum](#-ilk-kurulum)
2. [Gmail Ayarları](#-gmail-ayarları)
3. [Site Ekleme ve Yönetim](#-site-ekleme-ve-yönetim)
4. [Tarama İşlemleri](#-tarama-i̇şlemleri)
5. [Mail Gönderimi](#-mail-gönderimi)
6. [Sorun Giderme](#-sorun-giderme)

---

## 🚀 İlk Kurulum

### Adım 1: Python Kurulumu
1. [Python.org](https://www.python.org/downloads/) adresinden Python 3.7+ indirin
2. Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin
3. Kurulumu tamamlayın

### Adım 2: Programı İndirin
```bash
# GitHub'dan indirin
git clone https://github.com/emreyaman1/email-bot.git

# veya ZIP olarak indirip çıkartın
```

### Adım 3: Programı Başlatın
```bash
RUN.bat dosyasını çalıştırın
```

**İlk çalıştırmada:**
- Program gerekli kütüphaneleri otomatik yükler
- 1-2 dakika sürebilir
- İnternet bağlantısı gereklidir

---

## 📧 Gmail Ayarları

### Neden Uygulama Şifresi?

Gmail, güvenlik için normal şifrenizle dış uygulamalara giriş izni vermez. Uygulama şifresi oluşturmanız gerekir.

### Uygulama Şifresi Oluşturma

#### Adım 1: Google Hesabına Git
1. [myaccount.google.com](https://myaccount.google.com) adresine gidin
2. Sol menüden **"Güvenlik"** seçin

#### Adım 2: 2 Adımlı Doğrulamayı Aç
1. **"2 Adımlı Doğrulama"** bölümüne tıklayın
2. Eğer kapalıysa açın (telefon numarası gerekir)
3. Doğrulama işlemini tamamlayın

#### Adım 3: Uygulama Şifresi Oluştur
1. 2 Adımlı Doğrulama açıldıktan sonra sayfayı yenileyin
2. **"Uygulama şifreleri"** bölümünü bulun
3. Tıklayın ve yeni şifre oluşturun:
   - Uygulama: **"Mail"** seçin
   - Cihaz: **"Windows Bilgisayar"** seçin (veya uygun olanı)
4. **"Oluştur"** butonuna tıklayın

#### Adım 4: Şifreyi Kopyalayın
- Ekranda 16 haneli bir şifre görünecek
- Örnek: `abcd efgh ijkl mnop`
- Bu şifreyi kopyalayın (bir daha gösterilmeyecek!)

#### Adım 5: Programa Girin
1. Email Bot programını açın
2. **"Gmail Adresi"**: normal gmail adresinizi girin
3. **"Gmail Şifresi"**: kopyaladığınız 16 haneli şifreyi girin
4. **"Gmail'i Test Et"** butonuna tıklayın
5. ✅ "Gmail çalışıyor!" mesajını görmelisiniz

**Sorun mu yaşıyorsunuz?**
- Şifrede boşluk olmamalı: `abcdefghijklmnop`
- Normal şifrenizi değil, uygulama şifresini kullanın
- 2 Adımlı Doğrulama açık olmalı

---

## 🔗 Site Ekleme ve Yönetim

### Mevcut Siteler

Program varsayılan olarak 2 site ile gelir:
- ✅ İstanbul Anadolu Yakası OSB
- ✅ Manisa OSB

### Yeni Site Ekleme

#### Adım 1: URL Yönetimi Sekmesi
1. Programda **"URL Yönetimi"** sekmesine tıklayın
2. **"Yeni URL Ekle"** butonuna tıklayın

#### Adım 2: Bilgileri Girin
Açılan pencerede:
- **Site Adı**: Kolayca hatırlayabileceğiniz bir isim
  - Örnek: "Kocaeli OSB"
- **Site URL'si**: Firma listesi sayfasının tam adresi
  - Örnek: `https://www.kocaeliosb.com.tr/firmalar/`

#### Adım 3: Kaydet
- **"Ekle"** butonuna tıklayın
- Site listeye eklenecektir

### Site Silme
1. Silmek istediğiniz siteyi seçin
2. **"Seçili URL'yi Sil"** butonuna tıklayın
3. Onaylayın

### Site Seçme (Tarama İçin)
- Listedeki sitelerin yanındaki **checkbox**'ları işaretleyin
- Birden fazla site seçebilirsiniz
- Sadece işaretli siteler taranacaktır

---

## 🔍 Tarama İşlemleri

### Normal Tarama vs Derin Tarama

#### Normal Tarama ❌ Derin Tarama Kapalı
- Sadece firma listesi sayfasını tarar
- Hızlıdır (1-2 dakika)
- Az mail bulur (5-10 mail)
- **Önerilmez!**

#### Derin Tarama ✅ Derin Tarama Açık (ÖNERİLİR)
- Firma listesi sayfasını tarar
- **Her firma detay sayfasına girer**
- Email adreslerini toplar
- Daha yavaştır (30-60 dakika)
- ÇOK daha fazla mail bulur (100+ mail)
- **MUTLAKA KULLANIN!**

### Tarama Ayarları

#### Derin Tarama Ayarı
1. **"Ayarlar"** sekmesine gidin
2. ✅ **"Derin Tarama"** seçeneğini işaretleyin
3. **"Maksimum Sayfa"**: `150` yazın
   - Bu kadar firma sayfası taranacak
   - 100-200 arası ideal

#### Selenium Ayarları
- ✅ **"Selenium Kullan"**: Açık (önerilen)
- **"Tarayıcı Seçimi"**: Auto (otomatik)
- ❌ **"Tarayıcıyı Göster"**: Kapalı (daha hızlı)

### Taramayı Başlatma

#### Adım 1: Siteleri Seç
1. **"URL Yönetimi"** sekmesinde
2. Taranacak siteleri işaretleyin

#### Adım 2: Başlat
1. **"Tarama"** sekmesine gidin
2. **"Taramayı Başlat"** butonuna tıklayın
3. Uyarı mesajını okuyun ve onaylayın

#### Adım 3: Bekleyin
- **İşlem uzun sürecek** uyarısı göreceksiniz
- Tahmini süre gösterilir (örn: 45 dakika)
- Program otomatik çalışacaktır

### Tarama Sırasında

#### Ne Oluyor?
```
[1/150] 🔍 https://www.iayosb.com/firmalarimiz/
   📜 AGRESİF SCROLL başlatılıyor...
   🔗 LİNK TOPLAMA başlatılıyor...
   ✅ 137 firma bulundu!

[2/150] 🔍 https://www.iayosb.com/works/galvabor-...
   📧 galvabor@galvabor.com

[3/150] 🔍 https://www.iayosb.com/works/festo-...
   📧 info@festo.com.tr
```

#### Durum Ekranı
- **Üst Kısım**: Anlık durum (hangi sayfa taranıyor)
- **Log Ekranı**: Detaylı bilgiler
- **Sayaç**: Kaç mail bulundu

#### Durdurma
- **"Taramayı Durdur"** butonuna tıklayın
- Bulunan mailler kaydedilir

---

## 📤 Mail Gönderimi

### Hazırlık

#### 1. PDF Seç
- **"Mail Ayarları"** sekmesinde
- **"PDF Seç"** butonuna tıklayın
- CV veya gönderilecek dosyayı seçin

#### 2. Mail Metni Yaz
Aşağıdaki metin editörüne mesajınızı yazın:
```
Merhaba,

Ekli CV'mle birliş iş başvurusu yapmak istiyorum.

Deneyimlerim:
- 5 yıl yazılım geliştirme
- Python, JavaScript, SQL

İlginiz için teşekkür ederim.

Saygılarımla,
[Adınız]
```

#### 3. Konu Başlığı
- **"Mail Konusu"**: `İş Başvurusu` (varsayılan)
- İsterseniz değiştirebilirsiniz

### Gönderme

#### Adım 1: Mailleri Kontrol Et
1. **"Email Listesi"** sekmesine gidin
2. Toplanan mailleri görün
3. İstemediğiniz mailleri seçip **"Seçili Email'leri Sil"** yapın

#### Adım 2: Gönder Butonuna Bas
1. **"Mail Gönder"** butonuna tıklayın
2. Sistem kontrol yapacak:
   - ✅ Gmail bilgileri var mı?
   - ✅ PDF seçili mi?
   - ✅ Mail metni yazılmış mı?
   - ✅ Gönderilecek mail var mı?

#### Adım 3: Tekrar Gönderim Kontrolü
Eğer daha önce mail gönderdiyseniz:
```
⚠️ UYARI: Mail Zaten Gönderilmiş!

Son gönderim: 2 gün önce
Tekrar gönderim süresi: 7 gün

🔒 5 gün sonra tekrar gönderebilirsiniz.

Yine de göndermek istiyor musunuz?
```

Bu uyarı sizi **spam yapmaktan korur**.

#### Adım 4: Onay
```
📧 127 mail gönderilsin mi?
```
- **Evet**: Gönderim başlar
- **Hayır**: İptal

### Gönderim Sırasında

#### Anlık Durum
```
📧 Mail Gönderiliyor...
23/127 gönderildi | ✅ 22 | ❌ 1
```

#### Log Ekranı
```
✅ [23/127] firma1@example.com
✅ [24/127] firma2@example.com
❌ [25/127] hatali@mail.com: Invalid address
```

#### Ne Kadar Sürer?
- Her mail arası **2 saniye** bekleme
- 100 mail için: ~3.5 dakika
- 200 mail için: ~7 dakika

### Gönderim Sonrası

#### Sonuç Ekranı
```
✅ GÖNDERIM TAMAMLANDI!

📊 SONUÇ:
✅ Başarılı: 125
❌ Hatalı: 2

Toplam: 127 mail
```

#### Gönderim Geçmişi
- Hangi maillere gönderildi kayıtlıdır
- **"Email Listesi"** sekmesinde görebilirsiniz
- Bir daha aynı maillere (7 gün içinde) gönderilmez

---

## 🔧 Sorun Giderme

### Tarayıcı Bulunamadı

**Hata:**
```
⚠️ Hiç tarayıcı bulunamadı!
```

**Çözüm:**
En az birini yükleyin:
- [Microsoft Edge](https://www.microsoft.com/edge) (Önerilen)
- [Google Chrome](https://www.google.com/chrome)
- [Mozilla Firefox](https://www.mozilla.org/firefox)

---

### Gmail Bağlanamadı

**Hata:**
```
❌ Gmail bağlanamadı: Authentication failed
```

**Çözümler:**

#### 1. Uygulama Şifresi Kullanın
- Normal şifrenizi değil, **uygulama şifresini** girin
- [Gmail Ayarları](#-gmail-ayarları) bölümüne bakın

#### 2. 2 Adımlı Doğrulama Açın
- [myaccount.google.com/security](https://myaccount.google.com/security)
- 2 Adımlı Doğrulamayı aktif edin

#### 3. "Güvenli Olmayan Uygulamalar" Kapalı Olmalı
- Google bu özelliği kaldırdı
- Artık sadece uygulama şifresi çalışır

---

### Selenium Hatası

**Hata:**
```
❌ Selenium hatası: WebDriver executable not found
```

**Çözüm:**
- Program driver'ları otomatik indirir
- **İnternet bağlantınızı** kontrol edin
- Eğer yine olmuyorsa:
  - Tarayıcınızı güncelleyin
  - Programı yeniden başlatın

---

### Mail Toplanamıyor

**Sorun:** Tarama bitiyor ama hiç mail yok.

**Kontrol Edin:**

#### 1. Derin Tarama Açık mı?
- ✅ **"Derin Tarama"** işaretli olmalı
- Normal tarama çok az mail bulur

#### 2. URL Doğru mu?
- Sitenin **firma listesi sayfası** olmalı
- Örnek: `https://www.iayosb.com/firmalarimiz/`
- **Ana sayfa değil!**

#### 3. Site Çalışıyor mu?
- Tarayıcıdan manuel kontrol edin
- Bazı siteler geçici kapalı olabilir

---

### Çok Yavaş Çalışıyor

**Sorun:** Tarama çok uzun sürüyor.

**Normal mi?**

**Derin tarama uzun sürer:**
- 100 firma için: ~30-45 dakika
- 200 firma için: ~60-90 dakika
- Her firma sayfasını tek tek ziyaret ediyor

**Hızlandırma:**

#### 1. Maksimum Sayfa Azalt
- 150 yerine 100 yapın
- Daha az firma taranır ama daha hızlı

#### 2. Tarayıcıyı Göstermeyi Kapat
- ❌ **"Tarayıcıyı Göster"** kapalı olmalı
- %30-40 daha hızlıdır

#### 3. Selenium Yerine Requests?
- **Hayır!** Selenium gerekli
- Çoğu site JavaScript kullanıyor

---

### Dosya Uzantıları Toplanıyor

**Sorun:** `image@2x.png` gibi dosya isimleri mail olarak geçiyor.

**Çözüm:**
- Program zaten otomatik filtreler
- 40+ dosya uzantısı engellenir
- Eğer yine görüyorsanız, program güncel değildir

---

## 💡 İpuçları

### Maksimum Verim İçin

#### 1. Derin Tarama Mutlaka Açık
```
❌ Normal: 5-10 mail
✅ Derin: 100+ mail (10-20x daha fazla!)
```

#### 2. Gece Çalıştırın
- Derin tarama 1 saat sürebilir
- Bilgisayarı kapatmayın
- Uyurken çalışsın

#### 3. İlk Önce Test Edin
- Kendinize test maili gönderin
- PDF'in düzgün eklendiğini kontrol edin
- Sonra toplu gönderiye başlayın

#### 4. Gmail Limiti
- Günde maksimum **500 mail**
- Daha fazla göndermeyin (hesap askıya alınır)
- 2 günde bir gönderseniz ideal

### Güvenlik

#### 1. Spam Yapmayın
- Tekrar gönderim süresi: **minimum 7 gün**
- İnsanları rahatsız etmeyin
- KVKK kurallarına uyun

#### 2. Şifrenizi Koruyun
- Uygulama şifresini kimseyle paylaşmayın
- `settings.json` dosyasını yedekleyin
- GitHub'a yüklemeyin (`.gitignore` var)

#### 3. Veritabanı Yedekleme
```bash
# email_bot.db dosyasını yedekleyin
copy email_bot.db email_bot_backup_2026-02-14.db
```

---

## 📊 Sık Sorulan Sorular

### Kaç mail toplayabilirim?
- **İAYOSB**: ~120 mail
- **Manisa OSB**: ~80 mail
- **Toplam**: site sayısına bağlı

### Gmail dışında kullanabilir miyim?
- Hayır, sadece Gmail destekleniyor
- Outlook/Yahoo çalışmaz

### Ücretli mi?
- Tamamen **ÜCRETSİZ**
- Açık kaynak (MIT License)

### Virüs var mı?
- Hayır, %100 güvenli
- Kaynak kodu açık
- Kendiniz inceleyebilirsiniz

### Mail adresleri doğru mu?
- %95+ doğruluk oranı
- Ama yine de bazıları yanlış olabilir
- Normal karşılanmalı

---

## 📞 Destek

### Sorun mu yaşıyorsunuz?

1. **Bu kılavuzu okuyun** (çoğu sorun burada)
2. [Sorun Giderme](#-sorun-giderme) bölümüne bakın
3. Hala çözmediyseniz:
   - [GitHub Issues](https://github.com/emreyaman1/email-bot/issues)
   - Yeni issue açın

### Özellik İsteği
- Yeni özellik ister misiniz?
- [Feature Request](https://github.com/emreyaman1/email-bot/issues/new?template=feature_request.md) açın

---

**İyi kullanımlar! 🚀**

*Son Güncelleme: 2026-02-14*
