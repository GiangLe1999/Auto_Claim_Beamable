
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
import time
from queue import Queue
import random
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta

# Cấu hình tài khoản
accounts = [
    {
        "name": "anhcay",
        "chrome_path": "I:\\My Drive\\port tele\\may school\\anhcay\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "I:\\My Drive\\port tele\\may school\\anhcay\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9220,
    },
    {
        "name": "caytien03",
        "chrome_path": "I:\\My Drive\\port tele\\may school\\caytien03\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "I:\\My Drive\\port tele\\may school\\caytien03\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9221,
    },
    {
        "name": "caytien05",
        "chrome_path": "I:\\My Drive\\port tele\\may school\\caytien05\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "I:\\My Drive\\port tele\\may school\\caytien05\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9223,
    },
    {
        "name": "caytien06",
        "chrome_path": "I:\\My Drive\\port tele\\may school\\caytien06\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "I:\\My Drive\\port tele\\may school\\caytien06\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9224,
    },
    {
        "name": "caytien07",
        "chrome_path": "I:\\My Drive\\port tele\\may school\\caytien07\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "I:\\My Drive\\port tele\\may school\\caytien07\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9225,
    },
    {
        "name": "daonui",
        "chrome_path": "I:\\My Drive\\port tele\\may school\\daonui\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "I:\\My Drive\\port tele\\may school\\daonui\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9226,
    },
    {
        "name": "thanhtruong1691",
        "chrome_path": "I:\\My Drive\\port tele\\may school\\thanhtruong1691\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "I:\\My Drive\\port tele\\may school\\thanhtruong1691\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9228,
    },
]

chrome_driver_path = r"F:\Auto Claim\chromedriver.exe"

active_drivers = Queue()
MAX_CONCURRENT_DRIVERS = 30

# Lấy thời gian hiện tại theo múi giờ Việt Nam (UTC+7)
def get_vietnam_time():
    vietnam_tz = timezone(timedelta(hours=7))  # Múi giờ Việt Nam UTC+7
    return datetime.now(vietnam_tz).strftime('%H:%M:%S %d-%m-%Y')  

def init_driver(account):
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = account["chrome_path"]
        options.add_argument(f"--user-data-dir={account['user_data_dir']}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument(f"--remote-debugging-port={account['debug_port']}")
        options.add_argument("--disable-cache") 
        options.add_argument("--clear-cache")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        # Thêm các options để giảm tải tài nguyên
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disablce-software-rasterizer")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-prompt-on-repost")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-translate")
        options.add_argument("--disable-hang-monitor")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-component-update")
        options.add_argument("--memory-model=low")
        options.add_argument("--disable-backing-store-limit")
        options.add_argument("--enable-unsafe-swiftshader")
        
        service = Service(chrome_driver_path)
        # Thêm timeout và retry
        for attempt in range(3):
            try:
                driver = webdriver.Chrome(service=service, options=options)
                return driver
            except Exception:
                # print(f"Lần thử {attempt + 1}: Lỗi khởi tạo driver")
                time.sleep(5)
        
        return None
    
    except Exception as e:
        # print(f"Lỗi khởi tạo driver cho tài khoản {account['name']}: {e}")
        return None

def perform_meta_cat_actions(driver, account):
    try:
        driver.get("https://web.telegram.org/k/#@MTZCat_bot")
        time.sleep(3)  # Random delay

        start_game_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Start Game')]"))
        )
        start_game_button.click()
        time.sleep(3)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)

        claim_now_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Claim now')]"))
        )
        claim_now_button.click()
        time.sleep(3)
        return True
    except Exception as e:
        print(f"Lỗi thao tác MetaCat Bot ({account['name']}): {e}")
        return False

def get_wait_time_from_countdown(driver, xpath, default_wait=60):
    try:
        countdown_timer = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        countdown_text = countdown_timer.text.strip()
        hours, minutes, seconds = map(int, countdown_text.split(":"))
        wait_time_seconds = hours * 3600 + minutes * 60 + seconds + 5
        return wait_time_seconds
    except Exception as e:
        print(f"Lỗi tính thời gian chờ: {e}")
        return default_wait + random.uniform(5, 15)

def handle_single_claim_cycle(driver, account):
    try:
        success = perform_meta_cat_actions(driver, account)
        if not success:
            return 60  # Return default wait time if actions failed

        claim_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='Claim']"))
        )
        claim_button.click()
        print(f"({account['name']}): Đã claim lúc {get_vietnam_time()}")
        time.sleep(10)

        close_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close')]"))
        )
        close_button.click()
        time.sleep(5)

        wait_time = get_wait_time_from_countdown(
            driver,
            "//div[contains(@class, 'bg-gradient-to-b')]//span[contains(text(), ':')]"
        )
        return wait_time
    except Exception as e:
        try:
            # Nếu không tìm thấy nút Claim, kiểm tra thời gian chờ
            wait_time = get_wait_time_from_countdown(
                driver,
                "//div[contains(@class, 'bg-gradient-to-b')]//span[contains(text(), ':')]"
            )
            return wait_time

        except Exception as countdown_exception:
            print(f"Lỗi khi tính toán thời gian chờ: {countdown_exception}")
            wait_time = 60  # Giá trị chờ mặc định nếu không tìm thấy thời gian
            return wait_time

def handle_claim(account):
    while True:
        try:
            # Đợi cho đến khi có slot trống
            while active_drivers.qsize() >= MAX_CONCURRENT_DRIVERS:
                time.sleep(1)

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

            print(f"{account['name']}: Chờ {wait_time}s")
            time.sleep(wait_time)

def handle_daily_check_in(account):
    try:
        # Đợi cho đến khi có slot trống
        while active_drivers.qsize() >= MAX_CONCURRENT_DRIVERS:
            time.sleep(1)

        driver = init_driver(account)
        if not driver:
            return

        active_drivers.put(driver)
        success = perform_meta_cat_actions(driver, account)
        if not success:
            return

        mission_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Mission']"))
        )
        mission_button.click()
        time.sleep(5 + random.uniform(1, 3))

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(text(), \"You've already checked in for today.\")]"))
            )
            print(f"Đã điểm danh trước đó: {account['name']}")
        except:
            check_in_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Check In')]"))
            )
            check_in_button.click()
            print(f"Đã điểm danh: {account['name']}")

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

    # Khởi tạo ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:  # Chạy tối đa 10 luồng cùng lúc
        for account in accounts:
            if action == "1":
                executor.submit(handle_daily_check_in, account)
            else:
                executor.submit(handle_claim, account)
            time.sleep(6)  # Delay giữa các tài khoản

if __name__ == "__main__":
    main()