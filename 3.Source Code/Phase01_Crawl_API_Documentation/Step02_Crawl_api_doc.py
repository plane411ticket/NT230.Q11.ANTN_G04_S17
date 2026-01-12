import csv
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def crawl_with_selenium(urls, csv_filename):
    
    # Cấu hình Selenium chạy ẩn
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Khởi tạo WebDriver
    try:
        service = Service(executable_path=r"C:\Users\khidot411\Downloads\exe\chromedriver-win64\chromedriver-win64\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Đã khởi tạo Selenium WebDriver (headless)...")
    except Exception as e:
        print(f"[LỖI] Không khởi tạo được WebDriver: {e}")
        print("Vui lòng kiểm tra bạn đã tải chromedriver.exe và để đúng thư mục chưa.")
        return

    with open ("error.csv", mode='w', newline='', encoding='utf-8') as file_error, \
         open(csv_filename, mode='w', newline='', encoding='utf-8') as file_ok:
        
        writer_error = csv.writer(file_error)
        writer_error.writerow(['Link'])
        print(f"Đã mở file error.csv để ghi...")
    
        writer = csv.writer(file_ok)
        writer.writerow(['Cot_1_DEF', 'Cot_2_ABC'])
        print(f"Đã mở file {csv_filename} để ghi...")


        for url in urls:
            print(f"Đang xử lý URL: {url}")
            try:
                # Tải trang 
                driver.get(url)

                # Chờ cho bảng chứa thông tin xuất hiện
                table_xpath = "//table[@aria-label='Functions']"
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, table_xpath))
                )
                print("  Đã tìm thấy bảng (nội dung JavaScript đã tải xong).")

                # Lấy HTML sau khi JavaScript đã chạy
                page_source = driver.page_source

                # Parse HTML bằng lxml
                tree = etree.HTML(page_source)

                # Xây dựng XPath 
                rows_xpath = "//table[@aria-label='Functions']/tbody/tr"
                rows = tree.xpath(rows_xpath)

                if not rows:
                    print(f"  [LỖI] Đã chờ nhưng vẫn không tìm thấy hàng nào. URL: {url}")
                    writer_error.writerow(url)
                    continue

                print(f"  Tìm thấy {len(rows)} hàng (tr) trong bảng.")

                # Lặp qua các hàng
                for row in rows:
                    td = row.find("./td")
                    if td is not None:
                        all_strings = [s.strip() for s in td.xpath(".//text()") if s.strip()]
                        if len(all_strings) >= 2:
                            def_text = all_strings[0]
                            abc_text = all_strings[1]
                            writer.writerow([def_text, abc_text])
                        else:
                            writer_error.writerow(url)
                            print(f"    [CẢNH BÁO] Hàng không đúng định dạng: {etree.tostring(row, method='text', encoding='unicode').strip()}")
                    else:
                        writer_error.writerow(url)
                        print(f"    [CẢNH BÁO] Hàng không có <td>")

            except Exception as e:
                writer_error.writerow(url)
                print(f"  [LỖI] Xử lý {url} thất bại: {e}")

    # Đóng trình duyệt sau khi làm xong
    driver.quit()
    print(f"\nHoàn tất! Dữ liệu đã được lưu vào file {csv_filename}")

def load_urls_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]
    return urls

urls_to_crawl = load_urls_from_file("api_links.txt")
output_filename = "data_da_crawl_selenium02.csv"
crawl_with_selenium(urls_to_crawl, output_filename)