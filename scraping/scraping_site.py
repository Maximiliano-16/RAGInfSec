import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

# Базовый URL сайта
BASE_URL = "https://matchtv.ru"
# URL страницы списка новостей по футболу
NEWS_LIST_URL = "https://matchtv.ru/news/football"
# Заголовки запроса (User-Agent рекомендуется менять, чтобы эмулировать браузер)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.93 Safari/537.36"
}


def get_all_news_links():
    """
    Функция собирает ссылки на все новости со страниц списка новостей.

    Идея такая:
    - Начинаем с первой страницы (NEWS_LIST_URL).
    - Извлекаем все ссылки на новости, используя селектор для тега <a> с классом "node-news-list__item".
    - Пытаемся найти на странице ссылку на следующую страницу.
      Здесь предполагается, что для кнопки перехода на следующую страницу используется класс "pagination__next".
    - Если ссылка на следующую страницу найдена, переходим по ней и повторяем процесс.

    Возвращает список полных URL новостей.
    """
    news_links = []
    next_page_url = NEWS_LIST_URL  # Начинаем с первой страницы

    while next_page_url:
        print(f"Парсинг страницы: {next_page_url}")
        response = requests.get(next_page_url, headers=HEADERS)
        if response.status_code != 200:
            print("Ошибка при запросе страницы:", next_page_url)
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем все ссылки на новости
        for a_tag in soup.find_all("a", class_="node-news-list__item"):
            href = a_tag.get("href")
            if href:
                # Если ссылка относительная, приводим её к абсолютной
                full_url = urljoin(BASE_URL, href)
                news_links.append(full_url)

        # Поиск ссылки на следующую страницу.
        # Замечание: селектор для "следующей страницы" может отличаться от приведённого.
        next_button = soup.find("a", class_="pagination__next")
        if next_button and next_button.get("href"):
            next_page_url = urljoin(BASE_URL, next_button.get("href"))
            # Задержка между запросами, чтобы не нагружать сервер
            time.sleep(1)
        else:
            # Если следующей страницы нет, выходим из цикла
            next_page_url = None

    return news_links


def parse_news_page(url):
    """
    Функция получает страницу конкретной новости и извлекает из неё весь текст,
    который находится в тегах <p>.

    Аргументы:
        url (str): Полный URL страницы новости.

    Возвращает:
        text (str): Объединённый текст всех найденных тегов <p>.
    """
    print(f"Парсинг новости: {url}")
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print("Ошибка при запросе новости:", url)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    # Ищем все теги <p> на странице
    paragraphs = soup.find_all("p")
    # Получаем текст из каждого <p> и объединяем с переходом на новую строку
    text = "\n".join([p.get_text(strip=True) for p in paragraphs])
    return text


def main():
    # Сначала получаем все ссылки на новости
    news_links = get_all_news_links()
    print(f"Найдено {len(news_links)} новостей.")

    # Проходим по каждой новости и получаем её текст
    for link in news_links:
        news_text = parse_news_page(link)
        if news_text:
            print("=" * 80)
            print(f"Новость: {link}")
            print(news_text)
            # Задержка между запросами, чтобы не перегружать сервер
            time.sleep(1)


if __name__ == "__main__":
    main()
