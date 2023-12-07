from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
import time

url = 'https://www.ozon.ru/complaint/support/?incident_id=964080LGBGEF'  # 替换为您实际的 URL

# 设置 ChromeDriver 的路径，根据实际情况修改
edge_driver_path = 'D:/ProgrmFiles/msedgedriver.exe'

# 创建 Edge 浏览器实例
edge_options = EdgeOptions()
edge_service = EdgeService(executable_path=edge_driver_path)
# 添加一些配置，根据需要进行调整
# edge_options.add_argument('--headless')

# 注意这里使用 edge_options 作为第一个参数
browser = webdriver.Edge(service=edge_service, options=edge_options)

# 访问目标网页
browser.get(url)

# 等待页面加载完成，根据实际情况调整等待时间
time.sleep(1000)

# 找到按钮并点击
button = browser.find_element_by_xpath('//button[@class="rb"]')
button.click()

# 等待页面刷新完成，根据实际情况调整等待时间
time.sleep(5)

# 获取刷新后的页面源代码
page_source = browser.page_source

# 打印页面源代码，可以根据需要进行进一步处理
print(page_source)

# 关闭浏览器
browser.quit()
