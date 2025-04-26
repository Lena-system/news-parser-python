import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def parse_news(url, output_file='news.csv'):

    try:
        # Заголовки для имитации браузера
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Загрузка страницы
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки

        # Парсинг HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Предполагаемая структура новостей (подстройте под нужный сайт)
        news_items = soup.find_all('div', class_='news-item') or soup.find_all('article')

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Заголовки CSV
            writer.writerow(['Title', 'Link', 'Date', 'Summary'])

            for item in news_items:
                try:
                    # Извлечение данных (адаптируйте под структуру целевого сайта)
                    title = item.find('h2').text.strip() if item.find('h2') else 'No title'
                    link = item.find('a')['href'] if item.find('a') else '#'
                    date = item.find('time')['datetime'] if item.find('time') else datetime.now().isoformat()
                    summary = item.find('p').text.strip() if item.find('p') else ''

                    # Запись в CSV
                    writer.writerow([title, link, date, summary])

                except Exception as e:
                    print(f"Ошибка при обработке элемента: {e}")
                    continue

        print(f"Данные сохранены в {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
    except Exception as e:
        print(f"Общая ошибка: {e}")

if __name__ == "__main__":

    #здесь ссылка на целевой сайт target_url = ""
    parse_news(target_url)