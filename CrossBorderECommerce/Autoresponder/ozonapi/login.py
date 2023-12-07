import requests

# 目标网站的登录页面 URL
login_url = 'https://www.ozon.ru/product/kreslo-kachalka-hlo-50h30h90-sm-1315792293/'

# 构造登录时提交的表单数据，包括用户名和密码
login_data = {
    'username': 'your_username',
    'password': 'your_password',
}

# 使用 Session 对象保持登录状态
session = requests.Session()

# 发送登录请求
response = session.post(login_url, data=login_data)

# 检查登录是否成功
if response.status_code == 200:
    print('登录成功！')
    # 在登录成功后，可以继续访问其他页面或获取需要的信息
    # 例如，访问需要登录的页面
    target_url = 'https://example.com/target_page'
    target_response = session.get(target_url)
    # 处理 target_response 中的内容，提取所需信息
else:
    print('登录失败，状态码：', response.status_code)
