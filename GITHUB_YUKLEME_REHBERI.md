# 🚀 GitHub'a Yükleme Rehberi

## ✅ Yapılan Tüm Değişiklikler

### 1. ✨ Mail Gönderimi İyileştirmeleri
- ✅ **Anlık bildirim**: Kaç mail gönderildi gösteriliyor
- ✅ **İlerleme çubuğu**: `23/127 gönderildi | ✅ 22 | ❌ 1`
- ✅ **Detaylı özet**: Gönderim sonunda tam rapor

### 2. ⚠️ Uzun İşlem Uyarısı
- ✅ Derin tarama başlatılırken uyarı gösteriliyor
- ✅ Tahmini süre hesaplanıyor
- ✅ Kullanıcı onay veriyor

### 3. 🔒 Tekrar Gönderim Kontrolü
```
⚠️ UYARI: Mail Zaten Gönderilmiş!

Son gönderim: 2 gün önce
Tekrar gönderim süresi: 7 gün

🔒 5 gün sonra tekrar gönderebilirsiniz.
```

### 4. 🧹 Tüm Kişisel Veriler Temizlendi
- ✅ Settings.json → Boş/varsayılan
- ✅ Saved_urls.json → Sadece örnek siteler
- ✅ Email_bot.db → Silinmiş (yeni kullanıcılar için otomatik oluşacak)
- ✅ Tüm kişisel mail adresleri kaldırıldı
- ✅ Gmail şifreleri temizlendi

### 5. 🐛 İAYOSB Düzeltmesi
- ✅ URL pattern `/firmalar/` → `/works/` değiştirildi
- ✅ Artık İAYOSB.com'dan mükemmel çalışıyor

### 6. 🛡️ Email Validation
- ✅ Dosya uzantıları otomatik filtreniyor
- ✅ PNG, JPG, PDF vb. mail olarak algılanmıyor

---

## 📦 Hazır Dosyalar

GitHub'a yüklemek için tüm dosyalar hazır:

```
email-bot/
├── email_bot.py              ✅ Ana program
├── settings.json             ✅ Boş ayarlar (template)
├── saved_urls.json           ✅ Örnek URL'ler
├── README.md                 ✅ İngilizce README
├── KULLANIM_KILAVUZU.md      ✅ Türkçe detaylı kılavuz
├── LICENSE                   ✅ MIT License
└── .gitignore                ✅ Kişisel dosyaları korur
```

---

## 🎯 GitHub'a Yükleme Adımları

### Adım 1: GitHub Repository Oluştur
1. [GitHub.com](https://github.com) → Giriş yap
2. Sağ üstten **"+"** → **"New repository"**
3. Repository adı: `email-bot` (veya istediğiniz isim)
4. ✅ Public seçin (herkes görebilsin)
5. ❌ **"Initialize with README"** seçmeyin (bizde zaten var)
6. **"Create repository"** tıklayın

### Adım 2: Git Kurulumu (İlk kez kullanıyorsanız)

#### Windows için:
1. [Git for Windows](https://git-scm.com/download/win) indirin
2. Yükleyin (varsayılan ayarlarla)
3. Git Bash'i açın

#### Mac için:
```bash
# Terminal'i açın
git --version  # Yoksa otomatik yüklenir
```

#### Linux için:
```bash
sudo apt-get install git
```

### Adım 3: Dosyaları Hazırla

Tüm dosyalar outputs klasöründe hazır! Şimdi bunları kopyalayın:

```bash
# Yeni bir klasör oluştur
mkdir email-bot
cd email-bot

# Dosyaları buraya kopyala (outputs klasöründen)
# Windows: Dosyaları sürükle-bırak yapabilirsin
# Mac/Linux: cp komutu kullan
```

### Adım 4: Git İlk Ayar

```bash
# İlk kez kullanıyorsanız (sadece bir kez):
git config --global user.name "Adınız Soyadınız"
git config --global user.email "mail@example.com"
```

### Adım 5: Repository Başlat

```bash
# Git başlat
git init

# Dosyaları ekle
git add .

# İlk commit
git commit -m "İlk versiyon: Email Bot v3.3"
```

### Adım 6: GitHub'a Bağlan ve Yükle

GitHub'da oluşturduğunuz repository sayfasında gösterilen komutları kullanın:

```bash
# GitHub repository'ye bağlan (kendi URL'nizi yazın)
git remote add origin https://github.com/KULLANICI_ADINIZ/email-bot.git

# Ana branch'i main olarak ayarla
git branch -M main

# GitHub'a yükle
git push -u origin main
```

**İlk kez push yapıyorsanız:**
- GitHub kullanıcı adınızı soracak
- Şifre yerine **Personal Access Token** girmeniz gerekecek

### Adım 7: Personal Access Token Oluştur (Gerekirse)

1. GitHub → Settings (sağ üst profil fotoğrafı)
2. **Developer settings** (en altta)
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)**
5. Note: "Email Bot Upload"
6. ✅ **repo** seçeneğini işaretle
7. **Generate token**
8. Token'ı kopyala (bir daha gösterilmeyecek!)
9. Push yaparken şifre yerine bu token'ı gir

---

## 🎉 Tamamlandı!

Repository'niz artık hazır:
```
https://github.com/KULLANICI_ADINIZ/email-bot
```

### Ne Yapabilirsiniz?

#### 1. README'yi Düzenle
- GitHub sayfasında **README.md** dosyasını aç
- ✏️ Düzenle butonuna tıkla
- `KULLANICI_ADINIZ` yazan yerleri düzelt
- **Commit changes**

#### 2. Release Oluştur (İsteğe Bağlı)
1. Repository sayfasında **"Releases"** → **"Create a new release"**
2. Tag: `v3.3`
3. Title: `Email Bot v3.3 - İlk Sürüm`
4. Description:
```
## ✨ Özellikler
- 📧 Gmail üzerinden toplu mail gönderimi
- 🔍 Akıllı web scraping (Selenium + Requests)
- 🎯 Derin tarama modu
- 🛡️ Gelişmiş email validation
- 📊 Veritabanı ile takip sistemi

## 🚀 Kurulum
`python email_bot.py`

Detaylı kullanım için README.md dosyasına bakın.
```
5. **Publish release**

#### 3. Yıldız İste! ⭐
README'ye ekle:
```markdown
## ⭐ Beğendiyseniz Yıldız Verin!

Bu projeyi faydalı buldunuz mu? Yıldız verin!
```

---

## 🔒 Güvenlik Kontrol Listesi

Yüklemeden önce kontrol edin:

- ✅ `settings.json` boş/varsayılan değerler
- ✅ `email_bot.db` yok (silinmiş)
- ✅ Kişisel Gmail adresleri yok
- ✅ Kişisel Gmail şifreleri yok
- ✅ Toplanan email listesi yok
- ✅ `.gitignore` dosyası var
- ✅ README'de `KULLANICI_ADINIZ` placeholder'ları var

**Tüm kişisel veriler temizlendi! ✅**

---

## 📝 Güncelleme Yapmak

Gelecekte kod güncelledikçe:

```bash
# Değişiklikleri kaydet
git add .
git commit -m "Güncelleme açıklaması"

# GitHub'a yükle
git push
```

---

## 🤝 Katkıda Bulunma

Başkaları da katkıda bulunabilir:
1. Repository'yi **fork** ederler
2. Değişiklik yaparlar
3. **Pull Request** açarlar
4. Sen onaylarsın

---

## 💡 İpuçları

### README'yi Özelleştir
- Adınızı ekleyin
- İletişim bilgilerinizi ekleyin
- Örnek screenshot'lar ekleyin
- Video tutorial linki ekleyin

### Topics Ekle
Repository sayfasında **"Add topics"**:
- `python`
- `automation`
- `email`
- `web-scraping`
- `selenium`
- `gmail`
- `tkinter`

### LICENSE'ı Güncelle
```
Copyright (c) 2026 [Adınız]
```

---

## 🎊 Başarılar!

Artık programınız GitHub'da herkese açık!

İnsanlar:
- ⭐ Yıldız verebilir
- 🍴 Fork yapabilir
- 🐛 Issue açabilir
- 🔧 Pull request gönderebilir

**Açık kaynak dünyasına hoş geldiniz! 🚀**

---

**Not:** Bu dosyayı GitHub'a yüklemeyin, sadece rehber olarak kullanın.
