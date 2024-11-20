from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import datetime
from multiprocessing import Process, Event

# Cấu hình tài khoản
accounts = [
    # {
    #     "name": "Hải Bình Ngu Ngốc",
    #     "chrome_path": "C:\\Others\\Tele Accounts\\84826519744\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "C:\\Others\\Tele Accounts\\84826519744\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9227,  # Cổng Remote Debugging riêng
    #     "window_size": "500,700",  # Kích thước cửa sổ
    #     "window_position": "0,0"   # Vị trí cửa sổ
    # },
    # {
    #     "name": "Diễm Hằng Xinh Đẹp",
    #     "chrome_path": "C:\\Others\\Tele Accounts\\84929895980\\GoogleChromePortable\\GoogleChromePortable.exe",
    #     "user_data_dir": "C:\\Others\\Tele Accounts\\84929895980\\GoogleChromePortable\\Data\\profile\\Default",
    #     "debug_port": 9228,  # Cổng Debug riêng
    #     "window_size": "500,700",
    #     "window_position": "500,0"
    # },
    {
        "name": "Bình Minh Lên Rồi",
        "chrome_path": "C:\\Others\\Tele Accounts\\84925599903\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "C:\\Others\\Tele Accounts\\84925599903\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9223,  # Cổng Remote Debugging riêng
        "window_size": "500,700",
        "window_position": "1000,0"
    },
    {
        "name": "Đình Diệu Diệu Kỳ",
        "chrome_path": "C:\\Others\\Tele Accounts\\84567845408\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "C:\\Others\\Tele Accounts\\84567845408\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9224,  # Cổng Remote Debugging riêng
        "window_size": "500,700",
        "window_position": "1500,0"
    }
]

# Thêm một Event để dừng tất cả các tiến trình
shutdown_event = Event()

# Hàm kiểm tra thời gian và tắt máy
def shutdown_at_target_time(target_hour, target_minute):
    print(f"Hẹn giờ tắt máy lúc {target_hour:02d}:{target_minute:02d} (giờ Việt Nam)...")
    while not shutdown_event.is_set():
        now = datetime.datetime.now()
        # Chuyển sang múi giờ Việt Nam (+7 GMT nếu cần thiết)
        current_hour = now.hour
        current_minute = now.minute

        if current_hour == target_hour and current_minute >= target_minute:
            print("Đã đến thời gian hẹn giờ! Dừng chương trình và tắt máy tính...")
            shutdown_event.set()  # Gửi tín hiệu dừng đến tất cả tiến trình

            # Tắt máy tính
            if os.name == 'nt':  # Windows
                os.system("shutdown /s /t 1")
            else:  # Linux/MacOS
                os.system("shutdown now")

            break
        time.sleep(10)  # Kiểm tra mỗi 10 giây

# Hàm khởi tạo Selenium driver
def init_driver(account):
    options = webdriver.ChromeOptions()
    options.binary_location = account["chrome_path"]
    options.add_argument(f"--user-data-dir={account['user_data_dir']}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument(f"--remote-debugging-port={account['debug_port']}")

    # Kích thước và vị trí cửa sổ từ cấu hình
    window_size = account.get("window_size", "500,700")
    window_position = account.get("window_position", "0,0")
    options.add_argument(f"--window-size={window_size}")
    options.add_argument(f"--window-position={window_position}")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

# Hàm thực hiện các thao tác trên MetaCat Bot
def perform_meta_cat_actions(driver, account):
    try:
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

        # Chuyển sang iframe
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        print("Đã chuyển sang iframe của MetaCat Bot...")

        # Click nút Claim now
        claim_now_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Claim now')]"))
        )
        claim_now_button.click()
        print("Đã click vào nút Claim now...")
        time.sleep(10)
    except Exception as e:
        print(f"Lỗi khi thực hiện thao tác trên MetaCat Bot cho tài khoản {account['name']}: {e}")

# Hàm thực hiện logic điểm danh hàng ngày
def handle_daily_check_in(driver, account):
    try:
        perform_meta_cat_actions(driver, account)

        # Click nút Mission
        mission_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Mission']"))
        )
        mission_button.click()
        print(f"Đã click vào nút Mission cho tài khoản: {account['name']}")
        time.sleep(5)

        # Kiểm tra thông báo đã điểm danh
        try:
            already_checked_in_message = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(text(), \"You've already checked in for today.\")]"))
            )
            print(f"Tài khoản {account['name']} đã điểm danh trước đó.")
        except:
            # Thực hiện điểm danh
            check_in_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Check In')]"))
            )
            check_in_button.click()
            print(f"Đã điểm danh thành công cho tài khoản: {account['name']}")
            time.sleep(5)

            driver.quit()
    except Exception as e:
        print(f"Lỗi khi thực hiện điểm danh hàng ngày cho tài khoản {account['name']}: {e}")

# Hàm get thời gian chờ
def get_wait_time_from_countdown(driver, xpath, default_wait=60):
    try:
        countdown_timer = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        countdown_text = countdown_timer.text.strip()
        print(f"Thời gian đếm ngược tìm thấy: {countdown_text}")

        # Tính toán thời gian chờ từ định dạng hh:mm:ss
        hours, minutes, seconds = map(int, countdown_text.split(":"))
        wait_time_seconds = hours * 3600 + minutes * 60 + seconds + 5  # Thêm 5 giây để tránh lỗi
        print(f"Thời gian chờ tiếp theo: {wait_time_seconds} giây")
        return wait_time_seconds
    except Exception as e:
        print(f"Lỗi khi tính toán thời gian chờ: {e}")
        return default_wait

# Hàm Claim và quản lý thời gian chờ
def handle_claim(driver,account):
    is_first_claim = True  # Cờ xác định lần đầu claim

    while True:
        try:
            if not is_first_claim:
                # Khởi tạo lại driver nếu không phải lần đầu claim
                print(f"Khởi tạo lại trình duyệt cho tài khoản: {account['name']}")
                driver = init_driver(account)

            # Bắt đầu thực hiện các thao tác
            perform_meta_cat_actions(driver, account)

            # Thực hiện Claim
            claim_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//img[@alt='Claim']"))
            )
            claim_button.click()
            print(f"Đã Claim thành công cho tài khoản: {account['name']}")
            time.sleep(10)

            # Click nút Close
            close_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close')]"))
            )
            close_button.click()
            print("Đã click vào nút Close để xác nhận Transaction...")
            time.sleep(5)

            # Lấy thời gian chờ từ đồng hồ đếm ngược
            wait_time_seconds = get_wait_time_from_countdown(
                driver,
                xpath="//div[contains(@class, 'bg-gradient-to-b')]//span[contains(text(), ':')]",
                default_wait=60  # Thời gian chờ mặc định nếu không tìm thấy đồng hồ
            )
            print(f"Đặt thời gian chờ: {wait_time_seconds} giây")

        except Exception as e:
            try:
                # Nếu không tìm thấy nút Claim, kiểm tra thời gian chờ
                wait_time_seconds = get_wait_time_from_countdown(
                    driver,
                    xpath="//div[contains(@class, 'bg-gradient-to-b')]//span[contains(text(), ':')]",
                    default_wait=60
                )
                print(f"Thời gian chờ tiếp theo: {wait_time_seconds} giây")

            except Exception as countdown_exception:
                print(f"Lỗi khi tính toán thời gian chờ: {countdown_exception}")
                wait_time_seconds = 60  # Giá trị chờ mặc định nếu không tìm thấy thời gian

        finally:
            # Đóng trình duyệt
            if driver:
                driver.quit()
                print(f"Đã đóng trình duyệt cho tài khoản: {account['name']}")

            # Cập nhật trạng thái lần đầu
            is_first_claim = False

            # Chờ trước khi mở lại và tiếp tục vòng lặp
            print(f"Chờ {wait_time_seconds} giây trước khi tiếp tục...")
            time.sleep(wait_time_seconds)


def claim_process(account):
    # Hàm khởi tạo và xử lý logic Claim
    driver = init_driver(account)
    while not shutdown_event.is_set():
        handle_claim(driver, account)

def daily_check_in_process(account):
    # Hàm khởi tạo và xử lý logic Điểm danh hàng ngày
    driver = init_driver(account)
    while not shutdown_event.is_set():
        handle_daily_check_in(driver, account)

def main():
    print("Chọn hành động bạn muốn thực hiện:")
    print("1: Điểm danh hàng ngày")
    print("2: Claim tự động")
    action = input("Nhập số (1 hoặc 2): ")

    # Đặt giờ tắt máy (giờ Việt Nam, ví dụ: 23:30)
    target_hour = 23
    target_minute = 30

    processes = []

    # Khởi động tiến trình hẹn giờ
    shutdown_process = Process(target=shutdown_at_target_time, args=(target_hour, target_minute))
    shutdown_process.start()
    processes.append(shutdown_process)

    # Khởi động tiến trình chính theo lựa chọn của người dùng
    for account in accounts:
        if action == "1":
            # Truyền hàm target là daily_check_in_process
            p = Process(target=daily_check_in_process, args=(account,))
        elif action == "2":
            # Truyền hàm target là claim_process
            p = Process(target=claim_process, args=(account,))
        else:
            print("Hành động không hợp lệ! Vui lòng chọn 1 hoặc 2.")
            return

        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == "__main__":
    main()
