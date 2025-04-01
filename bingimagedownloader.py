import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import parse_qs, urlparse
from PIL import Image
import io
import random
import time
# Ввод параметров пользователем
query = input("Введите запрос для поиска картинок: ")
folder_name = input("Введите имя папки для сохранения: ")
file_prefix = input("Введите префикс имени файлов: ")
max_images = int(input("Введите количество картинок для скачивания: "))
# Настройка
folder = folder_name
os.makedirs(folder, exist_ok=True)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
downloaded = 0
first = 1
seen_urls = set()
while downloaded < max_images:
    url = f"https://www.bing.com/images/search?q={query}&first={first}"
    print(f"Запрос страницы: {url}")
    time.sleep(1)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    image_links = soup.find_all("a", class_="iusc")
    print(f"Найдено ссылок: {len(image_links)}")
    if not image_links:
        print("Ссылки закончились или Bing блокирует")
        break
    image_links = list(image_links)
    random.shuffle(image_links)
    for link in image_links:
        try:
            href = link.get("href")
            parsed_url = urlparse(f"https://www.bing.com{href}")
            params = parse_qs(parsed_url.query)
            img_url = params.get("mediaurl", max_images)[0]
            if img_url and img_url.startswith("http"):
                if img_url in seen_urls:
                    continue
                img_data = requests.get(img_url, headers=headers).content
                img = Image.open(io.BytesIO(img_data))
                ext = ".png" if img.format == "PNG" else ".jpg"
                file_path = os.path.join(folder, f"{file_prefix}{downloaded+1}{ext}")
                img.save(file_path)
                seen_urls.add(img_url)
                downloaded += 1
                print(f"Скачано ({downloaded}/{max_images}): {file_path}")
                if downloaded >= max_images:
                    break
        except Exception as e:
            print(f"Ошибка: {e}")
            continue
    first += max(len(image_links), 35)
print(f"Готово! Скачано {downloaded} уникальных изображений")
