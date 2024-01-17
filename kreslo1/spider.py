#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "2.0.1"
__date__ = "2023/11/28"
__author__ = ["Administrator"]
__description__ = "此文件说明"

import csv
import os
import time
from typing import Union

import requests
from loguru import logger
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger.add("log.log")
cur_dir = os.path.dirname(__file__)

logger.info(f"当前路径：{cur_dir}")


class SpiderShop:
    driver = None
    shop_name = {}
    browser = "chrome"  # chrome   firefox

    @classmethod
    def need_driver(cls, need=True):
        service = None

        options = Options()
        chromedriver = os.path.join(cur_dir, "chromedriver.exe")
        if os.path.exists(chromedriver):
            service = Service(executable_path=chromedriver)
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        options.add_argument(
            f"--user-agent='{user_agent}'")

        if need:
            options.add_argument('--incognito')
            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')
            options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
            cls.driver = webdriver.Chrome(service=service, options=options)
        else:
            os.system(rf'start chrome --remote-debugging-port=19521 --user-data-dir="C:\selenium"')  # --disable-plugins
            options.add_experimental_option("debuggerAddress", "127.0.0.1:19521")
            # options.add_experimental_option('useAutomationExtension', False)
            cls.driver = webdriver.Chrome(service=service, options=options)
            # cls.driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
            # cls.driver.execute_cdp_cmd('Network.clearBrowserCache', {})
            # cls.driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
            cls.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                          get: () => undefined
                        })
                      """
            })

    @classmethod
    def init_driver(cls):
        cls.need_driver(False)
        cls.driver.maximize_window()

    @classmethod
    def is_find_element(cls, by=None, value=None, timeout: Union[int, float] = 0.5):
        # try:
        #     wait = WebDriverWait(cls.driver, timeout, poll_frequency=0.5)
        #     element = wait.until(EC.presence_of_element_located((by, value)))
        # except (TimeoutException, NoSuchElementException):
        #     element = None
        # return element
        for _ in range(20):
            try:
                el = cls.driver.find_element(by=by, value=value)
                # if el.is_displayed():
                return el
                # time.sleep(0.2)
            except NoSuchElementException:
                time.sleep(timeout)
                continue

    @classmethod
    def click(cls, elment):
        try:
            elment.click()
        except Exception as e:
            # actions = ActionChains(cls.driver)
            # actions.move_to_element(elment).click().perform()
            cls.driver.execute_script("arguments[0].click();", elment)

    @classmethod
    def find_shop(cls, url, name, shop_el):
        sid = None
        for i in range(3):
            if new_page_el := cls.is_find_element(by=By.XPATH, value=shop_el, timeout=0.5):
                logger.debug(f"点击：{name}")
                cls.click(new_page_el)
                # //*[@id="layoutPage"]/div[1]/div[4]/div[2]/div/div/div[2]/span
                a = cls.is_find_element(by=By.XPATH,
                                        value='//*[@id="layoutPage"]/div[1]/div[4]/div[2]/div/div/div[2]/span')

                cur_url = cls.driver.current_url

                if cur_url == url or cur_url in list(cls.shop_name.values()):
                    logger.debug("向下滑动1")
                    scroll_script = f"window.scrollTo(0, 0);"
                    cls.driver.execute_script(scroll_script)

                    scroll_script = f"window.scrollTo(0, {900 + i * 100});"
                    cls.driver.execute_script(scroll_script)
                    continue
                # //*[@id="layoutPage"]/div[1]/div[4]/div[2]/div/div/div[2]/span/text()[2]
                if _ := cls.is_find_element(by=By.XPATH,
                                            value='//*[@id="layoutPage"]/div[1]/div[4]/div[2]/div/div/div[2]/span'):
                    sid = _.text.strip().split(":")[-1].split()
                    sid = sid[0] if sid else None
                logger.debug(f"{name} | {cur_url}")
                cls.shop_name[name] = [cur_url, sid]
                cls.save_csv([sid, cur_url])
                time.sleep(3)
                break
            else:
                # print("向下滑动2")
                scroll_script = f"window.scrollTo(0, {1000 + i * 300});"
                cls.driver.execute_script(scroll_script)
        else:
            logger.debug(f"{name}没找到")

    @classmethod
    def veify_api(cls):
        url = "https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=/searchSuggestions/?text=&url=/search/?text={value}&from_global=true"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"', 'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Service-Worker-Navigation-Preload': 'true',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': '__Secure-ext_xcid=d2680a810dcc29c25bcf3710106398ef; __Secure-ab-group=85; __Secure-user-id=0; abt_data=8324c4abcb26ea6f9be37e359966833b:2793c8b0e35611e3288e1b1cd73c39d500f488f825d55cfddf5b52a920a24ec5e02480fe92a8bf7d0c9baf89c97c49e9c7a983bcdbfe02a7d143b95266ebddfcfef1c4d66af00c0c54ad3684742053aa7101d33ae00988f844995422d69eb804d6853d3b8637f892de21d21bbf6efff9b58d8204204aa961a6ccc45ce720c9d80b68bb061489a4283548baf1dd9df0b188c40c2ff8f0f272b69c596e8790912186973dd014ae2949efe772d95663cf20546a2808c2c79ae4ccf927720e01d4cdca446c452e7d7ecf0f00675269b6c0aa; ADDRESSBOOKBAR_WEB_CLARIFICATION=1702537697; xcid=526e7fb67f3b2b3cea4f611043e95dac; cf_clearance=3vh5BNzSiIFYkY32pbcPBls8mM9Pox6.7V1.Vr1UCDI-1702626436-0-1-d18a6a2c.29072982.b9ef2846-0.2.1702626436; __Secure-access-token=3.0.p5ZOCDk6T-yFUsJLFOgwXw.85.l8cMBQAAAABleqnVCCgJJqN3ZWKgAICQoA..20231216162936.eSJk2eUTLwcRpTmQ9_vKSn8_4nMwarYHkhpK30Tmi6M; __Secure-refresh-token=3.0.p5ZOCDk6T-yFUsJLFOgwXw.85.l8cMBQAAAABleqnVCCgJJqN3ZWKgAICQoA..20231216162936.GkPXnj5CuQlkwluUnm6_-dKrqkQK9tuovfCLKs-YUtE; __cf_bm=0SBE_l5YToeInxaVEc2OERy1UnLhPOWgoXB71voilJk-1702738305-1-ASVi5dQkxmEST+qFuTKpBg7TwHpQxb4V7U8BlOnaGy9N866essablcS+DLkBpcBOz4g04UAxMX37/3y/zEVD28w=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}

        # cls.driver.get(url)

    @classmethod
    def verify(cls):
        url = "https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=/searchSuggestions/?text=&url=/search/?text={value}&from_global=true"

        for _ in range(13):
            try:
                page_text = cls.driver.page_source
                if "确认您是真人" in page_text or "检查站点连接是否安全" in page_text or "请稍候" in page_text:
                    print("点击验证")
                    cls.driver.get(url)
                    # //*[@id="challenge-stage"]/div/label/input
                    cls.driver.switch_to.frame(
                        cls.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/iframe'))
                    if _ := cls.is_find_element(by=By.XPATH, value='//*[@id="challenge-stage"]/div/label/span[2]'):
                        actions = ActionChains(cls.driver)
                        actions.move_to_element(_).click().perform()

            except Exception as e:
                pass
            finally:
                cls.driver.switch_to.default_content()
                if cls.is_find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[4]/div[2]/div/div/div[2]/span',
                                       timeout=1):
                    break

    @classmethod
    def page_loaded(cls, driver):
        return driver.execute_script('return document.readyState') == 'complete'

    @classmethod
    def save_csv(cls, data):
        # 使用 'w' 模式打开文件，并创建 CSV writer 对象
        with open("data.csv", mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    @classmethod
    def get_shop_info(cls, url):
        cls.init_driver()
        tmp_name = []
        cls.shop_name = {}
        while True:
            # cls.veify_api()
            cls.driver.get(url)
            wait = WebDriverWait(cls.driver, 10)
            wait.until(cls.page_loaded)

            scroll_script = "window.scrollTo(0, 900);"
            cls.driver.execute_script(scroll_script)

            time.sleep(1)

            # 更多
            if _ := cls.is_find_element(by=By.XPATH, value='//*[@id="seller-list"]/button'):
                cls.click(_)

            cls.verify()
            # 查看有几个
            records = cls.driver.find_elements(by=By.XPATH, value='//*[@id="seller-list"]/div/div')

            print("records:", len(records))

            if not tmp_name:
                for idx, _ in enumerate(records, 1):
                    for i in range(3):
                        value = f'//*[@id="seller-list"]/div/div[{idx}]/div/div[2]/div/div[1]/div/a'
                        if el := cls.is_find_element(by=By.XPATH, value=value, timeout=0.1):
                            _name = el.text
                            tmp_name.append(_name)
                            scroll_script = f"window.scrollTo(0, 0);"
                            cls.driver.execute_script(scroll_script)
                            break
                        else:
                            scroll_script = f"window.scrollTo(0, {900 + i * 100});"
                            cls.driver.execute_script(scroll_script)
                    else:
                        print("没找到商品")

            tmp_name = list(set(tmp_name))

            for idx, rec in enumerate(records, 1):

                # name
                value = f'//*[@id="seller-list"]/div/div[{idx}]/div/div[2]/div/div[1]/div/a'
                if _ := cls.is_find_element(by=By.XPATH, value=value):
                    name = _.text
                    print(name)
                    if not cls.shop_name.get(name):
                        new_page = f'//*[@id="seller-list"]/div/div[{idx}]/div/div[3]'
                        # new_page = '//*[@id="seller-list"]/div/div[3]/div/div[3]/div/div/div[2]'
                        cls.find_shop(url, name, new_page)
                        break
                    else:
                        logger.debug(f"{name}已找到过，不在查找")

            logger.info(cls.shop_name)
            if len(tmp_name) == len(cls.shop_name):
                break
        
        # cls.driver.close()
        return cls.shop_name


if __name__ == '__main__':
    url = "https://seller.ozon.ru/app/messenger?group=customers_v2&locale=zh-Hans"
    url = 'https://www.ozon.ru/product/kreslo-kachalka-ja012-90h90h68-sm-1323412451/'
    SpiderShop.get_shop_info(url)
