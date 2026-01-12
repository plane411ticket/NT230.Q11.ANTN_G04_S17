import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://learn.microsoft.com/en-us/windows/win32/api/"

def crawl_api_links():
    print("Đang xử lý URL:", BASE_URL)

    response = requests.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print("[LỖI] Không truy cập được trang:", response.status_code)
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Lấy hết anchor trong toàn trang
    all_links = soup.find_all("a")

    api_links = []

    for a in all_links:
        href = a.get("href")
        if not href:
            continue

        abs_url = urljoin(BASE_URL, href)

        # Lọc đúng link Win32 API
        if "/windows/win32/api/" in abs_url.lower():
            api_links.append(abs_url)

    # Loại trùng
    api_links = sorted(set(api_links))

    print(f"Thu được {len(api_links)} link API!")
    for url in api_links:
        print(url)

    with open("api_links.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(api_links))

    print("\nHoàn tất crawling!")

crawl_api_links()