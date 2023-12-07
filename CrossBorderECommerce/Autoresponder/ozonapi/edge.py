from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.ozon.ru/product/kreslo-kachalka-hlo-50h30h90-sm-1315792293/'

# 设置 EdgeDriver 的路径，根据实际情况修改
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

# 使用显式等待等待页面加载完成，根据实际情况调整超时时间和条件
wait = WebDriverWait(browser, 1000)
wait.until(EC.presence_of_element_located((By.ID, "layoutPage")))

# 处理 Cloudflare 验证页面
# 在这里，您需要编写代码来模拟用户与页面的交互，可能包括填写表单、点击按钮等
# 以下是一个简单的示例，点击页面上的一个按钮，该按钮可能是 Cloudflare 验证中的一部分
# button = browser.find_element(By.XPATH, '//button[@id="state-webInstallmentPurchase-2111450-default-1"]')
# button.click()
# 找到按钮并点击
button = browser.find_element(By.XPATH, f"//button[@class='rb']")
button.click()

# 继续等待页面加载完成，以确保验证码或其他验证机制被成功处理
wait.until(EC.presence_of_element_located((By.ID, "layoutPage")))

# 获取页面源代码
page_source = browser.page_source

# 打印页面源代码，可以根据需要进行进一步处理
print(page_source)

# 关闭浏览器
browser.quit()
