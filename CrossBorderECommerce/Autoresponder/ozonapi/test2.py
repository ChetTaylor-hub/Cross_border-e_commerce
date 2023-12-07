from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.ozon.ru/product/kreslo-kachalka-hlo-50h30h90-sm-1315792293/'  # 替换为目标网页的URL

# 设置 ChromeDriver 的路径，根据实际情况修改
chrome_driver_path = 'D:/ProgrmFiles/chromedriver_win32/chromedriver.exe'

# 创建 Chrome 浏览器实例
chrome_options = ChromeOptions()
# 添加一些配置，根据需要进行调整
chrome_options.add_argument('--headless')  # 可选择无头模式，不显示浏览器界面
chrome_service = ChromeService(executable_path=chrome_driver_path)
browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

# 访问目标网页
browser.get(url)

# 使用显式等待等待页面加载完成，根据实际情况调整超时时间和条件
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_element_located((By.ID, 'some-element-on-the-page')))

# 处理 Cloudflare 验证页面
# 在这里，您需要编写代码来模拟用户与页面的交互，可能包括填写表单、点击按钮等
# 以下是一个简单的示例，点击页面上的一个按钮，该按钮可能是 Cloudflare 验证中的一部分
button = browser.find_element(By.XPATH, '//button[@id="some-button"]')
button.click()

# 继续等待页面加载完成，以确保验证码或其他验证机制被成功处理
wait.until(EC.presence_of_element_located((By.ID, 'some-element-after-verification')))

# 获取页面源代码
page_source = browser.page_source

# 打印页面源代码，可以根据需要进行进一步处理
print(page_source)

# 关闭浏览器
browser.quit()
