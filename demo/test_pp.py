'''
Created on 2020年6月10日

@author: qguan
'''
# coding=utf-8

import time
import os
from PIL import Image
import pytesseract
from selenium import webdriver

pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-infobars') # 这类方法估计对版本V78以下有效
# chrome版本 V78，以上有效
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ['enable-automation'])


# 创建浏览器操作对象
driver = webdriver.Chrome(options=options)
# 进入该网站
driver.get("http://test.hcp-grand-backend.ieltsbro.com/login")
driver.implicitly_wait(20)  # 隐式等待
driver.maximize_window()  # 窗口最大化

# 找到img标签元素，提取标签属性，得到图形验证码地址
image_url = driver.find_element_by_xpath('//div/img').get_attribute('src')

os.system(r"curl -o image.png {}".format(image_url))

image = Image.open('image.png')

text = pytesseract.image_to_string(image)
print(text)
driver.find_element_by_xpath(
    "//input[@placeholder='请输入用户名']").send_keys('13266515340')
driver.find_element_by_xpath(
    "//input[@placeholder='请输入密码']").send_keys('A1234!')
driver.find_element_by_xpath("//input[@placeholder='请输入验证码']").send_keys(text)
# driver.find_element_by_xpath("//button[@type='button']").click()

# time.sleep(3)

driver.quit()
