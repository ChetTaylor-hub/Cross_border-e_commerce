import requests
from bs4 import BeautifulSoup

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 在这里添加代码来提取你需要的数据
    # 例如：soup.find_all('div', class_='your_class')
    main_content = soup.find_all('div', class_='main-content')

    print(main_content)
    return soup

url = 'https://www.ozon.ru/product/kreslo-kachalka-hlo-50h30h90-sm-1315792293/'
data = get_data(url)
print(data)
