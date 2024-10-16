import requests
import json
import time
import random
from setproctitle import setproctitle
from colorama import Fore, Style, init
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib.parse  # For decoding the URL-encoded initData

init(autoreset=True)
red = Fore.LIGHTRED_EX
blue = Fore.LIGHTBLUE_EX
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
black = Fore.LIGHTBLACK_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

url = "https://notpx.app/api/v1"

# ACTIVITY
WAIT = 180 * 3
DELAY = 1

# IMAGE
WIDTH = 1000
HEIGHT = 1000
MAX_HEIGHT = 50

# Initialize colorama for colored output
init(autoreset=True)

setproctitle("notpixel")

class NotPixTod:
    def __init__(self, no, proxies):
        ci = lambda a, b: (b * 1000) + (a + 1)
        self.p = no
        self.proxies = proxies
        self.colors = [
            "#3690ea",
            "#e46e6e",
            "#ffffff",
            "#be0039",
            "#6d001a",
            "#ffd635",
            "#ff9600",
            "#bf4300",
            "#7eed56",
            "#00cc78",
            "#00a368",
        ]
        self.block = {
            "#3690EA": [
                [ci(431, 452), ci(431, 452)],
                [ci(432, 452), ci(432, 452)],
                [ci(433, 452), ci(433, 452)],
                [ci(434, 452), ci(434, 452)],
                [ci(435, 452), ci(435, 452)],
                [ci(436, 452), ci(436, 452)],
                [ci(437, 452), ci(437, 452)],
                [ci(438, 452), ci(438, 452)],
                [ci(439, 452), ci(439, 452)],
                [ci(440, 452), ci(440, 452)],
                [ci(441, 452), ci(441, 452)],
                [ci(442, 452), ci(442, 452)],
                [ci(443, 452), ci(443, 452)],
                [ci(444, 452), ci(444, 452)],
                [ci(445, 452), ci(445, 452)],
                [ci(446, 452), ci(446, 452)],
                [ci(447, 452), ci(447, 452)],
                [ci(448, 452), ci(448, 452)],
                [ci(449, 452), ci(449, 452)],
                [ci(450, 452), ci(450, 452)],
                [ci(451, 452), ci(451, 452)],
            ]
        }

    def log(self, msg):
        now = datetime.now().isoformat().split("T")[1].split(".")[0]
        print(
            f"{black}[{now}]{white}-{blue}[{white}acc {self.p + 1}{blue}]{white} {msg}{reset}"
        )


# Function to log messages with timestamp in light grey color
def log_message(message, color=Style.RESET_ALL):
    current_time = datetime.now().strftime("[%H:%M:%S]")
    print(f"{Fore.LIGHTBLACK_EX}{current_time}{Style.RESET_ALL} {color}{message}{Style.RESET_ALL}")

# Function to initialize a requests session with retry logic
def get_session_with_retries(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Create a session with retry logic
session = get_session_with_retries()



# Function to claim resources from the server
def claim(header):
    log_message("BOT LAGI NGEGAMBAR", Fore.CYAN)
    try:
        session.get(f"{url}/mining/claim", headers=header, timeout=10)
    except requests.exceptions.RequestException as e:
        log_message(f"GAGAL COK: {e}", Fore.RED)

# Function to calculate pixel index based on x, y position
def get_pixel(x, y):
    return y * 1000 + x + 1

# Function to get x, y position from pixel index
def get_pos(pixel, size_x):
    return pixel % size_x, pixel // size_x

# Function to get pixel index based on canvas position
def get_canvas_pos(x, y):
    return get_pixel(start_x + x - 1, start_y + y - 1)

# Starting coordinates
start_x = 920
start_y = 386

# Main function to perform the painting process
# Main function to perform the painting process
def main(auth, account, notpixtod):
    headers = {'authorization': auth}
    try:
        # Claim resources dan ambil balance awal
        claim(headers)
        response = session.get(f"{url}/mining/status", headers=headers, timeout=10)
        balance = response.json().get("userBalance", 0)  # Balance awal
        log_message(f"balance: {balance:.2f}", Fore.CYAN)

        # Inisialisasi total poin
        total_points = 0

        # Mengecat setiap piksel di blok yang sudah didefinisikan
        # Looping untuk setiap koordinat dan warna
        charges = response.json().get("boosts", {}).get("energyLimit", 0)
        for i in range(charges):
            # Misalkan blocks adalah suatu data yang kamu proses (tidak jelas dari kode sebelumnya)
            # Ganti dengan blocks yang tepat
                try:
                    # Menggunakan data color dan koordinat yang sudah diambil dari notpixtod.block
                    pixel_id = random.randint(1, 1000000)
                    new_color = random.choice(list(notpixtod.block.keys())).upper()
                    temp_color = [color.upper() for color in notpixtod.colors]
                    temp_color.remove(new_color)
                    first_color = random.choice(temp_color).upper()
                    pixel_id = random.choice(random.choice(notpixtod.block[new_color]))
                    for i in range(2):
                        if i == 0:
                            # Data baru yang dikirimkan
                            data_post = {"pixelId": pixel_id, "newColor": first_color}
                            response = session.post(f"{url}/repaint/start", json=data_post, headers=headers, timeout=10)
                            new_balance = response.json().get("balance", 0)
                            inc = new_balance - balance  # Poin yang didapat dari pengecatan ini
                            balance = new_balance  # Update balance

                            # Hanya tampilkan poin yang didapat dari pengecatan, bukan balance besar
                            
                            log_message(f"Paint: {pixel_id}, color: {new_color}, reward: +{inc:.2f} points", Fore.GREEN)
                        else:
                            data_post = {"pixelId": pixel_id, "newColor": new_color}
                            response = session.post(f"{url}/repaint/start", json=data_post, headers=headers, timeout=10)
                            new_balance = response.json().get("balance", 0)
                            inc = new_balance - balance  # Poin yang didapat dari pengecatan ini
                            balance = new_balance  # Update balance

                            # Hanya tampilkan poin yang didapat dari pengecatan, bukan balance besar
                            
                            log_message(f"Paint: {pixel_id}, color: {new_color}, reward: +{inc:.2f} points", Fore.GREEN)
                                # Melakukan request pengecatan
                    
                    # Periksa status response
                    if response.status_code == 400:
                        log_message("Abis bensin", Fore.RED)
                        break
                    if response.status_code == 401:
                        log_message("Unauthorized", Fore.RED)
                        break

                    # Hitung poin yang didapat dari pengecatan
                    new_balance = response.json().get("balance", 0)
                    inc = new_balance - balance  # Poin yang didapat dari pengecatan ini
                    balance = new_balance  # Update balance

                    # Hanya tampilkan poin yang didapat dari pengecatan, bukan balance besar
                    
                
                

                    # Tambahkan poin ke total poin
                    total_points += inc

                except requests.exceptions.RequestException as e:
                    log_message(f"Failed to paint: {e}", Fore.RED)
                    break

        # Tampilkan total poin yang didapat di akhir sesi
        log_message(f"Total points yang didapat: {total_points:.2f} points", Fore.MAGENTA)

    except requests.exceptions.RequestException as e:
        log_message(f"Network error in account {account}: {e}", Fore.RED)

# Process accounts and manage sleep logic
def process_accounts(accounts):
    for account in accounts:
        username = extract_username_from_initdata(account)
        log_message(f"--- NOTPIXELTOT PAKE QUERYTOD: {username} ---", Fore.BLUE)
        notpixtod = NotPixTod(0, [])  # Create an instance of NotPixTod
        main(account, account, notpixtod)  # Pass notpixtod to the main function


# Function to extract the username from the URL-encoded init data
def extract_username_from_initdata(init_data):
    decoded_data = urllib.parse.unquote(init_data)
    
    username_start = decoded_data.find('"username":"') + len('"username":"')
    username_end = decoded_data.find('"', username_start)
    
    if username_start != -1 and username_end != -1:
        return decoded_data[username_start:username_end]
    
    return "Unknown"

# Function to load accounts from data.txt
def load_accounts_from_file(filename):
    with open(filename, 'r') as file:
        accounts = [f"initData {line.strip()}" for line in file if line.strip()]
    return accounts

if __name__ == "__main__":
    accounts = load_accounts_from_file('data.txt')
    process_accounts(accounts)
tion


# Function to extract the username from the URL-encoded init data
def extract_username_from_initdata(init_data):
    decoded_data = urllib.parse.unquote(init_data)
    
    username_start = decoded_data.find('"username":"') + len('"username":"')
    username_end = decoded_data.find('"', username_start)
    
    if username_start != -1 and username_end != -1:
        return decoded_data[username_start:username_end]
    
    return "Unknown"

# Function to load accounts from data.txt
def load_accounts_from_file(filename):
    with open(filename, 'r') as file:
        accounts = [f"initData {line.strip()}" for line in file if line.strip()]
    return accounts

if __name__ == "__main__":
    accounts = load_accounts_from_file('data.txt')
    process_accounts(accounts)
