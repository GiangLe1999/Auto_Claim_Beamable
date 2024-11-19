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
        "chrome_path": "C:\\Others\\Tele Accounts\\84826519744\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "C:\\Others\\Tele Accounts\\84826519744\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9227,  # Cổng Remote Debugging riêng
        "window_size": "500,700",  # Kích thước cửa sổ
        "window_position": "0,0"   # Vị trí cửa sổ
    },
    {
        "name": "Diễm Hằng Xinh Đẹp",
        "chrome_path": "C:\\Others\\Tele Accounts\\84929895980\\GoogleChromePortable\\GoogleChromePortable.exe",
        "user_data_dir": "C:\\Others\\Tele Accounts\\84929895980\\GoogleChromePortable\\Data\\profile\\Default",
        "debug_port": 9228,  # Cổng Debug riêng
        "window_size": "500,700",
        "window_position": "500,0"
    },
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
        "window_position": "1400,0"
    }
]

# Hàm khởi tạo Selenium
def init_driver(account):
    options = webdriver.ChromeOptions()
    options.binary_location = account["chrome_path"]
    options.add_argument(f"--user-data-dir={account['user_data_dir']}")  # Thư mục dữ liệu riêng
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument(f"--remote-debugging-port={account['debug_port']}")  # Cổng Debug riêng

    # Kích thước và vị trí cửa sổ từ cấu hình
    window_size = account.get("window_size", "500,700")
    window_position = account.get("window_position", "0,0")
    options.add_argument(f"--window-size={window_size}")
    options.add_argument(f"--window-position={window_position}")

    # Sử dụng webdriver-manager để tự động tải ChromeDriver
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

# Hàm xử lý logic chính
def handle_account(account, action):
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

        if action == "1":  # Điểm danh hàng ngày
            try:
                # Chờ nút "Mission" xuất hiện và click vào
                mission_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Mission']"))
                )
                mission_button.click()
                print("Đã click vào nút Mission...")
                time.sleep(5)

                # Kiểm tra ngay xem có thông báo đã điểm danh chưa
                already_checked_in_message = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//p[contains(text(), \"You've already checked in for today.\")]"))
                )
                print(f"Tài khoản {account['name']} đã điểm danh trước đó. Thoát profile.")
                return

            except:
                # Nếu không có thông báo thì thực hiện điểm danh
                pass

            # Chờ nút "Check In" xuất hiện và click vào
            check_in_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Check In')]"))
            )
            check_in_button.click()
            print("Đã click vào nút Check In...")
            time.sleep(5)

            # Chờ thông báo điểm danh thành công
            check_in_success_message = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(text(), \"You've already checked in for today.\")]"))
            )
            print(f"Tài khoản {account['name']} đã điểm danh thành công.")

        elif action == "2":  # Claim tự động
            # Biến thời gian chờ để Claim lần tiếp theo
            wait_time_seconds = 7230

            while True:
                try:
                    # Tìm nút Claim và click
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

                    # Sau khi Claim thành công, đặt thời gian chờ mặc định
                    wait_time_seconds = 7230
                except:
                    try:
                        # Nếu không tìm thấy nút Claim, tìm phần tử thời gian đếm ngược
                        countdown_timer = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//div[contains(@class, 'bg-gradient-to-b')]//span[contains(text(), ':')]")
                            )
                        )
                        countdown_text = countdown_timer.text.strip()
                        print(f"Đã tìm thấy thời gian đếm ngược: {countdown_text}")

                        # Tính toán thời gian chờ từ text "01:22:08"
                        hours, minutes, seconds = map(int, countdown_text.split(":"))
                        wait_time_seconds = hours * 3600 + minutes * 60 + seconds + 5 # 5s cộng thêm để tránh lỗi
                        print(f"Thời gian chờ tới lần Claim tiếp theo: {wait_time_seconds} giây")
                    except Exception as e:
                        print(f"Lỗi khi tìm kiếm thời gian đếm ngược hoặc Claim: {e}")
                        # Nếu không tìm thấy gì, chờ một khoảng thời gian ngắn trước khi thử lại
                        wait_time_seconds = 60  # Mặc định chờ 60 giây

                # Chờ tới lần Claim tiếp theo
                print(f"Chờ {wait_time_seconds} giây để tiếp tục Claim...")
                time.sleep(wait_time_seconds)

                # Chuyển lại vào iframe để tiếp tục tìm kiếm
                try:
                    driver.switch_to.default_content()  # Chuyển về ngữ cảnh chính
                    iframe = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
                    )
                    driver.switch_to.frame(iframe)  # Chuyển lại vào iframe
                except Exception as e:
                    print(f"Lỗi khi chuyển đổi iframe: {e}")
                    break

    except Exception as e:
        print(f"Lỗi xảy ra với tài khoản {account['name']}: {e}")

    finally:
        if driver:
            driver.quit()
            print(f"Đã đóng trình duyệt cho tài khoản: {account['name']}")

# Hàm chính
def main():
    # Prompt để người dùng chọn hành động
    print("Chọn hành động bạn muốn thực hiện:")
    print("1: Điểm danh hàng ngày")
    print("2: Claim tự động")
    action = input("Nhập số (1 hoặc 2): ")

    if action not in ["1", "2"]:
        print("Hành động không hợp lệ! Vui lòng chạy lại chương trình.")
        return

    processes = []
    for account in accounts:
        # Tạo một tiến trình riêng cho mỗi tài khoản
        p = Process(target=handle_account, args=(account, action))
        processes.append(p)
        p.start()

    # Đợi tất cả các tiến trình hoàn thành
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
