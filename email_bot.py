#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E-posta Otomasyon Botu v3.3 - ÇOKLU SİTE TARAMA + DERİN TARAMA
Birden fazla siteyi aynı anda tarayın!
Derin tarama: Firma detay sayfalarına girer ve mail toplar!
Chrome, Edge, Firefox - Otomatik tespit ve kullanım!
"""

import sys
import subprocess

# Gerekli kütüphaneleri otomatik yükle
def check_and_install_requirements():
    """Gerekli kütüphaneleri kontrol et ve eksikleri yükle"""
    required_packages = {
        'bs4': 'beautifulsoup4',
        'requests': 'requests',
        'lxml': 'lxml',
        'openpyxl': 'openpyxl',
        'selenium': 'selenium',
    }
    
    print("\n" + "="*60)
    print("  GEREKLI KUTUPHANELER KONTROL EDILIYOR...")
    print("="*60 + "\n")
    
    missing_packages = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  ✓ {package_name:25} - Yuklu")
        except ImportError:
            print(f"  ✗ {package_name:25} - EKSIK")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n{'='*60}")
        print(f"  {len(missing_packages)} KUTUPHANE YUKLENECEK")
        print(f"{'='*60}\n")
        print("  Lutfen bekleyin, bu 1-2 dakika surebilir...\n")
        
        failed_packages = []
        for i, package in enumerate(missing_packages, 1):
            print(f"[{i}/{len(missing_packages)}] {package} yukleniyor...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package, "--upgrade"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"     ✓ {package} basariyla yuklendi!\n")
            except subprocess.CalledProcessError as e:
                print(f"     ✗ {package} yuklenemedi!")
                print(f"     Hata kodu: {e.returncode}\n")
                failed_packages.append(package)
        
        print("="*60)
        if failed_packages:
            print("  UYARI: Bazi kutuphaneler yuklenemedi!")
            print(f"  Basarisiz: {', '.join(failed_packages)}")
            print("\n  Lutfen manuel yukleyin:")
            print(f"  pip install {' '.join(failed_packages)}")
        else:
            print("  TUM KUTUPHANELER YUKLENDI!")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("  TUM KUTUPHANELER MEVCUT!")
        print("="*60 + "\n")

if sys.version_info < (3, 7):
    print("HATA: Python 3.7+ gerekli!")
    sys.exit(1)

check_and_install_requirements()

# Kütüphaneleri import et
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog
    import threading
    import time
    import re
    import json
    import os
    from datetime import datetime
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin, urlparse
    import sqlite3
    import openpyxl
    import platform
    import shutil
    import gc  # Garbage collector - RAM optimizasyonu için
    
    # SELENIUM İÇİN
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.edge.service import Service as EdgeService
    from selenium.webdriver.edge.options import Options as EdgeOptions
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
except ImportError as e:
    print(f"Import hatası: {e}")
    print("Lütfen programı yeniden başlatın!")
    input("Enter'a basın...")
    sys.exit(1)


class BrowserManager:
    """Çoklu tarayıcı yöneticisi - Chrome, Edge, Firefox"""
    
    @staticmethod
    def detect_available_browsers():
        """Sistemde mevcut tarayıcıları tespit et"""
        available = []
        
        system = platform.system()
        
        # Edge kontrolü
        try:
            if system == "Windows":
                edge_paths = [
                    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                ]
                for path in edge_paths:
                    if os.path.exists(path):
                        available.append("Edge")
                        break
            elif system == "Darwin":  # macOS
                if os.path.exists("/Applications/Microsoft Edge.app"):
                    available.append("Edge")
            else:  # Linux
                if shutil.which("microsoft-edge") or shutil.which("microsoft-edge-stable"):
                    available.append("Edge")
        except:
            pass
        
        # Chrome kontrolü
        try:
            if system == "Windows":
                chrome_paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                ]
                for path in chrome_paths:
                    if os.path.exists(path):
                        available.append("Chrome")
                        break
            elif system == "Darwin":  # macOS
                if os.path.exists("/Applications/Google Chrome.app"):
                    available.append("Chrome")
            else:  # Linux
                if shutil.which("google-chrome") or shutil.which("chrome"):
                    available.append("Chrome")
        except:
            pass
        
        # Firefox kontrolü
        try:
            if system == "Windows":
                firefox_paths = [
                    r"C:\Program Files\Mozilla Firefox\firefox.exe",
                    r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
                ]
                for path in firefox_paths:
                    if os.path.exists(path):
                        available.append("Firefox")
                        break
            elif system == "Darwin":  # macOS
                if os.path.exists("/Applications/Firefox.app"):
                    available.append("Firefox")
            else:  # Linux
                if shutil.which("firefox"):
                    available.append("Firefox")
        except:
            pass
        
        return available
    
    @staticmethod
    def get_browser_version(browser_name):
        """Tarayıcı versiyonunu al"""
        try:
            system = platform.system()
            
            if browser_name == "Edge":
                if system == "Windows":
                    import winreg
                    try:
                        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Edge\BLBeacon")
                        version, _ = winreg.QueryValueEx(key, "version")
                        return version
                    except:
                        pass
                    
                    # Alternatif: Edge.exe'den
                    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                    if not os.path.exists(edge_path):
                        edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
                    
                    if os.path.exists(edge_path):
                        result = subprocess.check_output([edge_path, '--version'], text=True)
                        return result.split()[-1]
                
            elif browser_name == "Chrome":
                if system == "Windows":
                    import winreg
                    try:
                        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
                        version, _ = winreg.QueryValueEx(key, "version")
                        return version
                    except:
                        pass
                elif system == "Linux":
                    result = subprocess.check_output(['google-chrome', '--version'], text=True)
                    return result.split()[-1]
                elif system == "Darwin":
                    result = subprocess.check_output(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], text=True)
                    return result.split()[-1]
            
            elif browser_name == "Firefox":
                if system == "Windows":
                    result = subprocess.check_output([r"C:\Program Files\Mozilla Firefox\firefox.exe", '--version'], text=True)
                    return result.split()[-1]
                elif system == "Linux":
                    result = subprocess.check_output(['firefox', '--version'], text=True)
                    return result.split()[-1]
                elif system == "Darwin":
                    result = subprocess.check_output(['/Applications/Firefox.app/Contents/MacOS/firefox', '--version'], text=True)
                    return result.split()[-1]
        except:
            pass
        
        return None
    
    @staticmethod
    def download_driver(browser_name, version=None):
        """Driver'ı indir"""
        try:
            import zipfile
            import io
            
            system = platform.system()
            
            if browser_name == "Edge":
                # EdgeDriver indirme
                if not version:
                    # En son stable versiyonu al
                    version_url = "https://msedgedriver.azureedge.net/LATEST_STABLE"
                    try:
                        response = requests.get(version_url, timeout=10)
                        version = response.text.strip()
                    except:
                        version = "120.0.2210.91"  # Fallback
                
                if system == "Windows":
                    platform_name = "win64" if platform.machine().endswith('64') else "win32"
                    driver_name = "msedgedriver.exe"
                elif system == "Linux":
                    platform_name = "linux64"
                    driver_name = "msedgedriver"
                elif system == "Darwin":
                    platform_name = "mac64"
                    driver_name = "msedgedriver"
                else:
                    return None
                
                download_url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_{platform_name}.zip"
                
            elif browser_name == "Chrome":
                # ChromeDriver indirme
                if not version:
                    version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
                    try:
                        response = requests.get(version_url, timeout=10)
                        version = response.text.strip()
                    except:
                        version = "120.0.6099.109"
                
                if system == "Windows":
                    platform_name = "win32"
                    driver_name = "chromedriver.exe"
                elif system == "Linux":
                    platform_name = "linux64"
                    driver_name = "chromedriver"
                elif system == "Darwin":
                    platform_name = "mac64"
                    driver_name = "chromedriver"
                else:
                    return None
                
                download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_{platform_name}.zip"
            
            elif browser_name == "Firefox":
                # GeckoDriver indirme
                gecko_api = "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
                try:
                    response = requests.get(gecko_api, timeout=10)
                    latest = response.json()
                    version = latest['tag_name'].replace('v', '')
                except:
                    version = "0.33.0"
                
                if system == "Windows":
                    platform_name = "win64" if platform.machine().endswith('64') else "win32"
                    driver_name = "geckodriver.exe"
                    file_ext = "zip"
                elif system == "Linux":
                    platform_name = "linux64"
                    driver_name = "geckodriver"
                    file_ext = "tar.gz"
                elif system == "Darwin":
                    platform_name = "macos"
                    driver_name = "geckodriver"
                    file_ext = "tar.gz"
                else:
                    return None
                
                download_url = f"https://github.com/mozilla/geckodriver/releases/download/v{version}/geckodriver-v{version}-{platform_name}.{file_ext}"
            
            print(f"Driver indiriliyor: {download_url}")
            
            response = requests.get(download_url, timeout=30)
            response.raise_for_status()
            
            # Unzip
            temp_dir = os.path.join(os.path.expanduser("~"), f".{browser_name.lower()}driver")
            os.makedirs(temp_dir, exist_ok=True)
            
            if download_url.endswith('.zip'):
                with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                    zip_ref.extractall(temp_dir)
            else:  # tar.gz
                import tarfile
                with tarfile.open(fileobj=io.BytesIO(response.content)) as tar_ref:
                    tar_ref.extractall(temp_dir)
            
            driver_path = os.path.join(temp_dir, driver_name)
            
            # Linux/Mac için executable yap
            if system in ["Linux", "Darwin"]:
                os.chmod(driver_path, 0o755)
            
            return driver_path
        
        except Exception as e:
            print(f"Driver indirme hatası: {e}")
            return None
    
    @staticmethod
    def find_local_driver(browser_name):
        """Sistemde mevcut driver'ı bul"""
        if browser_name == "Edge":
            driver_names = ['msedgedriver.exe', 'msedgedriver']
        elif browser_name == "Chrome":
            driver_names = ['chromedriver.exe', 'chromedriver']
        elif browser_name == "Firefox":
            driver_names = ['geckodriver.exe', 'geckodriver']
        else:
            return None
        
        # PATH'de ara
        for name in driver_names:
            driver_path = shutil.which(name)
            if driver_path:
                return driver_path
        
        # Yaygın konumlarda ara
        possible_locations = [
            os.path.join(os.path.expanduser("~"), f".{browser_name.lower()}driver"),
            os.path.join(os.getcwd()),
        ]
        
        if platform.system() == "Windows":
            possible_locations.append(f"C:\\{browser_name.lower()}driver")
        else:
            possible_locations.append("/usr/local/bin")
        
        for location in possible_locations:
            for name in driver_names:
                driver_path = os.path.join(location, name)
                if os.path.exists(driver_path):
                    return driver_path
        
        return None


class EmailBot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📧 Mail Botu v3.3 - ÇOKLU SİTE TARAMA")
        self.root.geometry("1200x800")
        
        # Email validation için dosya uzantıları blacklist
        self.file_extensions_blacklist = {
            # Resim formatları
            'png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp', 'ico', 'tiff', 'tif',
            # Video formatları
            'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm',
            # Ses formatları
            'mp3', 'wav', 'ogg', 'flac', 'm4a', 'aac',
            # Döküman formatları
            'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'rtf',
            # Arşiv formatları
            'zip', 'rar', '7z', 'tar', 'gz',
            # Kod ve script formatları
            'js', 'css', 'html', 'xml', 'json', 'py', 'java', 'cpp', 'c', 'php',
            # Diğer
            'exe', 'dll', 'dmg', 'pkg', 'deb', 'rpm'
        }
        
        # YENI: Pencere simgesi ayarla
        try:
            # Icon dosyası varsa kullan
            if os.path.exists('email_bot_icon.ico'):
                self.root.iconbitmap('email_bot_icon.ico')
            else:
                # Windows için alternatif yöntem
                try:
                    import base64
                    from PIL import Image, ImageTk
                    import io
                    
                    # Küçük bir mail simgesi (base64 encoded)
                    icon_data = self.create_icon_base64()
                    icon_bytes = base64.b64decode(icon_data)
                    icon_image = Image.open(io.BytesIO(icon_bytes))
                    icon_photo = ImageTk.PhotoImage(icon_image)
                    self.root.iconphoto(True, icon_photo)
                except:
                    pass
        except:
            pass
        
        self.scanning = False
        self.auto_scan_active = False
        self.auto_scan_timer = None
        self.auto_scan_remaining_seconds = 0
        
        # YENİ: Tarama durumu için değişkenler
        self.current_scan_url = tk.StringVar(value="")
        self.emails_found_count = tk.IntVar(value=0)
        
        self.pdf_path = None
        self.email_text = ""
        
        self.gmail_address = tk.StringVar()
        self.gmail_password = tk.StringVar()
        self.resend_days = tk.IntVar(value=7)
        self.base_url = tk.StringVar(value="")
        self.email_subject = tk.StringVar(value="İş Başvurusu")
        
        # YENİ: Multi-browser
        self.use_selenium = tk.BooleanVar(value=True)
        self.show_browser = tk.BooleanVar(value=False)
        self.selected_browser = tk.StringVar(value="Auto")
        
        # YENİ: Derin tarama için
        self.deep_scan = tk.BooleanVar(value=False)
        self.max_pages = tk.IntVar(value=100)
        
        # YENİ: URL yönetimi için
        self.saved_urls = {}  # {isim: url}
        self.selected_url_name = tk.StringVar()
        self.url_checkboxes = {}  # {isim: BooleanVar} - Her URL için checkbox durumu
        
        # Driver yolları
        self.driver_paths = {}
        self.available_browsers = []
        
        # YENİ: Otomatik kayıt için zamanlayıcı ve flag
        self.auto_save_timer = None
        self.settings_changed = False
        
        self.init_database()
        self.load_saved_urls()  # YENİ: Kayıtlı URL'leri yükle
        self.create_gui()
        self.load_settings()
        self.detect_browsers()
        
        # YENİ: Tüm değişkenlere trace ekle
        self.setup_auto_save_triggers()
        
    def is_valid_email(self, email):
        """
        Email adresini doğrula - GEVŞEK MOD (IKA MCBU için)
        Sadece temel formatı kontrol et, agresif filtreleme yapma
        
        Args:
            email: Kontrol edilecek email adresi
            
        Returns:
            bool: Email geçerliyse True, değilse False
        """
        if not email or '@' not in email:
            return False
        
        email = email.lower().strip()
        
        # @ karakteri sayısı kontrolü (tam 1 tane olmalı)
        if email.count('@') != 1:
            return False
        
        # Email çok kısa olmamalı (minimum a@b.c)
        if len(email) < 5:
            return False
        
        try:
            username, domain = email.split('@')
            
            # Username kontrolü
            if not username or len(username) < 1:
                return False
            
            # Domain kontrolü - en az bir nokta içermeli
            if not domain or '.' not in domain:
                return False
            
            # Domain'in en az bir nokta içermesi ve TLD'si olması gerekir
            domain_parts = domain.split('.')
            if len(domain_parts) < 2:
                return False
            
            # TLD kontrolü (son kısım en az 2 karakter olmalı)
            tld = domain_parts[-1]
            if len(tld) < 2:
                return False
            
            # SADECE AÇIK DOSYA UZANTISI FİLTRELEMESİ - Diğer her şeyi geçir
            # Sadece resim/video/arşiv dosyalarını filtrele
            image_and_file_extensions = {
                'png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp', 'ico',
                'mp4', 'avi', 'mov', 'mp3', 'wav',
                'zip', 'rar', '7z', 'tar', 'gz',
                'exe', 'dll', 'dmg'
            }
            
            # Sadece TLD dosya uzantısıysa filtrele
            if tld in image_and_file_extensions:
                return False
            
            # Email'in son kısmı kontrol et (örn: something@image.png gibi)
            email_parts = email.split('.')
            if len(email_parts) > 1:
                last_ext = email_parts[-1]
                if last_ext in image_and_file_extensions:
                    return False
            
            # Nokta veya tire ile başlamamalı/bitmemeli (temel kontrol)
            if username.startswith('.') or username.endswith('.'):
                return False
            if domain.startswith('.') or domain.endswith('.'):
                return False
            if domain.startswith('-') or domain.endswith('-'):
                return False
            
            # Geçerli bir email - GEVŞEK MOD
            return True
            
        except Exception as e:
            # Herhangi bir hata durumunda False döndür
            return False
        
    def init_database(self):
        """SQLite veritabanını başlat"""
        self.conn = sqlite3.connect('email_bot.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_pool (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                source_url TEXT,
                collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS send_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                FOREIGN KEY (email) REFERENCES email_pool(email)
            )
        ''')
        
        self.conn.commit()
        
    def load_saved_urls(self):
        """Kayıtlı URL'leri yükle"""
        # Varsayılan URL'ler
        default_urls = {
            "İstanbul Anadolu Yakası OSB": "https://www.iayosb.com/firmalarimiz/",
            "Manisa OSB": "https://www.mosb.org.tr/firmalar/"
        }
        
        if os.path.exists('saved_urls.json'):
            try:
                with open('saved_urls.json', 'r', encoding='utf-8') as f:
                    self.saved_urls = json.load(f)
                    # Varsayılan URL'lerin ekli olduğundan emin ol
                    for name, url in default_urls.items():
                        if name not in self.saved_urls:
                            self.saved_urls[name] = url
            except:
                self.saved_urls = default_urls
        else:
            self.saved_urls = default_urls
            self.save_saved_urls()
    
    def save_saved_urls(self):
        """Kayıtlı URL'leri kaydet"""
        with open('saved_urls.json', 'w', encoding='utf-8') as f:
            json.dump(self.saved_urls, f, indent=2, ensure_ascii=False)
            
    def create_icon_base64(self):
        """Basit bir mail simgesi için base64 data (backup olarak)"""
        # Bu, küçük bir PNG mail simgesi
        return "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsTAAALEwEAmpwYAAABfUlEQVR4nO2W0U3DMBCGP6oOwAZ0BDoCbAAbdIROABvABh2BbkA3oCPQDWAENqAjcJWSKrLl1E5TE6nyS5Yt+T7/d8/nO4AZM+YfowLqAXYAfcDnBLAL2AW0/rvPA/YBJ4AtQA/wDngGrPu/bwAHgC1AC9j3+d0B1gBLPr8CuADeAJeAU8Ayv+MC8AjYBhwCrgFvgOeAbcAOoA64A1wD7gHHgDXAMuAE8AA4BJwBzgHPgFPA5oQALoFHwDpgE3AM+AJ8BL4DHgBrgFXAMeAT8BX4AXwGbgA3gS3AKmAV8A34BnwBfgK/gF/Ab+AX8BX4CXwCfgI/gB/AD+AH8B34DnwHvgPfgO/AN+Ab8A34CXwFfgBfgK/AZ+Az8An4BHwCPgGfgE/AJ+AT8An4BHwCPgOfgE/AJ+Az8Bn4DHwGPgOfgc/AZ+Az8Bn4DHwGPgOfgc/AZ+Az8Bn4DHwGPgOfgc/AZ+Az8Bn4DHwGPgOfgc/AZ+AzM2bMGP4BfgNt2B8hPLEAAAAASUVORK5CYII="
    
    def detect_browsers(self):
        """Tarayıcıları tespit et"""
        self.log("🔍 Tarayıcılar tespit ediliyor...")
        
        self.available_browsers = BrowserManager.detect_available_browsers()
        
        if not self.available_browsers:
            self.log("⚠️ Hiç tarayıcı bulunamadı!", "WARNING")
            messagebox.showwarning(
                "Tarayıcı Yok",
                "Edge, Chrome veya Firefox bulunamadı!\n\n" +
                "Lütfen en az birini yükleyin:\n" +
                "• Microsoft Edge (Önerilen - Windows'ta varsayılan)\n" +
                "• Google Chrome\n" +
                "• Mozilla Firefox"
            )
            return
        
        self.log(f"✅ {len(self.available_browsers)} tarayıcı bulundu: {', '.join(self.available_browsers)}")
        
        # Her tarayıcı için driver hazırla
        for browser in self.available_browsers:
            self.log(f"🔧 {browser} driver kontrol ediliyor...")
            
            # Önce mevcut driver'ı bul
            driver_path = BrowserManager.find_local_driver(browser)
            
            if driver_path:
                self.driver_paths[browser] = driver_path
                self.log(f"✅ {browser}Driver bulundu: {driver_path}")
            else:
                # İndir
                self.log(f"📥 {browser}Driver indiriliyor...")
                version = BrowserManager.get_browser_version(browser)
                if version:
                    self.log(f"{browser} versiyonu: {version}")
                
                driver_path = BrowserManager.download_driver(browser, version)
                
                if driver_path:
                    self.driver_paths[browser] = driver_path
                    self.log(f"✅ {browser}Driver indirildi: {driver_path}")
                else:
                    self.log(f"⚠️ {browser}Driver indirilemedi", "WARNING")
                    self.log(f"💡 Selenium otomatik driver yönetimi kullanılacak", "INFO")
        
        # Browser dropdown'ını güncelle
        self.update_browser_dropdown()
        
    def update_browser_dropdown(self):
        """Browser seçim dropdown'ını güncelle"""
        browsers = ["Auto (Otomatik)"] + self.available_browsers
        
        # Mevcut seçimi koru
        current = self.selected_browser.get()
        
        # Dropdown'ı güncelle
        self.browser_dropdown['values'] = browsers
        
        # Varsayılan seçim
        if current == "Auto" or current not in self.available_browsers:
            self.selected_browser.set("Auto (Otomatik)")
        
    def get_best_browser(self):
        """En iyi tarayıcıyı seç"""
        selection = self.selected_browser.get()
        
        # Kullanıcı manuel seçtiyse
        if selection != "Auto (Otomatik)":
            browser = selection
            if browser in self.available_browsers:
                self.log(f"🎯 Manuel seçim: {browser}")
                return browser
        
        # Otomatik: Öncelik sırası Edge > Chrome > Firefox
        priority = ["Edge", "Chrome", "Firefox"]
        
        for browser in priority:
            if browser in self.available_browsers:
                self.log(f"🎯 Otomatik seçim: {browser}")
                return browser
        
        return None
    
    def create_gui(self):
        """Ana GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_dashboard_tab(notebook)
        self.create_email_editor_tab(notebook)
        self.create_settings_tab(notebook)
        self.create_logs_tab(notebook)
        
    def create_dashboard_tab(self, notebook):
        """Ana panel"""
        dashboard = ttk.Frame(notebook)
        notebook.add(dashboard, text='📊 Ana Panel')
        
        info_frame = ttk.LabelFrame(dashboard, text="📈 İstatistikler", padding=10)
        info_frame.pack(fill='x', padx=10, pady=10)
        
        self.email_count_label = ttk.Label(info_frame, text="📧 Toplam Mail: 0", 
                                           font=('Arial', 14, 'bold'))
        self.email_count_label.pack(side='left', padx=20)
        
        self.sent_count_label = ttk.Label(info_frame, text="📤 Gönderilen: 0", 
                                         font=('Arial', 14, 'bold'))
        self.sent_count_label.pack(side='left', padx=20)
        
        # YENİ: Tarama durumu göstergesi
        scan_status_frame = ttk.LabelFrame(dashboard, text="📍 Tarama Durumu", padding=10)
        scan_status_frame.pack(fill='x', padx=10, pady=10)
        
        self.scan_progress_label = ttk.Label(scan_status_frame, text="Beklemede...", 
                                            font=('Arial', 12, 'bold'), foreground='gray')
        self.scan_progress_label.pack(pady=5)
        
        self.scan_details_label = ttk.Label(scan_status_frame, text="", 
                                           font=('Arial', 10), foreground='blue')
        self.scan_details_label.pack(pady=2)
        
        control_frame = ttk.LabelFrame(dashboard, text="🎮 Kontroller", padding=10)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill='x', pady=5)
        
        self.scan_btn = ttk.Button(btn_frame, text="🔍 Şimdi Tara", 
                                   command=self.start_scan, width=20)
        self.scan_btn.pack(side='left', padx=5)
        
        self.auto_scan_btn = ttk.Button(btn_frame, text="🤖 Otomatik Mail Bul", 
                                       command=self.toggle_auto_scan, width=20)
        self.auto_scan_btn.pack(side='left', padx=5)
        
        self.stop_scan_btn = ttk.Button(btn_frame, text="⏹️ Durdur", 
                                       command=self.stop_scan, state='disabled', width=20)
        self.stop_scan_btn.pack(side='left', padx=5)
        
        self.timer_label = ttk.Label(control_frame, text="", 
                                     font=('Arial', 12, 'bold'), foreground='blue')
        self.timer_label.pack(pady=5)
        
        email_frame = ttk.LabelFrame(dashboard, text="📧 Mail Listesi", padding=10)
        email_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        list_scroll = ttk.Scrollbar(email_frame)
        list_scroll.pack(side='right', fill='y')
        
        # FIX: selectmode=tk.EXTENDED yerine tk.MULTIPLE kullanıyoruz ama Ctrl+Click için düzgün çalışacak
        self.email_listbox = tk.Listbox(email_frame, yscrollcommand=list_scroll.set,
                                       font=('Consolas', 10), selectmode=tk.EXTENDED)
        self.email_listbox.pack(side='left', fill='both', expand=True)
        list_scroll.config(command=self.email_listbox.yview)
        
        btn_frame2 = ttk.Frame(dashboard)
        btn_frame2.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(btn_frame2, text="🗑️ Seçilileri Sil", 
                  command=self.delete_selected_emails).pack(side='left', padx=5)
        ttk.Button(btn_frame2, text="🗑️ TÜMÜNÜ SİL", 
                  command=self.delete_all_emails).pack(side='left', padx=5)
        ttk.Button(btn_frame2, text="📊 Excel'den Al", 
                  command=self.import_from_excel).pack(side='left', padx=5)
        ttk.Button(btn_frame2, text="📤 Dışa Aktar", 
                  command=self.export_emails).pack(side='left', padx=5)
        
    def create_email_editor_tab(self, notebook):
        """Mail editör"""
        editor = ttk.Frame(notebook)
        notebook.add(editor, text='✉️ Mail Editör')
        
        # Mail konusu
        subject_frame = ttk.LabelFrame(editor, text="📧 Mail Konusu", padding=10)
        subject_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(subject_frame, text="Konu:").pack(side='left', padx=5)
        ttk.Entry(subject_frame, textvariable=self.email_subject, width=60).pack(side='left', padx=5)
        
        pdf_frame = ttk.LabelFrame(editor, text="📎 CV Ekle", padding=10)
        pdf_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(pdf_frame, text="📁 PDF Seç", 
                  command=self.select_pdf).pack(side='left', padx=5)
        
        self.pdf_status_label = ttk.Label(pdf_frame, text="📄 PDF seçilmedi", 
                                         foreground="red")
        self.pdf_status_label.pack(side='left', padx=10)
        
        text_frame = ttk.LabelFrame(editor, text="📝 Mail Metni", padding=10)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.text_editor = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                     font=('Arial', 11), height=20)
        self.text_editor.pack(fill='both', expand=True)
        
        default_text = """Merhaba,

İş ilanlarınız için başvuruda bulunmak istiyorum. 

CV'mi ekte bulabilirsiniz. İlginiz için teşekkür ederim.

Saygılarımla,
"""
        self.text_editor.insert('1.0', default_text)
        
        # YENİ: Text editör değişikliklerini takip et
        self.text_editor.bind('<<Modified>>', self.on_text_modified)
        
        send_frame = ttk.Frame(editor)
        send_frame.pack(fill='x', padx=10, pady=10)
        
        self.send_btn = ttk.Button(send_frame, text="📧 Mailleri Gönder", 
                                   command=self.send_emails)
        self.send_btn.pack(pady=5)
        
    def create_settings_tab(self, notebook):
        """Ayarlar"""
        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text='⚙️ Ayarlar')
        
        # Canvas ve Scrollbar oluştur
        canvas = tk.Canvas(settings_tab)
        scrollbar = ttk.Scrollbar(settings_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Scrollable frame'in genişliğini canvas genişliğine bind et
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def _on_canvas_configure(event):
            # Canvas genişliği değiştiğinde, frame'in genişliğini güncelle
            canvas.itemconfig(canvas_window, width=event.width)
        
        scrollable_frame.bind("<Configure>", _on_frame_configure)
        canvas.bind("<Configure>", _on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar ve canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Ana container - genişliği dinamik
        settings = scrollable_frame
        settings.columnconfigure(0, weight=1)
        
        # Gmail - TAM GENİŞLİK
        gmail_frame = ttk.LabelFrame(settings, text="📮 Gmail Ayarları", padding=15)
        gmail_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        gmail_frame.columnconfigure(1, weight=1)
        
        ttk.Label(gmail_frame, text="E-posta:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=8, padx=5)
        ttk.Entry(gmail_frame, textvariable=self.gmail_address, font=('Arial', 10)).grid(row=0, column=1, sticky='ew', pady=8, padx=5)
        
        ttk.Label(gmail_frame, text="Uygulama Şifresi:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=8, padx=5)
        ttk.Entry(gmail_frame, textvariable=self.gmail_password, show='*', font=('Arial', 10)).grid(row=1, column=1, sticky='ew', pady=8, padx=5)
        
        # ÖNEMLİ NOT
        note_frame = ttk.Frame(gmail_frame)
        note_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10, padx=5)
        
        note_text = """⚠️ ÖNEMLİ: Bu şifre Gmail hesabınızın şifresi DEĞİLDİR!
Bu özel bir "Uygulama Şifresi"dir ve Gmail ayarlarından alınır.

📺 Nasıl alınır? Aşağıdaki linke tıklayın:"""
        
        ttk.Label(note_frame, text=note_text, foreground="red", 
                 font=('Arial', 9), justify='left').pack(anchor='w')
        
        # Video linki
        video_link = ttk.Label(note_frame, 
                              text="🎥 Gmail Uygulama Şifresi Nasıl Alınır? (YouTube)",
                              foreground="blue", font=('Arial', 9, 'underline'),
                              cursor="hand2")
        video_link.pack(anchor='w', pady=5)
        video_link.bind("<Button-1>", lambda e: self.open_video_link())
        
        # Test butonu
        test_btn_frame = ttk.Frame(gmail_frame)
        test_btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(test_btn_frame, text="🔧 Bağlantıyı Test Et", 
                  command=self.test_gmail_connection, width=25).pack()
        
        # URL Yönetimi - TAM GENİŞLİK
        url_frame = ttk.LabelFrame(settings, text="🌐 Hedef URL Yönetimi", padding=15)
        url_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        url_frame.columnconfigure(0, weight=1)
        
        # Üst butonlar
        url_btn_frame = ttk.Frame(url_frame)
        url_btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(url_btn_frame, text="➕ Yeni Site Ekle", 
                  command=self.add_new_url, width=18).pack(side='left', padx=5)
        ttk.Button(url_btn_frame, text="🗑️ Seçili Siteyi Sil", 
                  command=self.delete_selected_url, width=18).pack(side='left', padx=5)
        ttk.Button(url_btn_frame, text="✅ Tümünü Seç", 
                  command=self.select_all_urls, width=15).pack(side='left', padx=5)
        ttk.Button(url_btn_frame, text="❌ Tümünü Kaldır", 
                  command=self.deselect_all_urls, width=15).pack(side='left', padx=5)
        
        # Bilgilendirme
        info_label = ttk.Label(url_frame, 
                              text="💡 Tarama yapılacak siteleri işaretleyin (birden fazla seçebilirsiniz):",
                              foreground="blue", font=('Arial', 10))
        info_label.pack(pady=5)
        
        # URL listesi için scrollable frame
        url_list_frame = ttk.Frame(url_frame)
        url_list_frame.pack(fill='both', expand=True, pady=5)
        
        # Scrollbar
        url_scrollbar = ttk.Scrollbar(url_list_frame)
        url_scrollbar.pack(side='right', fill='y')
        
        # Canvas for scrolling
        self.url_canvas = tk.Canvas(url_list_frame, yscrollcommand=url_scrollbar.set, height=120)
        self.url_canvas.pack(side='left', fill='both', expand=True)
        url_scrollbar.config(command=self.url_canvas.yview)
        
        # Frame içinde checkboxlar
        self.url_checkbox_frame = ttk.Frame(self.url_canvas)
        self.url_canvas.create_window((0, 0), window=self.url_checkbox_frame, anchor='nw')
        
        # Update scroll region
        self.url_checkbox_frame.bind('<Configure>', 
                                     lambda e: self.url_canvas.configure(scrollregion=self.url_canvas.bbox('all')))
        
        # Checkbox'ları oluştur
        self.update_url_checkboxes()
        
        # Tarama Ayarları - TAM GENİŞLİK
        scan_frame = ttk.LabelFrame(settings, text="🔍 Tarama Ayarları", padding=15)
        scan_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        scan_frame.columnconfigure(1, weight=1)
        
        ttk.Label(scan_frame, text="Kaç günde bir gönder:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=8)
        ttk.Spinbox(scan_frame, from_=1, to=30, textvariable=self.resend_days, width=15, font=('Arial', 10)).grid(row=0, column=1, sticky='w', pady=8)
        
        # Checkboxlar
        ttk.Checkbutton(scan_frame, text="🌐 Selenium Kullan (WordPress/Elementor için ŞART!)", 
                       variable=self.use_selenium).grid(row=1, column=0, columnspan=2, sticky='w', pady=5)
        
        ttk.Checkbutton(scan_frame, text="👁️ Tarayıcıyı Göster (Debug için)", 
                       variable=self.show_browser).grid(row=2, column=0, columnspan=2, sticky='w', pady=5)
        
        ttk.Checkbutton(scan_frame, text="🔎 Derin Tarama (Firma detay sayfalarına gir - MOSB için ŞART!)", 
                       variable=self.deep_scan).grid(row=3, column=0, columnspan=2, sticky='w', pady=5)
        
        # Maksimum sayfa
        pages_frame = ttk.Frame(scan_frame)
        pages_frame.grid(row=4, column=0, columnspan=2, sticky='w', pady=8)
        ttk.Label(pages_frame, text="Maksimum sayfa:", font=('Arial', 10)).pack(side='left', padx=5)
        ttk.Spinbox(pages_frame, from_=10, to=1000, textvariable=self.max_pages, width=15, font=('Arial', 10)).pack(side='left', padx=5)
        ttk.Label(pages_frame, text="(Derin tarama için)", foreground='gray', font=('Arial', 9)).pack(side='left', padx=5)
        
        # Tarayıcı seçimi
        browser_frame = ttk.Frame(scan_frame)
        browser_frame.grid(row=5, column=0, columnspan=2, sticky='w', pady=8)
        
        ttk.Label(browser_frame, text="🌐 Tarayıcı:", font=('Arial', 10)).pack(side='left', padx=5)
        self.browser_dropdown = ttk.Combobox(browser_frame, textvariable=self.selected_browser, 
                                            state='readonly', width=20, font=('Arial', 10))
        self.browser_dropdown['values'] = ["Auto (Otomatik)", "Edge", "Chrome", "Firefox"]
        self.browser_dropdown.pack(side='left', padx=5)
        
        # KAYDET BUTONU - Ortalanmış ve Büyük
        save_frame = ttk.Frame(settings)
        save_frame.grid(row=3, column=0, sticky='ew', padx=10, pady=20)
        
        ttk.Button(save_frame, text="💾 AYARLARI KAYDET", 
                  command=self.save_settings, width=35).pack()
        
        # BİLGİLENDİRME - TAM GENİŞLİK
        info_frame = ttk.LabelFrame(settings, text="ℹ️ Bilgilendirme", padding=15)
        info_frame.grid(row=4, column=0, sticky='ew', padx=10, pady=10)
        info_frame.columnconfigure(0, weight=1)
        
        info_text = """✅ v3.3 - ÇOKLU SİTE TARAMA + DERİN TARAMA

• Birden fazla siteyi aynı anda tarayın
• Checkbox ile istediğiniz siteleri seçin
• Derin tarama: Firma detay sayfalarına girer (MOSB için!)
• Varsayılan: İstanbul Anadolu Yakası OSB & Manisa OSB
• Microsoft Edge, Chrome, Firefox desteği

💡 Kullanım:
   1. URL Yönetimi'nden siteleri seçin (✓)
   2. Ana Panel → "Şimdi Tara" veya "Otomatik Mail Bul"
   3. Seçili tüm siteler taranır!"""
        
        ttk.Label(info_frame, text=info_text, justify='left', 
                 foreground='blue', font=('Arial', 9)).pack(padx=10, pady=5, fill='x')
        
    def create_logs_tab(self, notebook):
        """Loglar"""
        logs = ttk.Frame(notebook)
        notebook.add(logs, text='📜 Loglar')
        
        self.log_text = scrolledtext.ScrolledText(logs, wrap=tk.WORD, 
                                                  font=('Consolas', 9), 
                                                  bg='#1e1e1e', fg='#00ff00')
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        btn_frame = ttk.Frame(logs)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(btn_frame, text="🗑️ Temizle", 
                  command=lambda: self.log_text.delete('1.0', tk.END)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="💾 Kaydet", 
                  command=self.save_logs).pack(side='left', padx=5)
    
    # YENİ: URL yönetim fonksiyonları
    def update_url_checkboxes(self):
        """URL checkbox listesini güncelle"""
        # Eski widget'ları temizle
        for widget in self.url_checkbox_frame.winfo_children():
            widget.destroy()
        
        # Yeni checkbox'lar oluştur
        self.url_checkboxes = {}
        
        for i, (name, url) in enumerate(self.saved_urls.items()):
            var = tk.BooleanVar(value=False)
            self.url_checkboxes[name] = var
            
            frame = ttk.Frame(self.url_checkbox_frame)
            frame.pack(fill='x', padx=5, pady=2)
            
            cb = ttk.Checkbutton(frame, text=name, variable=var, width=40)
            cb.pack(side='left')
            
            url_label = ttk.Label(frame, text=url, foreground="gray", font=('Arial', 8))
            url_label.pack(side='left', padx=10)
    
    def select_all_urls(self):
        """Tüm URL'leri seç"""
        for var in self.url_checkboxes.values():
            var.set(True)
        self.log("✅ Tüm siteler seçildi")
    
    def deselect_all_urls(self):
        """Tüm seçimleri kaldır"""
        for var in self.url_checkboxes.values():
            var.set(False)
        self.log("❌ Tüm seçimler kaldırıldı")
    
    def get_selected_urls(self):
        """Seçili URL'leri al"""
        selected = []
        for name, var in self.url_checkboxes.items():
            if var.get():
                if name in self.saved_urls:
                    selected.append((name, self.saved_urls[name]))
        return selected
    
    def delete_selected_url(self):
        """Seçili URL'leri sil"""
        selected_names = [name for name, var in self.url_checkboxes.items() if var.get()]
        
        if not selected_names:
            messagebox.showwarning("Uyarı", "Silmek için site seçin!")
            return
        
        if messagebox.askyesno("Onay", f"{len(selected_names)} site silinsin mi?"):
            for name in selected_names:
                if name in self.saved_urls:
                    del self.saved_urls[name]
            
            self.save_saved_urls()
            self.update_url_checkboxes()
            self.log(f"🗑️ {len(selected_names)} site silindi")
    
    def open_video_link(self):
        """Gmail uygulama şifresi video linkini aç"""
        import webbrowser
        video_url = "https://www.youtube.com/results?search_query=How+to+Generate+App+Password+in+Gmail"
        webbrowser.open(video_url)
        self.log("🎥 Video açıldı")
    
    def add_new_url(self):
        """Yeni URL ekle"""
        # İsim sor
        name_dialog = tk.Toplevel(self.root)
        name_dialog.title("Yeni Site Ekle")
        name_dialog.geometry("400x200")
        name_dialog.transient(self.root)
        name_dialog.grab_set()
        
        ttk.Label(name_dialog, text="Site İsmi:", font=('Arial', 11)).pack(pady=10)
        name_entry = ttk.Entry(name_dialog, width=40)
        name_entry.pack(pady=5)
        
        ttk.Label(name_dialog, text="Site URL:", font=('Arial', 11)).pack(pady=10)
        url_entry = ttk.Entry(name_dialog, width=40)
        url_entry.pack(pady=5)
        
        def save_new_url():
            name = name_entry.get().strip()
            url = url_entry.get().strip()
            
            if not name or not url:
                messagebox.showwarning("Uyarı", "İsim ve URL girin!")
                return
            
            if name in self.saved_urls:
                if not messagebox.askyesno("Uyarı", f"'{name}' zaten var. Üzerine yaz?"):
                    return
            
            self.saved_urls[name] = url
            self.save_saved_urls()
            self.update_url_checkboxes()
            
            self.log(f"✅ Yeni site eklendi: {name}")
            name_dialog.destroy()
        
        ttk.Button(name_dialog, text="💾 Kaydet", command=save_new_url).pack(pady=15)
    
    def delete_url(self):
        """Seçili URL'yi sil"""
        name = self.selected_url_name.get()
        if not name:
            messagebox.showwarning("Uyarı", "Site seçin!")
            return
        
        if messagebox.askyesno("Onay", f"'{name}' silinsin mi?"):
            del self.saved_urls[name]
            self.save_saved_urls()
            self.update_url_dropdown()
            self.log(f"🗑️ Site silindi: {name}")
        
    def log(self, message, level="INFO"):
        """Log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        print(log_message.strip())
        
    def refresh_email_list(self):
        """Listeyi yenile"""
        self.email_listbox.delete(0, tk.END)
        
        self.cursor.execute('SELECT email, collected_date FROM email_pool ORDER BY collected_date DESC')
        emails = self.cursor.fetchall()
        
        for email, date in emails:
            self.cursor.execute(
                'SELECT COUNT(*) FROM send_history WHERE email = ? AND status = "success"',
                (email,)
            )
            sent_count = self.cursor.fetchone()[0]
            
            status = f"✅({sent_count})" if sent_count > 0 else "⏳"
            self.email_listbox.insert(tk.END, f"{status} {email}")
        
        total_count = len(emails)
        self.cursor.execute('SELECT COUNT(DISTINCT email) FROM send_history WHERE status = "success"')
        sent_count = self.cursor.fetchone()[0]
        
        self.email_count_label.config(text=f"📧 Toplam: {total_count}")
        self.sent_count_label.config(text=f"📤 Gönderilen: {sent_count}")
    
    def delete_selected_emails(self):
        """Seçilileri sil"""
        selections = self.email_listbox.curselection()
        if not selections:
            messagebox.showwarning("Uyarı", "Mail seçin!")
            return
        
        emails_to_delete = []
        for selection in selections:
            email_text = self.email_listbox.get(selection)
            parts = email_text.split()
            for part in parts:
                if '@' in part:
                    emails_to_delete.append(part)
                    break
        
        if messagebox.askyesno("Onay", f"{len(emails_to_delete)} mail silinsin mi?"):
            for email in emails_to_delete:
                self.cursor.execute('DELETE FROM email_pool WHERE email = ?', (email,))
                self.cursor.execute('DELETE FROM send_history WHERE email = ?', (email,))
            
            self.conn.commit()
            self.log(f"🗑️ {len(emails_to_delete)} mail silindi")
            self.refresh_email_list()
    
    def delete_all_emails(self):
        """Tümünü sil"""
        self.cursor.execute('SELECT COUNT(*) FROM email_pool')
        count = self.cursor.fetchone()[0]
        
        if count == 0:
            messagebox.showinfo("Bilgi", "Liste zaten boş!")
            return
        
        if messagebox.askyesno("UYARI", f"{count} mail silinecek!\n\nEmin misiniz?"):
            if messagebox.askyesno("SON UYARI", "GERİ ALINAMAZ!\n\nDevam?"):
                self.cursor.execute('DELETE FROM email_pool')
                self.cursor.execute('DELETE FROM send_history')
                self.conn.commit()
                
                self.log(f"🗑️ {count} mail silindi!")
                messagebox.showinfo("Tamam", f"{count} mail silindi!")
                self.refresh_email_list()
    
    def import_from_excel(self):
        """Excel'den aktar"""
        file_path = filedialog.askopenfilename(
            title="Excel Seç",
            filetypes=[("Excel", "*.xlsx *.xls"), ("All", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            self.log(f"📊 Excel açılıyor: {os.path.basename(file_path)}")
            
            workbook = openpyxl.load_workbook(file_path, data_only=True)
            sheet = workbook.active
            
            email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
            emails_found = set()
            
            for row in sheet.iter_rows(values_only=True):
                for cell in row:
                    if cell and isinstance(cell, str):
                        found = email_pattern.findall(cell)
                        for email in found:
                            emails_found.add(email.lower().strip())
            
            workbook.close()
            
            if not emails_found:
                messagebox.showwarning("Uyarı", "Mail bulunamadı!")
                return
            
            new_count = 0
            for email in emails_found:
                try:
                    self.cursor.execute(
                        'INSERT OR IGNORE INTO email_pool (email, source_url) VALUES (?, ?)',
                        (email, f'Excel: {os.path.basename(file_path)}')
                    )
                    if self.cursor.rowcount > 0:
                        new_count += 1
                except Exception as e:
                    self.log(f"❌ {email}: {e}", "ERROR")
            
            self.conn.commit()
            
            self.log(f"✅ Excel: {len(emails_found)} bulundu, {new_count} yeni")
            messagebox.showinfo("Başarılı", f"✅ {new_count} yeni mail eklendi!")
            
            self.refresh_email_list()
            
        except Exception as e:
            self.log(f"❌ Excel hatası: {e}", "ERROR")
            messagebox.showerror("Hata", f"Excel okunamadı:\n{e}")
            
    def export_emails(self):
        """Dışa aktar"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("CSV", "*.csv"), ("All", "*.*")]
        )
        
        if file_path:
            self.cursor.execute('SELECT email FROM email_pool')
            emails = self.cursor.fetchall()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                for email in emails:
                    f.write(email[0] + '\n')
            
            messagebox.showinfo("Tamam", f"{len(emails)} mail kaydedildi!")
            self.log(f"📤 {len(emails)} mail → {file_path}")
            
    def select_pdf(self):
        """PDF seç"""
        file_path = filedialog.askopenfilename(
            title="CV PDF",
            filetypes=[("PDF", "*.pdf"), ("All", "*.*")]
        )
        
        if file_path:
            self.pdf_path = file_path
            filename = os.path.basename(file_path)
            self.pdf_status_label.config(text=f"📄 {filename}", foreground="green")
            self.log(f"📎 PDF: {filename}")
            # Otomatik kaydet
            self.auto_save_settings()
    
    # YENİ: Tarama durumu güncelleme fonksiyonları
    def update_scan_status(self, status_text, details_text="", color="blue"):
        """Tarama durumunu güncelle"""
        self.scan_progress_label.config(text=status_text, foreground=color)
        if details_text:
            self.scan_details_label.config(text=details_text)
        self.root.update()
    
    def start_scan(self):
        """Taramayı başlat"""
        if self.scanning:
            messagebox.showwarning("Uyarı", "Tarama zaten aktif!")
            return
        
        # Seçili URL'leri al
        selected_urls = self.get_selected_urls()
        
        if not selected_urls:
            messagebox.showwarning("Uyarı", "Taranacak site seçin!\n\nAyarlar → URL Yönetimi'nden en az bir site seçmelisiniz.")
            return
        
        # Derin tarama uyarısı
        if self.deep_scan.get():
            max_pages = self.max_pages.get()
            estimated_time = max_pages * 0.5  # Her sayfa yaklaşık 30 saniye
            minutes = int(estimated_time)
            
            message = f"⚠️ DERİN TARAMA MODU AÇIK ⚠️\n\n"
            message += f"• Maksimum {max_pages} sayfa taranacak\n"
            message += f"• Tahmini süre: {minutes} dakika\n\n"
            message += f"Bu işlem uzun sürebilir.\n"
            message += f"Lütfen tarama tamamlanana kadar bekleyin.\n\n"
            message += f"Devam edilsin mi?"
            
            if not messagebox.askyesno("Uzun İşlem Uyarısı", message):
                return
        
        # Tarama durumunu sıfırla
        self.emails_found_count.set(0)
        
        mode = "SELENIUM" if self.use_selenium.get() else "REQUESTS"
        browser = self.get_best_browser() if self.use_selenium.get() else "N/A"
        browser_mode = "GÖRÜNÜR" if self.show_browser.get() else "HEADLESS"
        
        self.update_scan_status(
            f"🔍 Tarama başlatılıyor...",
            f"{len(selected_urls)} site | {mode} ({browser} - {browser_mode})",
            "orange"
        )
        
        self.scanning = True
        self.scan_btn.config(state='disabled')
        self.stop_scan_btn.config(state='normal')
        
        # Çoklu URL tarama thread
        thread = threading.Thread(target=self._multi_scan_thread, 
                                 args=(selected_urls,), daemon=True)
        thread.start()
        
    def stop_scan(self):
        """Durdur"""
        self.scanning = False
        self.scan_btn.config(state='normal')
        self.stop_scan_btn.config(state='disabled')
        self.update_scan_status("⏹️ Durduruldu", "", "red")
        self.log("⏹️ Durduruldu")
        
    def toggle_auto_scan(self):
        """Otomatik tarama"""
        if not self.auto_scan_active:
            self.auto_scan_active = True
            self.auto_scan_btn.config(text="⏸️ Durdur")
            self.scan_btn.config(state='disabled')
            self.log("🤖 Otomatik başlatıldı (30 dk)")
            
            self.start_scan()
            self.start_auto_scan_timer()
        else:
            self.auto_scan_active = False
            self.auto_scan_btn.config(text="🤖 Otomatik Mail Bul")
            self.scan_btn.config(state='normal')
            self.timer_label.config(text="")
            
            if self.auto_scan_timer:
                self.root.after_cancel(self.auto_scan_timer)
            
            self.log("⏸️ Otomatik durduruldu")
    
    def start_auto_scan_timer(self):
        """Otomatik timer"""
        self.auto_scan_remaining_seconds = 30 * 60
        self.update_timer()
    
    def update_timer(self):
        """Timer güncelle"""
        if not self.auto_scan_active:
            return
        
        if self.auto_scan_remaining_seconds > 0:
            minutes = self.auto_scan_remaining_seconds // 60
            seconds = self.auto_scan_remaining_seconds % 60
            self.timer_label.config(text=f"⏰ Sonraki tarama: {minutes:02d}:{seconds:02d}")
            
            self.auto_scan_remaining_seconds -= 1
            self.auto_scan_timer = self.root.after(1000, self.update_timer)
        else:
            self.log("🤖 Otomatik tarama başlıyor...")
            self.start_scan()
            self.start_auto_scan_timer()
    
    def _multi_scan_thread(self, selected_urls):
        """Çoklu site tarama thread"""
        try:
            total_emails = set()
            total_new = 0
            
            self.log("="*60)
            self.log(f"🔍 ÇOKLU SİTE TARAMA BAŞLADI")
            self.log(f"📍 {len(selected_urls)} site taranacak")
            self.log("="*60)
            
            for idx, (site_name, site_url) in enumerate(selected_urls, 1):
                if not self.scanning:
                    self.log("⏹️ Kullanıcı taramayı durdurdu")
                    break
                
                self.log("")
                self.log("="*60)
                self.log(f"[{idx}/{len(selected_urls)}] 📍 {site_name}")
                self.log(f"🌐 {site_url}")
                self.log("="*60)
                
                self.update_scan_status(
                    f"🔍 [{idx}/{len(selected_urls)}] {site_name} taranıyor...",
                    f"Toplam {len(total_emails)} mail bulundu",
                    "green"
                )
                
                # Tek site tara
                try:
                    emails_found = self._scan_single_site(site_url, site_name)
                    
                    # Veritabanına kaydet
                    new_count = 0
                    for email in emails_found:
                        try:
                            self.cursor.execute(
                                'INSERT OR IGNORE INTO email_pool (email, source_url) VALUES (?, ?)',
                                (email, f"{site_name}: {site_url}")
                            )
                            if self.cursor.rowcount > 0:
                                new_count += 1
                                total_new += 1
                        except:
                            pass
                    
                    self.conn.commit()
                    total_emails.update(emails_found)
                    
                    self.log(f"✅ {site_name}: {len(emails_found)} mail | Yeni: {new_count}")
                    
                except Exception as e:
                    self.log(f"❌ {site_name} tarama hatası: {e}", "ERROR")
                    continue
            
            self.log("")
            self.log("="*60)
            self.log(f"✅ TÜM TARAMALAR TAMAMLANDI!")
            self.log(f"📊 {len(selected_urls)} site tarandı")
            self.log(f"📧 Toplam: {len(total_emails)} mail | Yeni: {total_new}")
            self.log("="*60)
            
            self.update_scan_status(
                f"✅ Tarama tamamlandı!",
                f"{len(selected_urls)} site | {len(total_emails)} mail bulundu | {total_new} yeni",
                "green"
            )
            
            if total_new > 0:
                messagebox.showinfo("Başarılı", f"✅ {total_new} yeni mail eklendi!\n📍 {len(selected_urls)} site tarandı")
            else:
                messagebox.showinfo("Bilgi", f"Yeni mail bulunamadı.\n📍 {len(selected_urls)} site tarandı")
            
            self.refresh_email_list()
            
        except Exception as e:
            self.log(f"❌ Çoklu tarama hatası: {e}", "ERROR")
            self.update_scan_status("❌ Hata oluştu!", str(e), "red")
            messagebox.showerror("Hata", f"Tarama başarısız:\n{e}")
        finally:
            self.scanning = False
            self.scan_btn.config(state='normal')
            self.stop_scan_btn.config(state='disabled')
    
    def _scan_single_site(self, base_url, site_name="Site"):
        """Tek bir site tara"""
        # Selenium veya Requests seç
        if self.use_selenium.get():
            self.log(f"🌐 SELENIUM ile taranıyor...")
            return self._selenium_scan(base_url)
        else:
            self.log(f"📡 REQUESTS ile taranıyor...")
            return self._requests_scan(base_url)
    
    def _scan_thread(self):
        """Ana tarama thread (eski versiyon - geriye dönük uyumluluk için)"""
        try:
            base_url = self.base_url.get()
            
            # URL'den site ismini çıkar
            parsed_url = urlparse(base_url)
            site_name = parsed_url.netloc
            
            self.log("="*60)
            self.log(f"🔍 TARAMA BAŞLADI: {base_url}")
            self.log("="*60)
            
            self.update_scan_status(
                f"🔍 {site_name} taranıyor...",
                "Mail adresleri aranıyor...",
                "green"
            )
            
            # Selenium veya Requests seç
            if self.use_selenium.get():
                self.log("="*60)
                self.log("🌐 SELENIUM TARAMA")
                self.log("="*60)
                emails_found = self._selenium_scan(base_url)
            else:
                self.log("="*60)
                self.log("📡 REQUESTS TARAMA")
                self.log("="*60)
                emails_found = self._requests_scan(base_url)
            
            # Veritabanına kaydet
            new_count = 0
            for email in emails_found:
                try:
                    self.cursor.execute(
                        'INSERT OR IGNORE INTO email_pool (email, source_url) VALUES (?, ?)',
                        (email, base_url)
                    )
                    if self.cursor.rowcount > 0:
                        new_count += 1
                        self.emails_found_count.set(self.emails_found_count.get() + 1)
                        # Her yeni mail eklendiğinde durumu güncelle
                        self.update_scan_status(
                            f"🔍 {site_name} taranıyor...",
                            f"✅ {self.emails_found_count.get()} mail bulundu",
                            "green"
                        )
                except:
                    pass
            
            self.conn.commit()
            
            self.log("="*60)
            self.log(f"✅ TARAMA TAMAMLANDI!")
            self.log(f"📧 Toplam: {len(emails_found)} | Yeni: {new_count}")
            self.log("="*60)
            
            self.update_scan_status(
                f"✅ Tarama tamamlandı!",
                f"{len(emails_found)} mail bulundu, {new_count} yeni eklendi",
                "green"
            )
            
            if new_count > 0:
                messagebox.showinfo("Başarılı", f"✅ {new_count} yeni mail eklendi!")
            else:
                messagebox.showinfo("Bilgi", "Yeni mail bulunamadı.")
            
            self.refresh_email_list()
            
        except Exception as e:
            self.log(f"❌ Tarama hatası: {e}", "ERROR")
            self.update_scan_status("❌ Hata oluştu!", str(e), "red")
            messagebox.showerror("Hata", f"Tarama başarısız:\n{e}")
        finally:
            self.scanning = False
            self.scan_btn.config(state='normal')
            self.stop_scan_btn.config(state='disabled')
    
    def _selenium_scan(self, base_url):
        """Selenium ile tara"""
        emails = set()
        driver = None
        
        try:
            browser_name = self.get_best_browser()
            
            if not browser_name:
                raise Exception("Kullanılabilir tarayıcı yok!")
            
            self.log(f"🌐 {browser_name} başlatılıyor...")
            
            # Browser'a göre ayarlar
            if browser_name == "Edge":
                options = EdgeOptions()
                if not self.show_browser.get():
                    options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                
                driver_path = self.driver_paths.get("Edge")
                if driver_path:
                    service = EdgeService(driver_path)
                    driver = webdriver.Edge(service=service, options=options)
                else:
                    driver = webdriver.Edge(options=options)
                    
            elif browser_name == "Chrome":
                options = ChromeOptions()
                if not self.show_browser.get():
                    options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                
                driver_path = self.driver_paths.get("Chrome")
                if driver_path:
                    service = ChromeService(driver_path)
                    driver = webdriver.Chrome(service=service, options=options)
                else:
                    driver = webdriver.Chrome(options=options)
                    
            elif browser_name == "Firefox":
                options = FirefoxOptions()
                if not self.show_browser.get():
                    options.add_argument('--headless')
                
                driver_path = self.driver_paths.get("Firefox")
                if driver_path:
                    service = FirefoxService(driver_path)
                    driver = webdriver.Firefox(service=service, options=options)
                else:
                    driver = webdriver.Firefox(options=options)
            
            self.log(f"✅ {browser_name} başlatıldı")
            
            # DERIN TARAMA MOD
            if self.deep_scan.get():
                self.log("="*60)
                self.log("🔎 DERİN TARAMA MODU AÇIK")
                self.log(f"📄 Maksimum {self.max_pages.get()} sayfa taranacak")
                self.log("="*60)
                
                emails = self._deep_scan_with_driver(driver, base_url)
            else:
                # Normal tek sayfa tarama
                self.log(f"🌐 Sayfa yükleniyor: {base_url}")
                
                driver.get(base_url)
                
                # Sayfanın yüklenmesini bekle
                time.sleep(5)
                
                # JavaScript ile yüklenen içeriği bekle
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                except:
                    pass
                
                # ULTRA AGRESIF SCROLL - MOSB gibi siteler için
                self.log("📜 Sayfa kaydırılıyor (infinite scroll için)...")
                
                last_height = driver.execute_script("return document.body.scrollHeight")
                scroll_count = 0
                max_scrolls = 100  # MOSB için artırıldı
                no_change_count = 0
                
                # MOSB için özel: "Load More" butonlarını kontrol et
                load_more_clicked = 0
                
                while scroll_count < max_scrolls:
                    # Önce "Load More" / "Daha Fazla" butonlarını ara ve tıkla
                    try:
                        load_more_buttons = driver.find_elements(By.XPATH, 
                            "//button[contains(text(), 'Daha') or contains(text(), 'Load') or contains(text(), 'More') or contains(@class, 'load-more')]")
                        
                        for btn in load_more_buttons:
                            if btn.is_displayed() and btn.is_enabled():
                                try:
                                    driver.execute_script("arguments[0].scrollIntoView();", btn)
                                    time.sleep(0.5)
                                    btn.click()
                                    load_more_clicked += 1
                                    self.log(f"   🔘 'Daha Fazla' butonu tıklandı ({load_more_clicked})")
                                    time.sleep(3)  # Yeni içeriğin yüklenmesi için bekle
                                except:
                                    pass
                    except:
                        pass
                    
                    # En alta scroll yap
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    scroll_count += 1
                    
                    # MOSB için daha uzun bekleme
                    time.sleep(3)  # 2'den 3'e artırıldı
                    
                    # Yeni yüksekliği kontrol et
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    
                    if new_height == last_height:
                        # Yükseklik değişmedi, ama belki yavaş yükleniyor
                        no_change_count += 1
                        if no_change_count >= 5:  # 3'ten 5'e artırıldı - daha sabırlı
                            self.log(f"✅ Scroll tamamlandı ({scroll_count} kez kaydırıldı)")
                            break
                    else:
                        # Yükseklik değişti, yeni içerik var
                        no_change_count = 0
                        last_height = new_height
                        self.log(f"🔄 Yeni içerik yüklendi (Scroll {scroll_count}/100)")
                
                if scroll_count >= max_scrolls:
                    self.log(f"⚠️ Maksimum scroll limitine ulaşıldı ({max_scrolls})")
                
                # Son bir kez daha bekle
                time.sleep(2)
                
                # Sayfa kaynağını al
                page_source = driver.page_source
                
                # Email pattern
                email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
                found = email_pattern.findall(page_source)
                
                # Email validation ile filtrele
                for email in found:
                    clean_email = email.lower().strip()
                    # Geliştirilmiş validation - dosya uzantılarını ve geçersiz emailleri filtrele
                    if self.is_valid_email(clean_email):
                        emails.add(clean_email)
                        self.log(f"📧 {clean_email}")
                    else:
                        # Geçersiz email'leri logla (debug için)
                        if clean_email.count('@') == 1:  # @ içeriyorsa ama geçersizse logla
                            self.log(f"⚠️ Filtrelendi (dosya/geçersiz): {clean_email}", "WARNING")
            
            self.log(f"✅ Selenium tarama tamamlandı: {len(emails)} mail")
            
        except Exception as e:
            self.log(f"❌ Selenium hatası: {e}", "ERROR")
            raise
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
        
        return emails
    
    def _deep_scan_with_driver(self, driver, base_url):
        """Derin tarama - tüm alt sayfaları ziyaret et (RAM-OPTIMIZE)"""
        emails = set()
        visited_urls = set()
        urls_to_visit = [base_url]
        
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        base_domain = urlparse(base_url).netloc
        
        max_pages = self.max_pages.get()
        page_count = 0
        
        # Driver restart için
        browser_name = self.get_best_browser()
        driver_restart_interval = 75  # Her 75 sayfada bir driver'ı yeniden başlat
        
        while urls_to_visit and page_count < max_pages and self.scanning:
            # Her 75 sayfada bir driver'ı yeniden başlat (RAM için)
            if page_count > 0 and page_count % driver_restart_interval == 0:
                self.log(f"🔄 Driver yeniden başlatılıyor (RAM optimizasyonu - {page_count} sayfa)")
                
                try:
                    driver.quit()
                    gc.collect()  # Garbage collection
                    time.sleep(3)
                    
                    # Driver'ı yeniden başlat
                    if browser_name == "Edge":
                        from selenium.webdriver.edge.options import Options as EdgeOptions
                        from selenium.webdriver.edge.service import Service as EdgeService
                        options = EdgeOptions()
                        if not self.show_browser.get():
                            options.add_argument('--headless')
                        options.add_argument('--disable-gpu')
                        options.add_argument('--no-sandbox')
                        options.add_argument('--disable-dev-shm-usage')
                        
                        driver_path = self.driver_paths.get("Edge")
                        if driver_path:
                            service = EdgeService(driver_path)
                            driver = webdriver.Edge(service=service, options=options)
                        else:
                            driver = webdriver.Edge(options=options)
                    
                    elif browser_name == "Chrome":
                        from selenium.webdriver.chrome.options import Options as ChromeOptions
                        from selenium.webdriver.chrome.service import Service as ChromeService
                        options = ChromeOptions()
                        if not self.show_browser.get():
                            options.add_argument('--headless')
                        options.add_argument('--disable-gpu')
                        options.add_argument('--no-sandbox')
                        options.add_argument('--disable-dev-shm-usage')
                        
                        driver_path = self.driver_paths.get("Chrome")
                        if driver_path:
                            service = ChromeService(driver_path)
                            driver = webdriver.Chrome(service=service, options=options)
                        else:
                            driver = webdriver.Chrome(options=options)
                    
                    elif browser_name == "Firefox":
                        from selenium.webdriver.firefox.options import Options as FirefoxOptions
                        from selenium.webdriver.firefox.service import Service as FirefoxService
                        options = FirefoxOptions()
                        if not self.show_browser.get():
                            options.add_argument('--headless')
                        
                        driver_path = self.driver_paths.get("Firefox")
                        if driver_path:
                            service = FirefoxService(driver_path)
                            driver = webdriver.Firefox(service=service, options=options)
                        else:
                            driver = webdriver.Firefox(options=options)
                    
                    self.log(f"✅ Driver yeniden başlatıldı")
                except Exception as e:
                    self.log(f"⚠️ Driver restart hatası: {e}", "WARNING")
            current_url = urls_to_visit.pop(0)
            
            if current_url in visited_urls:
                continue
            
            try:
                page_count += 1
                visited_urls.add(current_url)
                
                self.log(f"[{page_count}/{max_pages}] 🔍 {current_url}")
                self.update_scan_status(
                    f"🔎 Derin tarama devam ediyor...",
                    f"{page_count}/{max_pages} sayfa | {len(emails)} mail bulundu",
                    "green"
                )
                
                driver.get(current_url)
                time.sleep(2)
                
                # İLK SAYFA İÇİN ÖZEL: RAM-OPTİMİZE AGRESİF SCROLL (2 geçiş)
                if page_count == 1:
                    self.log("   📜 RAM-OPTİMİZE AGRESİF SCROLL başlatılıyor (2 geçiş)...")
                    
                    # JavaScript scroll event tetikleyici fonksiyon
                    trigger_scroll_js = """
                        window.dispatchEvent(new Event('scroll'));
                        document.dispatchEvent(new Event('scroll'));
                    """
                    
                    # PASS 1: Akıllı aşağı scroll (RAM-efficient)
                    self.log("   🔄 GEÇİŞ 1/2: Akıllı aşağı scroll...")
                    last_height = driver.execute_script("return document.body.scrollHeight")
                    scroll_count = 0
                    max_scrolls = 120  # 150'den 120'ye düşürüldü - RAM için
                    no_change_count = 0
                    load_more_clicked = 0
                    
                    # Link elementlerini say
                    initial_link_count = len(driver.find_elements(By.TAG_NAME, "a"))
                    self.log(f"   📊 Başlangıç link sayısı: {initial_link_count}")
                    
                    while scroll_count < max_scrolls:
                        # Her 20 scroll'da bir RAM temizliği
                        if scroll_count > 0 and scroll_count % 20 == 0:
                            gc.collect()  # Garbage collection
                            self.log(f"   🧹 RAM temizliği yapıldı (Scroll {scroll_count})")
                        
                        # Load More butonlarını her 10 scrollda bir kontrol et (RAM için optimize)
                        if scroll_count % 10 == 0:
                            try:
                                # Daha az selector - RAM için
                                load_more_selectors = [
                                    "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'daha')]",
                                    "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'load')]",
                                    "//*[contains(@class, 'load-more')]",
                                    "//*[contains(@class, 'show-more')]"
                                ]
                                
                                for selector in load_more_selectors:
                                    try:
                                        buttons = driver.find_elements(By.XPATH, selector)
                                        for btn in buttons[:1]:  # Sadece ilk butona tıkla - RAM için
                                            if btn.is_displayed() and btn.is_enabled():
                                                try:
                                                    driver.execute_script("arguments[0].click();", btn)
                                                    load_more_clicked += 1
                                                    self.log(f"   🔘 Buton tıklandı! (#{load_more_clicked})")
                                                    time.sleep(3)
                                                    driver.execute_script(trigger_scroll_js)
                                                    break  # Bir buton yeterli
                                                except:
                                                    pass
                                    except:
                                        continue
                            except:
                                pass
                        
                        # Scroll yap - sadece instant (smooth RAM'i doldurur)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        driver.execute_script(trigger_scroll_js)
                        
                        scroll_count += 1
                        time.sleep(3.5)  # 4'ten 3.5'e düşürüldü - biraz hız için
                        
                        new_height = driver.execute_script("return document.body.scrollHeight")
                        
                        # Her 30 scroll'da bir link sayısını kontrol et
                        if scroll_count % 30 == 0:
                            current_link_count = len(driver.find_elements(By.TAG_NAME, "a"))
                            self.log(f"   🔄 İçerik yükleniyor... (Scroll {scroll_count}, {current_link_count} link)")
                        
                        if new_height == last_height:
                            no_change_count += 1
                            if no_change_count >= 6:  # 7'den 6'ya düşürüldü
                                final_link_count = len(driver.find_elements(By.TAG_NAME, "a"))
                                self.log(f"   ✅ Geçiş 1 tamamlandı ({scroll_count} scroll, {final_link_count} link)")
                                break
                        else:
                            no_change_count = 0
                            last_height = new_height
                    
                    # GEÇİŞ 1 sonrası RAM temizliği
                    gc.collect()
                    self.log("   🧹 Geçiş 1 sonrası RAM temizliği")
                    
                    # PASS 2: Hızlı tekrar scroll (double-check) - 3. geçişi kaldırdık
                    self.log("   🔄 GEÇİŞ 2/2: Hızlı double-check...")
                    
                    # Yukarı-aşağı 3 kez (10 yerine 3)
                    for i in range(3):
                        driver.execute_script("window.scrollTo(0, 0);")  # Üste
                        time.sleep(1)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Alta
                        time.sleep(1)
                        driver.execute_script(trigger_scroll_js)
                    
                    final_link_count = len(driver.find_elements(By.TAG_NAME, "a"))
                    self.log(f"   ✅ 2 GEÇİŞ TAMAMLANDI!")
                    self.log(f"   📊 Başlangıç: {initial_link_count} link → Final: {final_link_count} link")
                    self.log(f"   ➕ Artış: +{final_link_count - initial_link_count} link")
                    
                    # Final RAM temizliği
                    gc.collect()
                    time.sleep(2)
                else:
                    # FİRMA DETAY SAYFALARI İÇİN AGRESİF SCROLL
                    # JavaScript ile yüklenen içerik için daha uzun bekleme
                    self.log(f"   📜 Firma detay sayfası scroll ediliyor...")
                    
                    # İlk scroll - sayfanın yüklenmesini bekle
                    time.sleep(2)  # Sayfa yüklenmesi için ekstra bekleme
                    
                    # Agresif scroll - 5 tur
                    for scroll_round in range(5):
                        # Alta scroll
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)  # JavaScript yüklenmesi için daha uzun bekleme
                        
                        # Üste scroll
                        driver.execute_script("window.scrollTo(0, 0);")
                        time.sleep(1)
                    
                    # Son bir kez alta scroll ve bekle
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)  # Mail yüklenmesi için ekstra bekleme
                    
                    self.log(f"   ✅ Scroll tamamlandı")
                
                # YÖNTEM 1: Page source ile mail bul
                page_source = driver.page_source
                found_emails = email_pattern.findall(page_source)
                
                # YÖNTEM 2: Visible text ile mail bul (daha güvenilir)
                try:
                    body_text = driver.find_element(By.TAG_NAME, "body").text
                    visible_emails = email_pattern.findall(body_text)
                    found_emails.extend(visible_emails)
                except:
                    pass
                
                # YÖNTEM 3: mailto: linklerinden mail bul (hidden emails için)
                try:
                    mailto_links = driver.find_elements(By.XPATH, "//a[starts-with(@href, 'mailto:')]")
                    for link in mailto_links:
                        href = link.get_attribute("href")
                        if href and "mailto:" in href:
                            email_from_mailto = href.replace("mailto:", "").split("?")[0].strip()
                            found_emails.append(email_from_mailto)
                            self.log(f"   📧 mailto: linkten bulundu: {email_from_mailto}")
                except:
                    pass
                
                # YÖNTEM 4: Email input alanlarından value bul
                try:
                    email_inputs = driver.find_elements(By.XPATH, "//input[@type='email'] | //input[contains(@name, 'email') or contains(@id, 'email')]")
                    for input_elem in email_inputs:
                        value = input_elem.get_attribute("value")
                        if value and "@" in value:
                            found_emails.append(value)
                            self.log(f"   📧 input'tan bulundu: {value}")
                except:
                    pass
                
                # YÖNTEM 5: Contact/email class/id'li elementlerden mail bul
                try:
                    contact_elements = driver.find_elements(By.XPATH, 
                        "//*[contains(@class, 'email') or contains(@class, 'mail') or contains(@class, 'contact') or " +
                        "contains(@id, 'email') or contains(@id, 'mail') or contains(@id, 'contact')]")
                    for elem in contact_elements:
                        elem_text = elem.text
                        if elem_text and "@" in elem_text:
                            contact_emails = email_pattern.findall(elem_text)
                            found_emails.extend(contact_emails)
                except:
                    pass
                
                # Mail bul - tüm yöntemlerden gelen mailleri işle
                page_emails_found = 0
                filtered_emails_debug = []
                
                for email in found_emails:
                    clean_email = email.lower().strip()
                    # Geçersiz karakterleri temizle
                    clean_email = re.sub(r'[<>"\']', '', clean_email)
                    
                    # Geliştirilmiş validation - dosya uzantılarını ve geçersiz emailleri filtrele
                    if self.is_valid_email(clean_email):
                        if clean_email not in emails:
                            emails.add(clean_email)
                            page_emails_found += 1
                            self.log(f"   📧 {clean_email}")
                            self.emails_found_count.set(len(emails))
                    else:
                        # Geçersiz email'leri logla - DETAYLI DEBUG
                        if clean_email.count('@') == 1:
                            filtered_emails_debug.append(clean_email)
                
                # Debug: Filtrelenen mailleri göster
                if filtered_emails_debug:
                    self.log(f"   ⚠️ FİLTRELENEN MAILLER ({len(filtered_emails_debug)}):", "WARNING")
                    for filtered_email in filtered_emails_debug[:10]:  # İlk 10 tanesini göster
                        self.log(f"      • {filtered_email}", "WARNING")
                
                # Debug: Eğer bu sayfada mail bulunamadıysa logla
                if page_emails_found == 0:
                    self.log(f"   ⚠️ Bu sayfada mail bulunamadı (toplam: {len(found_emails)} email pattern bulundu, {len(filtered_emails_debug)} filtrelendi)", "WARNING")
                
                # Belleği temizle
                page_source = None
                body_text = None
                found_emails = None
                
                # Her 25 sayfada bir garbage collection
                if page_count % 25 == 0:
                    gc.collect()
                    self.log(f"   🧹 RAM temizliği ({page_count} sayfa)")
                
                # Sadece ilk sayfada linkleri topla (firma listesi sayfası)
                if page_count == 1:
                    self.log("   🔗 RAM-OPTİMİZE LİNK TOPLAMA başlatılıyor...")
                    
                    try:
                        # Önce sayfanın en üstüne git
                        driver.execute_script("window.scrollTo(0, 0);")
                        time.sleep(2)
                        
                        all_found_links = set()
                        
                        # YÖNTEM 1: Optimize edilmiş scroll + link toplama
                        self.log("   📜 YÖNTEM 1: Optimize scroll + collect...")
                        
                        scroll_position = 0
                        scroll_step = 500  # 300'den 500'e artırıldı - RAM için
                        max_scroll_height = driver.execute_script("return document.body.scrollHeight")
                        
                        self.log(f"   📊 Sayfa yüksekliği: {max_scroll_height}px")
                        
                        step_count = 0
                        while scroll_position < max_scroll_height:
                            # Scroll yap
                            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                            time.sleep(0.6)  # 0.8'den 0.6'ya düşürüldü - hız için
                            
                            # Her 25 adımda bir link topla (her adımda değil - RAM için)
                            if step_count % 25 == 0:
                                try:
                                    links = driver.find_elements(By.TAG_NAME, "a")
                                    
                                    for link in links:
                                        try:
                                            href = link.get_attribute("href")
                                            
                                            # ÇOKLU SİTE DESTEĞİ - Farklı URL pattern'lerini kontrol et
                                            should_add = False
                                            
                                            if href:
                                                # İAYOSB için /works/
                                                if '/works/' in href:
                                                    should_add = True
                                                # MOSB ve benzer siteler için /firmalar/
                                                elif '/firmalar/' in href or '/firmalarimiz/' in href:
                                                    should_add = True
                                                # İKA MCBU için /Duyuru/ ve /DuyuruArsiv/
                                                elif '/Duyuru/' in href or '/duyuru/' in href:
                                                    should_add = True
                                                elif '/DuyuruArsiv/' in href or '/duyuruarsiv/' in href:
                                                    should_add = True
                                                elif '/Arsiv/' in href or '/arsiv/' in href:
                                                    should_add = True
                                                # Genel firma/şirket/member sayfaları
                                                elif any(pattern in href.lower() for pattern in ['/firma/', '/sirket/', '/member/', '/company/', '/detay/', '/detail/']):
                                                    should_add = True
                                            
                                            if should_add:
                                                parsed = urlparse(href)
                                                
                                                if parsed.netloc == base_domain or not parsed.netloc:
                                                    full_url = urljoin(base_url, href) if not parsed.netloc else href
                                                    clean_url = full_url.split('#')[0].split('?')[0]
                                                    
                                                    if clean_url != base_url:
                                                        all_found_links.add(clean_url)
                                        except:
                                            continue
                                    
                                    # Her 50 adımda bir garbage collection
                                    if step_count % 50 == 0:
                                        gc.collect()
                                except:
                                    pass
                            
                            # Scroll pozisyonunu artır
                            scroll_position += scroll_step
                            step_count += 1
                            
                            # Log her 10000px'de bir (daha az log - RAM için)
                            if scroll_position % 10000 == 0:
                                self.log(f"   🔍 {scroll_position}px tarandı... ({len(all_found_links)} link)")
                        
                        self.log(f"   ✅ Yöntem 1: {len(all_found_links)} link bulundu")
                        
                        # YÖNTEM 2: BeautifulSoup final check (tek yöntem yeterli - RAM için)
                        self.log("   🔗 YÖNTEM 2: BeautifulSoup final check...")
                        
                        # Sayfanın son halini al
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        page_source = driver.page_source
                        
                        try:
                            soup = BeautifulSoup(page_source, 'lxml')
                            all_links = soup.find_all('a', href=True)
                            
                            extra_count = 0
                            for a_tag in all_links:
                                href = a_tag.get('href', '')
                                
                                # ÇOKLU SİTE DESTEĞİ - Farklı URL pattern'lerini kontrol et
                                should_add = False
                                
                                if href:
                                    # İAYOSB için /works/
                                    if '/works/' in href:
                                        should_add = True
                                    # MOSB ve benzer siteler için /firmalar/
                                    elif '/firmalar/' in href or '/firmalarimiz/' in href:
                                        should_add = True
                                    # İKA MCBU için /Duyuru/ ve /DuyuruArsiv/
                                    elif '/Duyuru/' in href or '/duyuru/' in href:
                                        should_add = True
                                    elif '/DuyuruArsiv/' in href or '/duyuruarsiv/' in href:
                                        should_add = True
                                    elif '/Arsiv/' in href or '/arsiv/' in href:
                                        should_add = True
                                    # Genel firma/şirket/member sayfaları
                                    elif any(pattern in href.lower() for pattern in ['/firma/', '/sirket/', '/member/', '/company/', '/detay/', '/detail/']):
                                        should_add = True
                                
                                if should_add:
                                    parsed = urlparse(href)
                                    
                                    if parsed.netloc == base_domain or not parsed.netloc:
                                        full_url = urljoin(base_url, href) if not parsed.netloc else href
                                        clean_url = full_url.split('#')[0].split('?')[0]
                                        
                                        if clean_url != base_url and clean_url not in all_found_links:
                                            all_found_links.add(clean_url)
                                            extra_count += 1
                            
                            if extra_count > 0:
                                self.log(f"   ➕ BeautifulSoup ile {extra_count} ek link bulundu")
                        except Exception as e:
                            self.log(f"   ⚠️ BeautifulSoup hatası: {e}", "WARNING")
                        
                        # Belleği temizle
                        page_source = None
                        soup = None
                        gc.collect()
                        
                        self.log(f"   ✅ Yöntem 2: {len(all_found_links)} link (toplam)")
                        
                        # Toplanan linklerden zaten ziyaret edilmeyenleri ekle
                        new_links = 0
                        for clean_url in all_found_links:
                            if clean_url not in visited_urls and clean_url not in urls_to_visit:
                                urls_to_visit.append(clean_url)
                                new_links += 1
                        
                        self.log("")
                        self.log(f"   ✅ 2 YÖNTEM TAMAMLANDI!")
                        self.log(f"   📊 Toplam benzersiz link: {len(all_found_links)}")
                        self.log(f"   ➕ Ziyaret edilecek: {len(urls_to_visit)} firma")
                        self.log("")
                        
                        # Final cleanup
                        all_found_links.clear()
                        gc.collect()
                        
                    except Exception as e:
                        self.log(f"   ❌ Link toplama hatası: {e}", "ERROR")
                
            except Exception as e:
                self.log(f"   ❌ Sayfa hatası: {e}", "WARNING")
                continue
        
        if page_count >= max_pages:
            self.log(f"⚠️ Maksimum sayfa limitine ulaşıldı ({max_pages})")
        
        return emails
    
    def _requests_scan(self, base_url):
        """Requests ile tara (basit siteler için)"""
        emails = set()
        
        try:
            self.log(f"📡 Sayfa indiriliyor: {base_url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(base_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Email pattern
            email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
            found = email_pattern.findall(response.text)
            
            # Email validation ile filtrele
            for email in found:
                clean_email = email.lower().strip()
                # Geliştirilmiş validation - dosya uzantılarını ve geçersiz emailleri filtrele
                if self.is_valid_email(clean_email):
                    emails.add(clean_email)
                    self.log(f"📧 {clean_email}")
                else:
                    # Geçersiz email'leri logla (debug için)
                    if clean_email.count('@') == 1:  # @ içeriyorsa ama geçersizse logla
                        self.log(f"⚠️ Filtrelendi (dosya/geçersiz): {clean_email}", "WARNING")
            
            self.log(f"✅ Requests tarama tamamlandı: {len(emails)} mail")
            
        except Exception as e:
            self.log(f"❌ Requests hatası: {e}", "ERROR")
            raise
        
        return emails
    
    def send_emails(self):
        """Mail gönder"""
        if not self.gmail_address.get() or not self.gmail_password.get():
            messagebox.showwarning("Uyarı", "Gmail bilgilerini girin!")
            return
        
        if not self.pdf_path or not os.path.exists(self.pdf_path):
            messagebox.showwarning("Uyarı", "PDF seçin!")
            return
        
        self.email_text = self.text_editor.get('1.0', tk.END).strip()
        if not self.email_text:
            messagebox.showwarning("Uyarı", "Mail metni yazın!")
            return
        
        resend_days = self.resend_days.get()
        
        # ÖNCE: Son gönderimden bu yana kaç gün geçti kontrol et
        self.cursor.execute('''
            SELECT MAX(sent_date) as last_sent
            FROM send_history
            WHERE status = 'success'
        ''')
        
        result = self.cursor.fetchone()
        if result and result[0]:
            last_sent = result[0]
            # SQLite datetime string'ini parse et
            from datetime import datetime, timedelta
            try:
                last_sent_dt = datetime.strptime(last_sent, '%Y-%m-%d %H:%M:%S')
                now = datetime.now()
                days_since = (now - last_sent_dt).days
                
                if days_since < resend_days:
                    remaining_days = resend_days - days_since
                    message = f"⚠️ UYARI: Mail Zaten Gönderilmiş!\n\n"
                    message += f"Son gönderim: {days_since} gün önce\n"
                    message += f"Tekrar gönderim süresi: {resend_days} gün\n\n"
                    message += f"🔒 {remaining_days} gün sonra tekrar gönderebilirsiniz.\n\n"
                    message += f"Yine de göndermek istiyor musunuz?"
                    
                    if not messagebox.askyesno("Tekrar Gönderim Uyarısı", message, icon='warning'):
                        self.log(f"⚠️ Mail gönderimi iptal edildi (Son gönderim: {days_since} gün önce)")
                        return
            except:
                pass
        
        self.cursor.execute('''
            SELECT DISTINCT ep.email
            FROM email_pool ep
            LEFT JOIN (
                SELECT email, MAX(sent_date) as last_sent
                FROM send_history
                WHERE status = 'success'
                GROUP BY email
            ) sh ON ep.email = sh.email
            WHERE sh.last_sent IS NULL 
               OR sh.last_sent < datetime('now', '-' || ? || ' days')
        ''', (resend_days,))
        
        emails_to_send = [row[0] for row in self.cursor.fetchall()]
        
        if not emails_to_send:
            messagebox.showinfo("Bilgi", f"Gönderilecek yeni mail yok!\n\nTüm maillere son {resend_days} gün içinde gönderilmiş.")
            return
        
        if not messagebox.askyesno("Onay", f"📧 {len(emails_to_send)} mail gönderilsin mi?"):
            return
        
        thread = threading.Thread(target=self._send_emails_thread, 
                                 args=(emails_to_send,), daemon=True)
        thread.start()
        
    def _send_emails_thread(self, emails):
        """Mail gönder thread"""
        self.send_btn.config(state='disabled')
        self.log(f"📤 Gönderim başladı: {len(emails)} alıcı")
        self.log(f"⏳ Lütfen bekleyin, her mail 2 saniye arayla gönderiliyor...")
        
        success = 0
        fail = 0
        
        try:
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login(self.gmail_address.get(), self.gmail_password.get())
            
            for i, to_email in enumerate(emails, 1):
                try:
                    # Anlık durum güncellemesi
                    self.update_scan_status(
                        f"📧 Mail Gönderiliyor...",
                        f"{i}/{len(emails)} gönderildi | ✅ {success} | ❌ {fail}",
                        "blue"
                    )
                    
                    msg = MIMEMultipart()
                    msg['From'] = self.gmail_address.get()
                    msg['To'] = to_email
                    msg['Subject'] = self.email_subject.get()
                    
                    msg.attach(MIMEText(self.email_text, 'plain', 'utf-8'))
                    
                    with open(self.pdf_path, 'rb') as f:
                        pdf = MIMEBase('application', 'pdf')
                        pdf.set_payload(f.read())
                        encoders.encode_base64(pdf)
                        pdf.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(self.pdf_path)}"')
                        msg.attach(pdf)
                    
                    smtp.send_message(msg)
                    
                    self.cursor.execute('INSERT INTO send_history (email, status) VALUES (?, ?)', (to_email, 'success'))
                    self.conn.commit()
                    
                    success += 1
                    self.log(f"✅ [{i}/{len(emails)}] {to_email}")
                    time.sleep(2)
                    
                except Exception as e:
                    fail += 1
                    self.log(f"❌ [{i}/{len(emails)}] {to_email}: {e}", "ERROR")
                    self.cursor.execute('INSERT INTO send_history (email, status) VALUES (?, ?)', (to_email, f'failed: {e}'))
                    self.conn.commit()
            
            smtp.quit()
            
            # Final durum
            self.update_scan_status(
                f"✅ Gönderim Tamamlandı!",
                f"Toplam: {len(emails)} | ✅ {success} başarılı | ❌ {fail} hata",
                "green"
            )
            
            self.log(f"")
            self.log(f"{'='*60}")
            self.log(f"✅ GÖNDERIM TAMAMLANDI!")
            self.log(f"{'='*60}")
            self.log(f"Toplam: {len(emails)} mail")
            self.log(f"✅ Başarılı: {success}")
            self.log(f"❌ Hatalı: {fail}")
            self.log(f"{'='*60}")
            self.log(f"")
            
            messagebox.showinfo("Gönderim Tamamlandı", 
                              f"📊 SONUÇ:\n\n✅ Başarılı: {success}\n❌ Hatalı: {fail}\n\nToplam: {len(emails)} mail")
            
            self.refresh_email_list()
            
        except Exception as e:
            self.log(f"❌ SMTP hatası: {e}", "ERROR")
            self.update_scan_status("❌ Hata!", f"SMTP bağlantı hatası", "red")
            messagebox.showerror("Hata", f"Mail gönderilemedi:\n\n{e}")
        finally:
            self.send_btn.config(state='normal')
            
    def test_gmail_connection(self):
        """Gmail test"""
        if not self.gmail_address.get() or not self.gmail_password.get():
            messagebox.showwarning("Uyarı", "Bilgileri girin!")
            return
        
        try:
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login(self.gmail_address.get(), self.gmail_password.get())
            smtp.quit()
            
            self.log("✅ Gmail bağlantısı OK!")
            messagebox.showinfo("Başarılı", "Gmail çalışıyor! ✅")
        except Exception as e:
            self.log(f"❌ Gmail hatası: {e}", "ERROR")
            messagebox.showerror("Hata", f"Gmail bağlanamadı:\n{e}")
            
    def save_settings(self):
        """Ayarları kaydet"""
        settings = {
            'gmail_address': self.gmail_address.get(),
            'gmail_password': self.gmail_password.get(),
            'email_subject': self.email_subject.get(),
            'base_url': self.base_url.get(),
            'resend_days': self.resend_days.get(),
            'pdf_path': self.pdf_path,
            'email_text': self.text_editor.get('1.0', tk.END).strip(),
            'use_selenium': self.use_selenium.get(),
            'show_browser': self.show_browser.get(),
            'selected_browser': self.selected_browser.get(),
            'selected_url_name': self.selected_url_name.get(),
            'deep_scan': self.deep_scan.get(),
            'max_pages': self.max_pages.get()
        }
        
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        
        self.log("💾 Kaydedildi")
        messagebox.showinfo("Tamam", "Ayarlar kaydedildi!")
    
    def setup_auto_save_triggers(self):
        """Tüm değişkenler için otomatik kayıt tetikleyicileri kur"""
        # StringVar ve IntVar trace ekle
        variables = [
            self.gmail_address,
            self.gmail_password,
            self.email_subject,
            self.base_url,
            self.resend_days,
            self.selected_browser,
            self.selected_url_name,
            self.max_pages
        ]
        
        for var in variables:
            var.trace_add('write', lambda *args: self.schedule_auto_save())
        
        # BooleanVar trace ekle
        bool_vars = [
            self.use_selenium,
            self.show_browser,
            self.deep_scan
        ]
        
        for var in bool_vars:
            var.trace_add('write', lambda *args: self.schedule_auto_save())
    
    def on_text_modified(self, event=None):
        """Text editörde değişiklik olduğunda çağrılır"""
        if self.text_editor.edit_modified():
            self.schedule_auto_save()
            self.text_editor.edit_modified(False)
    
    def schedule_auto_save(self):
        """Değişiklik olduktan 2 saniye sonra otomatik kaydet"""
        # Önceki zamanlayıcıyı iptal et
        if self.auto_save_timer:
            self.root.after_cancel(self.auto_save_timer)
        
        # 2 saniye sonra kaydet
        self.auto_save_timer = self.root.after(2000, self.auto_save_settings)
    
    def auto_save_settings(self):
        """Ayarları sessizce otomatik kaydet (program kapatılırken veya değişiklik olduğunda)"""
        try:
            settings = {
                'gmail_address': self.gmail_address.get(),
                'gmail_password': self.gmail_password.get(),
                'email_subject': self.email_subject.get(),
                'base_url': self.base_url.get(),
                'resend_days': self.resend_days.get(),
                'pdf_path': self.pdf_path,
                'email_text': self.text_editor.get('1.0', tk.END).strip(),
                'use_selenium': self.use_selenium.get(),
                'show_browser': self.show_browser.get(),
                'selected_browser': self.selected_browser.get(),
                'selected_url_name': self.selected_url_name.get(),
                'deep_scan': self.deep_scan.get(),
                'max_pages': self.max_pages.get()
            }
            
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            # Sessizce kaydet, log'a yazma (çok fazla log oluşmasın)
        except Exception as e:
            # Hata olursa bile ses çıkarma, sadece kritik durumlarda log
            pass
        
    def load_settings(self):
        """Ayarları yükle"""
        if os.path.exists('settings.json'):
            try:
                with open('settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                self.gmail_address.set(settings.get('gmail_address', ''))
                self.gmail_password.set(settings.get('gmail_password', ''))
                self.email_subject.set(settings.get('email_subject', 'İş Başvurusu'))
                self.base_url.set(settings.get('base_url', ''))
                self.resend_days.set(settings.get('resend_days', 7))
                self.pdf_path = settings.get('pdf_path')
                self.use_selenium.set(settings.get('use_selenium', True))
                self.show_browser.set(settings.get('show_browser', False))
                self.selected_browser.set(settings.get('selected_browser', 'Auto'))
                self.deep_scan.set(settings.get('deep_scan', False))
                self.max_pages.set(settings.get('max_pages', 100))
                
                # URL seçimini yükle
                saved_url_name = settings.get('selected_url_name', '')
                if saved_url_name and saved_url_name in self.saved_urls:
                    self.selected_url_name.set(saved_url_name)
                    self.on_url_selected(None)
                
                if self.pdf_path and os.path.exists(self.pdf_path):
                    self.pdf_status_label.config(text=f"📄 {os.path.basename(self.pdf_path)}", foreground="green")
                
                email_text = settings.get('email_text', '')
                if email_text:
                    self.text_editor.delete('1.0', tk.END)
                    self.text_editor.insert('1.0', email_text)
                
                self.log("✅ Ayarlar yüklendi")
            except Exception as e:
                self.log(f"⚠️ Ayarlar yüklenemedi: {e}", "WARNING")
                
    def save_logs(self):
        """Logları kaydet"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log", "*.log"), ("Text", "*.txt"), ("All", "*.*")]
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get('1.0', tk.END))
            
            messagebox.showinfo("Tamam", "Loglar kaydedildi!")
            
    def run(self):
        """Başlat"""
        self.log("🚀 E-posta Bot v3.3 - ÇOKLU SİTE TARAMA başlatıldı")
        self.log(f"🌐 Selenium: {'AÇIK' if self.use_selenium.get() else 'KAPALI'}")
        self.log(f"👁️ Tarayıcı: {'GÖRÜNÜR' if self.show_browser.get() else 'GİZLİ'}")
        self.log(f"🔎 Derin Tarama: {'AÇIK' if self.deep_scan.get() else 'KAPALI'}")
        
        browsers_str = ', '.join(self.available_browsers) if self.available_browsers else "YOK"
        self.log(f"🌐 Mevcut tarayıcılar: {browsers_str}")
        
        # Kayıtlı URL'leri göster
        if self.saved_urls:
            self.log(f"📌 Kayıtlı siteler: {len(self.saved_urls)}")
            for name in self.saved_urls.keys():
                self.log(f"   • {name}")
        
        self.refresh_email_list()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Kapat"""
        if self.auto_scan_active:
            if messagebox.askyesno("Çıkış", "Otomatik tarama aktif!\n\nYine de çık?"):
                self.auto_scan_active = False
                # Ayarları otomatik kaydet
                self.auto_save_settings()
                self.conn.close()
                self.root.destroy()
        else:
            # Ayarları otomatik kaydet
            self.auto_save_settings()
            self.conn.close()
            self.root.destroy()


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings('ignore')
    import urllib3
    urllib3.disable_warnings()
    
    try:
        app = EmailBot()
        app.run()
    except Exception as e:
        print("\n" + "="*60)
        print("  ❌ KRITIK HATA!")
        print("="*60)
        print(f"\nHata: {str(e)}")
        print(f"\nHata tipi: {type(e).__name__}")
        print("\nStack trace:")
        import traceback
        traceback.print_exc()
        print("\n" + "="*60)
        print("  Program beklenmedik bir hatayla karsilasti.")
        print("  Lutfen yukaridaki hata mesajini kontrol edin.")
        print("="*60 + "\n")
        input("Kapatmak icin Enter'a basin...")
        sys.exit(1)
