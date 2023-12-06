import cloudscraper
from bs4 import BeautifulSoup

url = "https://www.ozon.ru/product/kreslo-kachalka-hlo-50h30h90-sm-1315792293/"

# 创建 cloudscraper 实例
scraper = cloudscraper.create_scraper()

# 获取页面内容
response = scraper.get(url)

# 使用 BeautifulSoup 解析页面源代码
soup = BeautifulSoup(response.text, 'html.parser')

# 在这里，您可以使用 BeautifulSoup 的方法来提取您需要的信息
# 例如：target_content = soup.find('div', class_='your-class-name').text

# 打印提取到的信息
print(soup.prettify())
