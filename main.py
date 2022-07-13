import bs4
import requests
import re
from fake_headers import Headers

# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'литературы']


def super_article_serch(keywords):
    headers = Headers(browser='chrome', os="win", headers=True).generate()
    set_keywords = set(keywords)
    base_url = 'https://habr.com'
    url = base_url + '/ru/all/'
    response = requests.get(url, headers=headers)
    text = response.text
    soup = bs4.BeautifulSoup(text, features="html.parser")
    articles = soup.find_all("article")
    for article in articles:
        article_url = article.find(class_="tm-article-snippet__readmore").attrs["href"]
        article_response = requests.get(base_url+article_url, headers=headers)
        text_article = article_response.text
        soup_article = bs4.BeautifulSoup(text_article, features="html.parser")
        artikle_all = soup_article.find(id="post-content-body")
        artikle_all_set = set(re.findall(r'\w+', artikle_all.text))    # Множество слов всей статьи
        previe = article.find(class_="tm-article-body tm-article-snippet__lead").text
        previe_words_set = set(re.findall(r'\w+', previe))    # Множество слов превью статьи
        if len(previe_words_set.intersection(set_keywords)) != 0 or len(artikle_all_set.intersection(set_keywords)) != 0:
            date = article.find(class_="tm-article-snippet__datetime-published").find("time").attrs["title"].split(",")[0]
            title = article.find("h2").find("span").text
            href = article.find(class_="tm-article-snippet__title-link").attrs["href"]
            result = f'{date} - {title} - {base_url+href}'
            print(result)


if __name__ == '__main__':
    super_article_serch(KEYWORDS)
