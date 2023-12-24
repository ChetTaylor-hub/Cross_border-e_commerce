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

from loguru import logger
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

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
        options.add_argument(
            "--user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'")

        if need:
            cls.driver = webdriver.Chrome(service=service, options=options)
        else:
            os.system(r'start chrome --remote-debugging-port=9526')
            options.add_experimental_option("debuggerAddress", "127.0.0.1:9526")
            options.add_argument('--incognito')
            cls.driver = webdriver.Chrome(service=service, options=options)

    @classmethod
    def init_driver(cls):
        cls.need_driver(False)
        cls.driver.maximize_window()
        # cls.driver.implicitly_wait(10)


    @classmethod
    def is_find_element(cls, by=None, value=None, timeout: Union[int, float] = 0.5):
        for _ in range(20):
            try:
                el = cls.driver.find_element(by=by, value=value)
                if el.is_displayed():
                    return el
                time.sleep(0.2)
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
    def find_shop(cls, name, shop_el):
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
                print("向下滑动2")
                scroll_script = f"window.scrollTo(0, {1000 + i * 300});"
                cls.driver.execute_script(scroll_script)
        else:
            logger.debug(f"{name}没找到")

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
        while True:

            cls.driver.get(url)
            wait = WebDriverWait(cls.driver, 10)
            wait.until(cls.page_loaded)

            scroll_script = "window.scrollTo(0, 900);"
            cls.driver.execute_script(scroll_script)

            # 更多
            if _ := cls.is_find_element(by=By.XPATH, value='//*[@id="seller-list"]/button'):
                _.click()
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
                        cls.find_shop(name, new_page)
                        break
                    else:
                        logger.debug(f"{name}已找到过，不在查找")

            logger.info(cls.shop_name)
            if len(tmp_name) == len(cls.shop_name):
                break
            
    def 

if __name__ == '__main__':
    url = "https://www.ozon.ru/product/1353884336/"
    SpiderShop.get_shop_info(url)
