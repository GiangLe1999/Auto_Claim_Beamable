from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import os
import datetime
import threading
from queue import Queue
import random
from concurrent.futures import ThreadPoolExecutor


# Cấu hình tài khoản
accounts = [
    {
        "name": "84925599903",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84925599903\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84925599903\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9223,
    },
    {
        "name": "84914418511",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84914418511\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84914418511\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9224,
    },
    {
        "name": "84918134941",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84918134941\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84918134941\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9225,
    },
    {
        "name": "84816828974",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84816828974\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84816828974\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9226,
    },
    {
        "name": "84852158289",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84852158289\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84852158289\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9227,
    },
    {
        "name": "84912161609",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84912161609\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84912161609\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9228,
    }
]

chrome_driver_path = r"D:\Workspace\Python\chromedriver.exe"
# Giữ nguyên phần accounts configuration như cũ

# Global variables
shutdown_event = threading.Event()
active_drivers = Queue()
MAX_CONCURRENT_DRIVERS = 30

def shutdown_at_target_time(target_hour, target_minute):
    print(f"Hẹn giờ tắt máy lúc {target_hour:02d}:{target_minute:02d} (giờ Việt Nam)...")
    while not shutdown_event.is_set():
        now = datetime.datetime.now()
        if now.hour == target_hour and now.minute >= target_minute:
            print("Đã đến thời gian hẹn giờ! Dừng chương trình và tắt máy tính...")
            shutdown_event.set()
            if os.name == 'nt':
                os.system("shutdown /s /t 1")
            else:
                os.system("shutdown now")
            break
        time.sleep(10)

def init_driver(account):
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = account["chrome_path"]
        options.add_argument(f"--user-data-dir={account['user_data_dir']}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument(f"--remote-debugging-port={account['debug_port']}")
        # options.add_argument("--disable-cache") 
        # options.add_argument("--clear-cache")
        
        # Thêm các options để giảm tải tài nguyên
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        # options.add_argument("--disablce-software-rasterizer")
        # options.add_argument("--disable-infobars")
        # options.add_argument("--disable-notifications")
        # options.add_argument("--disable-logging")
        # options.add_argument("--disable-default-apps")
        # options.add_argument("--disable-popup-blocking")
        # options.add_argument("--disable-prompt-on-repost")
        # options.add_argument("--disable-sync")
        # options.add_argument("--disable-web-security")
        # options.add_argument("--disable-translate")
        # options.add_argument("--disable-hang-monitor")
        # options.add_argument("--disable-client-side-phishing-detection")
        # options.add_argument("--disable-component-update")
        # options.add_argument("--memory-model=low")
        # options.add_argument("--disable-backing-store-limit")
        # options.add_argument("--enable-unsafe-swiftshader")
        
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Lỗi khởi tạo driver cho tài khoản {account['name']}: {e}")
        return None

# Chat /up for daily checkin 
def chat_actions(driver, account):
    try:
        driver.get("https://web.telegram.org/k/#-2043049770")
        time.sleep(3)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "peer-title")]'))
        )

        message_box = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"]'))
        )

        wait_time = random.randint(1, 5)
        time.sleep(wait_time)

        message_box.send_keys('/up')
        message_box.send_keys(Keys.ENTER)

        time.sleep(3)
        return True
    except Exception as e:
        print(f"Lỗi thao tác điểm danh ({account['name']}): {e}")
        return False
    

def open_wallet_actions(driver, account):
    try:
        driver.get("https://web.telegram.org/k/#@UXUYbot")
        time.sleep(3)  # Random delay

        start_game_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Wallet')]"))
        )
        start_game_button.click()
        time.sleep(3)

        # Tìm và nhấp vào button có class 'popup-button btn primary rp'
        try:
            popup_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "popup-button.btn.primary.rp"))
            )
            popup_button.click()
            time.sleep(2)
        except TimeoutException:
            print(f"Không tìm thấy nút Launch, tiếp tục chạy chương trình cho ({account['name']})")
        except Exception as e:
            print(f"Lỗi không xác định khi tìm popup-button: {e}")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)

        time.sleep(3)
        return True
    except Exception as e:
        print(f"Lỗi mở wallet ({account['name']}): {e}")
        return False

def get_wait_time_from_countdown(driver, xpath, default_wait=60):
    try:
        countdown_timer = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        countdown_text = countdown_timer.text.strip()
        percents = float(countdown_text)  # Chuyển đổi thành số thập phân (float)
        wait_time_seconds = (100 - percents) * 10800 / 100  # Tính thời gian chờ dựa trên phần trăm
        return wait_time_seconds
    except Exception as e:
        print(f"Lỗi tính thời gian chờ: {e}")
        return default_wait + random.uniform(5, 15)
    

def handle_single_claim_cycle(driver, account):
    try:
        success = open_wallet_actions(driver, account)
        if not success:
            return 60  # Return default wait time if actions failed

        claim_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "bg-Orange"))
        )
        claim_button.click()
        time.sleep(5)

        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[span[text()='Claim']]"))
        )
        close_button.click()
        time.sleep(5)

        wait_time = 10805
        return wait_time
    except Exception as e:
        try:
            # Nếu không tìm thấy nút Claim, kiểm tra thời gian chờ
            wait_time = get_wait_time_from_countdown(
                driver,
                "//span[@style=\"font-variant-numeric: tabular-nums;\"]"
            )
            return wait_time

        except Exception as countdown_exception:
            print(f"Lỗi khi tính toán thời gian chờ: {countdown_exception}")
            wait_time = 60  # Giá trị chờ mặc định nếu không tìm thấy thời gian
            return wait_time

def handle_claim(account):
    while not shutdown_event.is_set():
        try:
            # Đợi cho đến khi có slot trống
            while active_drivers.qsize() >= MAX_CONCURRENT_DRIVERS:
                time.sleep(1)
                if shutdown_event.is_set():
                    return

            driver = init_driver(account)
            if not driver:
                time.sleep(60)
                continue

            active_drivers.put(driver)
            wait_time = handle_single_claim_cycle(driver, account)

        except Exception as e:
            print(f"Lỗi trong claim ({account['name']}): {e}")
            wait_time = 60 + random.uniform(5, 15)

        finally:
            if driver:
                try:
                    driver.quit()
                    active_drivers.get()
                except:
                    pass

            print(f"Chờ {wait_time}s: {account['name']}")
            time.sleep(wait_time)

def handle_daily_check_in(account):
    try:
        # Đợi cho đến khi có slot trống
        while active_drivers.qsize() >= MAX_CONCURRENT_DRIVERS:
            time.sleep(1)
            if shutdown_event.is_set():
                return

        driver = init_driver(account)
        if not driver:
            return

        active_drivers.put(driver)

        success = chat_actions(driver, account)
        if not success:
            return

    except Exception as e:
        print(f"Lỗi điểm danh ({account['name']}): {e}")

    finally:
        if driver:
            try:
                time.sleep(5 + random.uniform(1, 3))
                driver.quit()
                active_drivers.get()
                print(f"Đã đóng driver: {account['name']}")
            except:
                pass

def main():
    print("1: Điểm danh hàng ngày")
    print("2: Claim tự động")
    action = input("Chọn (1/2): ")

    target_hour = 3
    target_minute = 5

    # Start shutdown timer
    shutdown_thread = threading.Thread(
        target=shutdown_at_target_time,
        args=(target_hour, target_minute)
    )
    shutdown_thread.daemon = True
    shutdown_thread.start()

    # Khởi tạo ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:  # Chạy tối đa 10 luồng cùng lúc
        for account in accounts:
            if action == "1":
                executor.submit(handle_daily_check_in, account)
            else:
                executor.submit(handle_claim, account)
            time.sleep(10)  # Delay giữa các tài khoản

if __name__ == "__main__":
    main()