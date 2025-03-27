from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from queue import Queue
import random
from concurrent.futures import ThreadPoolExecutor

# Cấu hình tài khoản
accounts = [
    # {
    #     "name": "84523929485",
    #     "chrome_path": "D:\\Accounts\\Tele Accounts\\84523929485\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "D:\\Accounts\\Tele Accounts\\84523929485\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9499,
    # },
    # {
    #     "name": "84925599903",
    #     "chrome_path": "D:\\Accounts\\Tele Accounts\\84925599903\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "D:\\Accounts\\Tele Accounts\\84925599903\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9500,
    # },
    # {
    #     "name": "84914418511",
    #     "chrome_path": "D:\\Accounts\\Tele Accounts\\84914418511\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "D:\\Accounts\\Tele Accounts\\84914418511\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9501,
    # },
    # {
    #     "name": "84918134941",
    #     "chrome_path": "D:\\Accounts\\Tele Accounts\\84918134941\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "D:\\Accounts\\Tele Accounts\\84918134941\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9502,
    # },
    # {
    #     "name": "84816828974",
    #     "chrome_path": "D:\\Accounts\\Tele Accounts\\84816828974\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "D:\\Accounts\\Tele Accounts\\84816828974\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9503,
    # },
    # {
    #     "name": "84852158289",
    #     "chrome_path": "D:\\Accounts\\Tele Accounts\\84852158289\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "D:\\Accounts\\Tele Accounts\\84852158289\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9504,
    # },
    # {
    #     "name": "84912161609",
    #     "chrome_path": "D:\\Accounts\\Tele Accounts\\84912161609\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "D:\\Accounts\\Tele Accounts\\84912161609\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9505,
    # },
    # {
    #     "name": "84563639029",
    #     "chrome_path": "D:\\Accounts\\Tele Accounts\\84563639029\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "D:\\Accounts\\Tele Accounts\\84563639029\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9506,
    # },
    {
        "name": "84379145648",
        "chrome_path": "D:\\Accounts\\Tele Accounts\\84379145648\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "D:\\Accounts\\Tele Accounts\\84379145648\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9507,
    },
]

chrome_driver_path = r"D:\Workspace\Python\chromedriver.exe"

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
        # options.add_argument("--disable-extensions")
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
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.page_load_strategy = 'normal'
        
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Lỗi khởi tạo driver cho tài khoản {account['name']}: {e}")
        return None

def single_task(driver, account):
    try:
        driver.get("https://hub.beamable.network/modules/dailycheckin")
        time.sleep(15)

        # Tìm và click vào button "Show More"
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Show More')]"))
        )
        show_more_button.click()
        time.sleep(5)

        # 2️⃣ Chờ "Claim" được thêm vào DOM
        claim_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[div[contains(text(), 'Claim')]]"))
        )
        print("✅ Nút Claim đã xuất hiện trong DOM")

        # 3️⃣ Dùng JavaScript để click (bypass lỗi)
        driver.execute_script("arguments[0].click();", claim_button)
        time.sleep(5)

        return True

    except Exception as e:
        print(f"Lỗi khi thực hiện các thao tác: {e}")

        time.sleep(10)  # Chờ hoàn tất đăng nhập
        return True


def proceed(account):
    try:
        # Đợi cho đến khi có slot trống
        while active_drivers.qsize() >= MAX_CONCURRENT_DRIVERS:
            time.sleep(30)

        driver = init_driver(account)
        if not driver:
            return

        active_drivers.put(driver)

        success = single_task(driver, account)
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
    # Khởi tạo ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:  # Chạy tối đa 10 luồng cùng lúc
        for account in accounts:
            executor.submit(proceed, account)
        time.sleep(60)  # Delay giữa các tài khoản


if __name__ == "__main__":
    main()