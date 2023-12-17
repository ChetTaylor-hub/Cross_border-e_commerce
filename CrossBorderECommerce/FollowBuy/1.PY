import json
import requests
import pandas as pd

htnl_id=input('请输入您的id：')
html_id_1="https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=%2Fproduct%2Fkreslo-kachalka-hlo-50h30h90-sm-"+htnl_id
html=html_id_1+"%2F%3Flayout_container%3DpdpPage2column%26layout_page_index%3D2%26sh%3DxJRILtoOPA%26start_page_id%3Db52f7f930c7289a5ff0baaa9d8fa25f8"
print("请打开网站复制网页内容并保存为txt文件到代码根目录："+html)

response = requests.get(html)

# 打开文件（替换成你的文件路径）
file_path = input('请输入您保存的文件名不用加后缀：') + '.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    # 读取文件内容
    file_content = file.read()


text_1=json.loads(file_content)
a=text_1['widgetStates']["webSellerList-711858-pdpPage2column-2"]

a_1=json.loads(a)
a_2=a_1['sellers']
data=[]
for i in a_2:
    print("id为："+str(i['sku']))
    print("用户名为："+str(i['name']))
    print("网站为："+str(i['productLink']))
    data.append([i['sku'],i['name'],i['productLink']])

    try:
            # 如果文件存在，则读取已有的CSV文件
        df = pd.read_csv('数据.csv', encoding='utf-8')
    except FileNotFoundError:
            # 如果文件不存在，则创建一个新的DataFrame
        df = pd.DataFrame(columns=['ID', '用户名', '链接'])

        # 将多组数据逐一添加到DataFrame中
    for d in data:
            df = pd.concat([df, pd.DataFrame({'ID': [d[0]], '用户名': [d[1]], '链接': [d[2]]})], ignore_index=True)

        # 将DataFrame保存为CSV文件
    
    df.to_csv('数据内容.csv', mode='w', header=True, index=False, encoding='utf-8')
    print("已保存到数据内容.csv")
        


