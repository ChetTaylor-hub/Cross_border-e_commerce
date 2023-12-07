import requests
from bs4 import BeautifulSoup

def get_data(url):
    


    # headers = {
    # "Client-Id": "1499102",
    # "Api-Key": "d8c89da0-9caa-4d70-b034-54a2f21c94a2",
    # }

    headers = {
        "Origin": "https://www.ozon.ru",
        "Referer": "https://www.ozon.ru/product/kreslo-kachalka-hlo-50h30h90-sm-1315792293/",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # headers= {
    #     "Accept": "image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*", 
    #     "Accept-Encoding": "gzip, deflate", 
    #     "Accept-Language": "zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3", 
    #     "Host": "httpbin.org", 
    #     "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; wbx 1.0.0; wbxapp 1.0.0; Zoom 3.6.0)", 
    #     "X-Amzn-Trace-Id": "Root=1-628b672d-4d6de7f34d15a77960784504"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"data = {soup}")
    
    # 在这里添加代码来提取你需要的数据
    # 例如：soup.find_all('div', class_='your_class')
    # main_content = soup.find_all('div', class_='main-content')

    # print(main_content)
    # return soup

url = 'https://www.ozon.ru/product/kreslo-kachalka-hlo-50h30h90-sm-1315792293/'
data = get_data(url)
print(data)

