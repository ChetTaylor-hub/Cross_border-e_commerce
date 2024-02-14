import re
import time
import aircv as ac
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
from spider import SpiderShop

logger.add("log.log")


class Complaint(SpiderShop):

    @classmethod
    def input_text(cls, element, text, model=1):
        for _ in range(3):
            try:
                if model == 1:
                    element.clear()
                    element.send_keys(text)
                    break
                else:
                    actions = ActionChains(cls.driver)
                    actions.move_to_element(element).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                        Keys.CONTROL).send_keys(
                        Keys.BACKSPACE).perform()
                    actions.click(element).send_keys(text).perform()
            except Exception as e:
                try:
                    # 显式等待直到元素可见
                    actions = ActionChains(cls.driver)
                    actions.move_to_element(element).click().key_down(Keys.CONTROL).send_keys('a').key_up(
                        Keys.CONTROL).send_keys(
                        Keys.BACKSPACE).perform()
                    actions.click(element).send_keys(text).perform()
                    break
                except Exception as e:
                    time.sleep(2)

    @classmethod
    def check_is_click(cls):
        wait = WebDriverWait(cls.driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.ID, 'myButton')))

    @classmethod
    def matchimg(cls, imgsrc, imgobj, confidence=0.85):
        """
         :param imgsrc:
         :param imgobj:
         :param confidence:
         :rtype:dict
         :return:

         Args:
             imgsrc(string): 图像、素材
             imgobj(string): 需要查找的图片
             confidence: 阈值，当相识度小于该阈值的时候，就忽略掉

         Returns:
             A tuple of found [(point, score), ...]
         """

        imsrc = cv2.imdecode(np.fromfile(imgsrc, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        imobj = cv2.imdecode(np.fromfile(imgobj, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

        match_result = ac.find_template(imsrc, imobj, confidence)
        # if match_result is not None:
        #     match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 获取原始图片宽高 0为高，1为宽
        print(imgsrc, imgobj, match_result)
        return match_result


    @classmethod
    def goto_complaint_page(cls):
        if not cls.driver:
            cls.init_driver()
        cls.driver.get("https://seller.ozon.ru/app/messenger?group=customers_v2&locale=zh-Hans")

    @classmethod
    def create_application(cls):
        if el := cls.is_find_element(By.XPATH, '//*[@id="app"]/footer/div/div/div/div/div'):
            cls.click(el)
        if el := cls.is_find_element(By.XPATH, '//*[contains(text(), "创建申请")]'):
            cls.click(el)

    @classmethod
    def get_content(cls, other_code, my_code, url):
        content = f"""
我举报卖家
(卖家店铺名称)的产品 （код товара: {other_code}）
盗用我的商品（код товара: {my_code}） 。
这种行为严重损害了我的利益，希望平台予以严厉打击！
请查看所附的图片编辑器截图，
我们付出了大量的工作对产品进行俄语翻译和编辑，以达到平台的要求。
他们直接就窃取了我们的成果！请平台介入，立刻下架他们的产品！
跟卖链接{url}；"""
        return content

    @classmethod
    def _do_complaint(cls, other_code, my_code, url, file=None):
        content = cls.get_content(other_code, my_code, url)
        cls.goto_complaint_page()
        cls.create_application()

        if select_obj_el := cls.is_find_element(By.XPATH, '//*[text()="请选择主题"]'):

            cls.input_text(select_obj_el, '质量监管')
            if el := cls.is_find_element(By.XPATH, '//*[text()="质量监管"]'):
                cls.click(el)
        if el := cls.is_find_element(By.XPATH, '//*[text()="请选择子主题"]'):
            cls.input_text(el, '其他卖家违反平台规则')
            if el := cls.is_find_element(By.XPATH, '//*[text()="其他卖家违反平台规则"]'):
                cls.click(el)

        if el := cls.is_find_element(By.XPATH, '//*[@placeholder="请描述您的问题"]'):
            cls.input_text(el, content)

        if file:
            if upload_el := cls.is_find_element(By.XPATH, '//*[@type="file"]'):
                if upload_el.is_enabled():
                    upload_el.send_keys(file)

                else:
                    logger.error(r"没上传文件")
                    return
            else:
                logger.error(r"没上传文件")
                return

        if el := cls.is_find_element(By.XPATH, '//*[text()="发送"]'):
            cls.click(el)
            logger.info(f"提交成功")
        else:
            logger.error(f"提交失败")

    @classmethod
    def complaint(cls, url, file=None):
        # https://www.ozon.ru/product/kreslo-kachalka-ja012-90h90h68-sm-1323412451/
        cls.close()
        my_code = url
        if _ := re.findall(r"sm-(\d+)", url):
            my_code = _[0]
        shop_name = cls.get_shop_info(url)
        for _, (report_url, other_code) in shop_name.items():
            cls._do_complaint(other_code, my_code, report_url)


if __name__ == '__main__':
    url = 'https://www.ozon.ru/product/kreslo-kachalka-ja012-90h90h68-sm-1323412451/'
    # import pygetwindow as gw
    # name = "DeepL翻译：全世界最准确的翻译"
    # name = "请稍候…"
    # browser_windows = gw.getWindowsWithTitle(name)
    # browser_windows[0].maximize()
    # time.sleep(1)

    Complaint.complaint(url, r"")