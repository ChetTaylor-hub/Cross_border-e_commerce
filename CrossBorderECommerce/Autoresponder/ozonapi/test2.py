from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from bs4 import BeautifulSoup
import time

url = "https://www.ozon.ru/product/kreslo-kachalka-hlo-50h30h90-sm-1315792293/"

# 设置 EdgeDriver 的路径，根据实际情况修改
edge_driver_path = 'D:/ProgrmFilesms/edgedriver.exe'

# 创建 Edge 浏览器实例
edge_options = EdgeOptions()
# 添加一些配置，根据需要进行调整
# edge_options.add_argument('--headless')

# 创建 Edge 浏览器服务
edge_service = EdgeService(edge_driver_path)

# 注意这里使用 edge_options 作为第一个参数
browser = webdriver.Edge(service=edge_service, options=edge_options)

# 访问目标网页
browser.get(url)

# 等待 JavaScript 执行，时间根据实际情况调整
time.sleep(5)

# 获取页面源代码
page_source = browser.page_source

# 关闭浏览器
browser.quit()

# 使用 BeautifulSoup 解析页面源代码
soup = BeautifulSoup(page_source, 'html.parser')

# 在这里，您可以使用 BeautifulSoup 的方法来提取您需要的信息
# 例如：target_content = soup.find('div', class_='your-class-name').text

# 打印提取到的信息
print(soup.prettify())