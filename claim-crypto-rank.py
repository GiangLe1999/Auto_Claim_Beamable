from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
from queue import Queue
import random
from concurrent.futures import ThreadPoolExecutor
import re

# Cấu hình tài khoản
accounts = [
    {
        "name": "84912161609",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84912161609\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84912161609\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9505,
    },
    {
        "name": "84852158289",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84852158289\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84852158289\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9504,
    },
    {
        "name": "84816828974",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84816828974\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84816828974\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9503,
    },
    {
        "name": "84918134941",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84918134941\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84918134941\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9502,
    },
    {
        "name": "84914418511",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84914418511\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84914418511\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9501,
    },
    {
        "name": "84925599903",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84925599903\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84925599903\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9500,
    },
]

chrome_driver_path = r"D:\Workspace\Python\chromedriver.exe"

# Global variables
active_drivers = Queue()
MAX_CONCURRENT_DRIVERS = 1


def init_driver(account):
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = account["chrome_path"]
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage") # Giúp tránh lỗi bộ nhớ dùng chung bị giới hạn
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument(f"--user-data-dir={account['user_data_dir']}")
        options.add_argument(f"--remote-debugging-port={account['debug_port']}")

        options.add_argument("--disable-software-rasterizer")
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
        options.page_load_strategy = 'normal'
        
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Lỗi khởi tạo driver cho tài khoản {account['name']}: {e}")
        return None

# Daily checkin 
def checkin_actions(driver, account):
    try:
        success = open_app(driver, account)
        if not success:
            return 60  # Return default wait time if actions failed

        task_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Tasks')]"))
        )
        task_button.click()
        time.sleep(2)

        claim_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Claim')]"))
        )
        claim_button.click()
        time.sleep(2)

        confirm_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Check in')]"))
        )
        confirm_button.click()
        time.sleep(2)

        return True
    except Exception as e:
        print(f"Lỗi thao tác điểm danh ({account['name']}): {e}")
        return False
    

# Like post interactions 
def like_post_actions(driver, account):
    try:
        success = open_app(driver, account)
        if not success:
            return 60  # Return default wait time if actions failed

        task_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Tasks')]"))
        )
        task_button.click()
        time.sleep(2)

        like_x_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[span[contains(text(), 'Like Latest Post on X')]]"))
        )
        like_x_button.click()
        time.sleep(2)

        like_tele_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[span[contains(text(), 'Like Latest Post')]]"))
        )
        like_tele_button.click()

        time.sleep(30)

        confirm_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Claim')]"))
        )
        confirm_button.click()
        time.sleep(2)

        confirm_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Claim')]"))
        )
        confirm_button.click()
        time.sleep(2)

        return True
    except Exception as e:
        print(f"Lỗi thao tác điểm danh ({account['name']}): {e}")
        return False

def open_app(driver, account):
    try:
        driver.get("https://web.telegram.org/k/#@CryptoRank_app_bot")
        time.sleep(3)  # Random delay

        start_app_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Launch APP')]"))
        )
        start_app_button.click()
        time.sleep(3)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)

        time.sleep(3)
        return True
    except Exception as e:
        print(f"Lỗi mở app ({account['name']}): {e}")
        return False

def get_wait_time_from_countdown(driver, xpath, default_wait=60):
    try:
        countdown_timer = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        countdown_text = countdown_timer.text.strip()

        hours = 0
        minutes = 0
        time_match = re.match(r'(\d+)h (\d+)m', countdown_text)
        if time_match:
            hours = int(time_match.group(1))
            minutes = int(time_match.group(2))
        total_seconds = (hours * 60 * 60) + (minutes * 60) + 5

        return total_seconds
    except Exception as e:
        print(f"Lỗi tính thời gian chờ: {e}")
        return default_wait
    

def handle_single_claim_cycle(driver, account):
    try:
        success = open_app(driver, account)
        if not success:
            return 60  # Return default wait time if actions failed

        claim_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "whitespace-nowrap"))
        )
        claim_button.click()
        time.sleep(5)

        start_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "whitespace-nowrap"))
        )
        start_button.click()
        time.sleep(3)

        wait_time = 21615
        return wait_time
    except Exception as e:
        try:
            # Nếu không tìm thấy nút Claim, kiểm tra thời gian chờ
            wait_time = get_wait_time_from_countdown(
                driver,
                "//div[contains(@class, 'text-sm')]"
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
                time.sleep(30)
                # if shutdown_event.is_set():
                #     return

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
            time.sleep(30)

        driver = init_driver(account)
        if not driver:
            return

        active_drivers.put(driver)

        success = checkin_actions(driver, account)
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

def handle_daily_like_post(account):
    try:
        # Đợi cho đến khi có slot trống
        while active_drivers.qsize() >= MAX_CONCURRENT_DRIVERS:
            time.sleep(30)

        driver = init_driver(account)
        if not driver:
            return

        active_drivers.put(driver)

        success = like_post_actions(driver, account)
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
    print("3: Like post hàng ngày")
    action = input("Chọn (1/2/3): ")

    # target_hour = 3
    # target_minute = 5

    # Start shutdown timer
    # shutdown_thread = threading.Thread(
    #     target=shutdown_at_target_time,
    #     args=(target_hour, target_minute)
    # )
    # shutdown_thread.daemon = True
    # shutdown_thread.start()

    # Khởi tạo ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:  # Chạy tối đa 10 luồng cùng lúc
        for account in accounts:
            if action == "1":
                executor.submit(handle_daily_check_in, account)
            elif action == "2":
                executor.submit(handle_claim, account)
            elif action == "3":
                executor.submit(handle_daily_like_post, account)
            time.sleep(30)  # Delay giữa các tài khoản

if __name__ == "__main__":
    main()