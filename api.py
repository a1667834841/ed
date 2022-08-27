from time import sleep
from selenium.webdriver.common.by import By
import io
from PIL import Image

import ocr_api


def addAttribute(driver, elementobj, attributeName, value):
    '''
    封装向页面标签添加新属性的方法
    调用JS给页面标签添加新属性，arguments[0]~arguments[2]分别
    会用后面的element，attributeName和value参数进行替换
    添加新属性的JS代码语法为：element.attributeName=value
    比如input.name='test'
    '''
    driver.execute_script("arguments[0].%s=arguments[1]" % attributeName, elementobj, value)


def setAttribute(driver, elementobj, attributeName, value):
    '''
    封装设置页面对象的属性值的方法
    调用JS代码修改页面元素的属性值，arguments[0]~arguments[1]分别
    会用后面的element，attributeName和value参数进行替换
    '''
    driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", elementobj, attributeName, value)


def getAttribute(elementobj, attributeName):
    # 封装获取页面对象的属性值方法
    return elementobj.get_attribute(attributeName)


def removeAttribute(driver, elementobj, attributeName):
    '''
    封装删除页面属性的方法
    调用JS代码删除页面元素的指定的属性，arguments[0]~arguments[1]分别
    会用后面的element，attributeName参数进行替换
    '''
    driver.execute_script("arguments[0].removeAttribute(arguments[1])",
                          elementobj, attributeName)

def get_captcha_head_less(driver,captcha_path = 'img/captcha.png'):

    # 截取全屏的关键 设置最大窗口
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    # print(width,height)
    #将浏览器的宽高设置成刚刚获取的宽高
    driver.set_window_size(width, height)
    sleep(1)
    # 截图 body 大图
    driver.save_screenshot('img/full_page.png')
    # 定位验证码所在的位置
    CodeImage = driver.find_element(By.CLASS_NAME, 'code')
    # print(CodeImage.location)  # {'x': 564, 'y': 310}
    # print(CodeImage.size)  # {'height': 30, 'width': 119}
    left = CodeImage.location['x']
    top = CodeImage.location['y']
    right = CodeImage.size['width'] + left
    height = CodeImage.size['height'] + top
    temporary_img = Image.open('img/full_page.png')
    temporary_img = temporary_img.crop((left, top, right, height))
    temporary_img.save(captcha_path)

def get_captcha_head(driver,captcha_path = 'img/captcha.png'):
    captcha = driver.find_element(By.CLASS_NAME, 'code')
    captcha.screenshot(captcha_path)

def ocr_captcha(cap_path):
    cap_img = Image.open(cap_path,mode='r')
    imgByteArr = io.BytesIO()
    cap_img.save(imgByteArr, format='PNG')
    cap_img_bytes = imgByteArr.getvalue()
    cap_number = ocr_api.ocr_captcha(cap_img_bytes)
    print(cap_number)
    return cap_number


'''
获取cookie
'''
def get_cookies_dict(driver):
    c = driver.get_cookies()
    # print(c)
    cookies = {}
    # 获取cookie中的name和value,转化成requests可以使用的形式
    for cookie in c:
        cookies[cookie['name']] = cookie['value']
    # print(cookies)
    return cookies

def get_cookies_list(driver):
    return driver.get_cookies()

'''
get headers
'''
def get_headers(driver):
    headers = {}
    for request in driver.requests:
        print(request.url) # <--------------- Request url
        print(request.headers) # <----------- Request headers
        headers[headers['name']] = headers['value']
        # print(request.response.headers) # <-- Response headers
    
    return headers

