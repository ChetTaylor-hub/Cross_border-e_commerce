'''
Author: TaoChen 2575394301qq.com
Date: 2024-02-02 11:44:31
LastEditors: TaoChen 2575394301qq.com
LastEditTime: 2024-02-02 12:44:24
FilePath: \kreslo1\license.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import datetime
import pickle
import os

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.subscription_end_date = None

    def subscribe(self, months):
        if self.subscription_end_date is None or self.subscription_end_date < datetime.datetime.now():
            self.subscription_end_date = datetime.datetime.now()
        self.subscription_end_date += datetime.timedelta(days=30*months)

class LicenseManager:
    def __init__(self, license_file):
        self.license_file = license_file
        if os.path.exists(self.license_file):
            with open(self.license_file, 'rb') as f:
                self.user = pickle.load(f)
        else:
            self.user = None

    def subscribe(self, name, email, months):
        if self.user is None:
            self.user = User(name, email)
        self.user.subscribe(months)
        with open(self.license_file, 'wb') as f:
            pickle.dump(self.user, f)

    def check_subscription(self):
        if self.user is None:
            return False
        return datetime.datetime.now() < self.user.subscription_end_date



# 使用示例
license_manager = LicenseManager('license.pkl')
# 用户订阅12个月
license_manager.subscribe('John Doe', 'john.doe@example.com', 12)
# 检查订阅状态
if license_manager.check_subscription():
    print('Subscription is active.')
else:
    print('Subscription haswi expired.')
