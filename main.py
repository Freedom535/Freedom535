import requests
from bs4 import BeautifulSoup
import json
import time
start_time = time.time()
def get_data():
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    projects_data_list = []
    projects_urls = []
    url = 'https://am.ua/uk/mototsikly/'
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    all_pages = soup.find('a', class_='cm-history ty-pagination__item hidden-phone ty-pagination__range cm-ajax').text
    pages = all_pages.split(' ')[2]
    hrefs = []
    for i in range(1, int(pages) + 1):
        url = f"https://am.ua/uk/mototsikly/page-{i}/"
        r = requests.get(url=url, headers=headers)
        # save data
        with open(f"data/page_{i}.html", "w", encoding='utf-8') as file:
            file.write(r.text)
        with open(f"data/page_{i}.html", encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        articles = soup.find_all('div', class_='ut2-gl__name')
        for article in articles:
            project_url =  article.find('a').get('href')
            projects_urls.append(project_url)
    for project_url in projects_urls:
        req = requests.get(project_url, headers)
        soup = BeautifulSoup(req.text, "lxml")
        try:
            name = soup.find(class_='ut2-pb__title').text
        except Exception:
            name = 'Немає назви'
        try:
            price = soup.find(class_='ty-price-num').text
        except Exception:
            price  = 'Ціна не вказана'
        try:
            availability = soup.find(class_='ty-qty-in-stock ty-control-group__item').text.strip('\n')
            availability.rstrip('')
            availability.rstrip('\n')
        except Exception:
            availability = 'Немає в наявності'
        try:
            brand = soup.find('div' ,class_='ty-product-feature__value').find('a').text
        except Exception:
            brand = 'Немає бренду'
        projects_data_list.append(
            {
                "Назва товару": name,
                "Ціна товару": price,
                "Бренд товару": brand,
                "Наявність товару": availability
            }
        )
        print(projects_data_list)
    # save results
    with open("data/projects_data.json", "a", encoding="utf-8") as file:
        json.dump(projects_data_list, file, indent=4, ensure_ascii=False)
    finis_time = time.time() - start_time
    print(f'Затраченое время на работу скрипта {finis_time}')

def main():
    get_data()
if __name__ == '__main__':
    main()