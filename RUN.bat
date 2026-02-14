@echo off
title Email Bot Baslatici
color 0A

echo.
echo ====================================================
echo           EMAIL BOT BASLATICI v1.0
echo ====================================================
echo.

REM ===== PYTHON KONTROLU =====
echo [1/4] Python kontrol ediliyor...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [HATA] Python bulunamadi!
    echo.
    echo Cozum:
    echo 1. Python yuklemeniz gerekiyor
    echo 2. https://www.python.org/downloads/ adresinden indirin
    echo 3. Yuklerken "Add Python to PATH" secenegini isaretleyin
    echo.
    echo Kurulum sonrasi bilgisayari yeniden baslatin.
    echo.
    pause
    exit /b 1
)

REM Python versiyonunu al ve goster
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo       Python %PYVER% bulundu - OK
echo.

REM ===== PIP KONTROLU =====
echo [2/4] pip kontrol ediliyor...

python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [HATA] pip bulunamadi!
    echo.
    echo Cozum:
    echo 1. Komut satirinda su komutu calistirin:
    echo    python -m ensurepip --default-pip
    echo 2. Veya Python'u yeniden yukleyin
    echo.
    pause
    exit /b 1
)

echo       pip bulundu - OK
echo.

REM ===== EMAIL_BOT.PY KONTROLU =====
echo [3/4] Bot dosyasi kontrol ediliyor...

REM Once dir komutu ile kontrol et
dir email_bot.py >nul 2>&1
if %errorlevel% neq 0 (
    REM Alternatif kontrol - Python ile
    python -c "import os; exit(0 if os.path.exists('email_bot.py') else 1)" >nul 2>&1
    if %errorlevel% neq 0 (
        color 0C
        echo.
        echo ====================================================
        echo [HATA] email_bot.py dosyasi bulunamadi!
        echo ====================================================
        echo.
        echo Mevcut klasor: %CD%
        echo.
        echo Bu klasordeki Python dosyalari:
        dir /b *.py 2>nul
        if %errorlevel% neq 0 (
            echo    [Hicbir .py dosyasi bulunamadi]
        )
        echo.
        echo Tum dosyalar:
        dir /b
        echo.
        echo ====================================================
        echo.
        echo COZUM:
        echo.
        echo 1. email_bot.py dosyasinin bu klasorde oldugunu
        echo    kontrol edin
        echo.
        echo 2. Dosya adini kontrol edin:
        echo    - Tam olarak "email_bot.py" olmali
        echo    - Ekstra bosluk olmamali
        echo    - .txt uzantisi olmamali
        echo.
        echo 3. Tum dosyalari yeniden indirip bu klasore
        echo    cikarmay deneyin
        echo.
        echo ====================================================
        echo.
        pause
        exit /b 1
    )
)

echo       email_bot.py bulundu - OK
echo.

REM ===== KUTUPHANE YUKLEME =====
echo [4/4] Gerekli kutuphaneler yukleniyor...
echo       (Bu birkac dakika surebilir)
echo.

echo       - beautifulsoup4 yukleniyor...
python -m pip install beautifulsoup4 --quiet --upgrade
if %errorlevel% neq 0 (
    echo         [UYARI] Hata olustu, tekrar deneniyor...
    pip install beautifulsoup4 --upgrade
)

echo       - requests yukleniyor...
python -m pip install requests --quiet --upgrade
if %errorlevel% neq 0 (
    echo         [UYARI] Hata olustu, tekrar deneniyor...
    pip install requests --upgrade
)

echo       - lxml yukleniyor...
python -m pip install lxml --quiet --upgrade
if %errorlevel% neq 0 (
    echo         [UYARI] Hata olustu, tekrar deneniyor...
    pip install lxml --upgrade
)

echo.
echo       Tum kutuphaneler yuklendi - OK
echo.

REM ===== BOTU BASLAT =====
color 0A
echo ====================================================
echo           BOT BASLATILIYOR...
echo ====================================================
echo.

python email_bot.py

REM ===== HATA KONTROLU =====
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ====================================================
    echo [HATA] Bot calistirilirken bir hata olustu!
    echo ====================================================
    echo.
    echo Olasi nedenler:
    echo.
    echo 1. Kutuphane sorunu:
    echo    - Cozum: Bu dosyayi tekrar calistirin
    echo    - veya: pip install beautifulsoup4 requests lxml
    echo.
    echo 2. Kod hatasi:
    echo    - Yukardaki hata mesajini okuyun
    echo.
    echo 3. Izin sorunu:
    echo    - RUN.bat'i yonetici olarak calistirin
    echo    - Sag tiklayip "Yonetici olarak calistir" secin
    echo.
    pause
    exit /b 1
)

echo.
echo Bot kapatildi.
pause
