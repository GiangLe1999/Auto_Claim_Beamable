from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from multiprocessing import Process

# Cấu hình tài khoản
accounts = [
    {
        "name": "Hải Bình Ngu Ngốc",
        "user_data_dir": "C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data\\Profile_1",
        "debug_port": 9225  # Cổng Debug riêng
    },
    {
        "name": "Diễm Hằng Xinh Đẹp",
        "user_data_dir": "C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data\\Profile_2",
        "debug_port": 9226  # Cổng Debug riêng
    }
]

# Hàm khởi tạo Selenium
def init_driver(account):
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={account['user_data_dir']}")  # Thư mục profile của Chrome
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument(f"--remote-debugging-port={account['debug_port']}")  # Cổng Debug riêng

    # Sử dụng webdriver-manager để tự động tải ChromeDriver
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

# Hàm xử lý logic chính
def handle_account(account):
    driver = None
    try:
        driver = init_driver(account)
        print(f"Đang xử lý tài khoản: {account['name']}")

        # Truy cập tới MetaCat Bot
        driver.get("https://web.telegram.org/k/#@MTZCat_bot")
        print(f"Đang mở MetaCat Bot cho tài khoản: {account['name']}")
        time.sleep(5)

        # Click nút Start Game
        start_game_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Start Game')]"))
        )
        start_game_button.click()
        print("Đã click vào nút Start Game...")
        time.sleep(5)

        # Chuyển sang iframe (cửa sổ con của MetaCat Bot)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)  # Chuyển ngữ cảnh sang iframe
        print("Đã chuyển sang iframe của MetaCat Bot...")

        # Click nút Claim now
        claim_now_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Claim now')]"))
        )
        claim_now_button.click()
        print("Đã click vào nút Claim now...")
        time.sleep(10)

        # Click nút Claim
        claim_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='Claim']"))
        )
        claim_button.click()
        print("Đã click vào nút Claim...")
        time.sleep(10)

        # Click nút Close
        close_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close')]"))
        )
        close_button.click()
        print("Đã click vào nút Close để xác nhận Transaction...")
        time.sleep(5)

        # Lặp lại việc click nút Claim mỗi 2 giờ
        while True:
            print(f"Chờ 2 tiếng để Claim tiếp theo cho tài khoản: {account['name']}")
            time.sleep(7200)  # Chờ 2 tiếng

            # Click nút Claim
            driver.switch_to.frame(iframe)  # Chuyển lại vào iframe
            claim_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//img[@alt='Claim']"))
            )
            claim_button.click()
            print(f"Đã Claim thành công cho tài khoản: {account['name']}")
            time.sleep(10)

            # Click nút Close
            close_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close')]"))
            )
            close_button.click()
            print("Đã click vào nút Close để xác nhận Transaction...")
            time.sleep(5)

    except Exception as e:
        print(f"Lỗi xảy ra với tài khoản {account['name']}: {e}")

    finally:
        if driver:
            driver.quit()
            print(f"Đã đóng trình duyệt cho tài khoản: {account['name']}")

# Hàm chính
def main():
    processes = []
    for account in accounts:
        # Tạo một tiến trình riêng cho mỗi tài khoản
        p = Process(target=handle_account, args=(account,))
        processes.append(p)
        p.start()

    # Đợi tất cả các tiến trình hoàn thành
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
