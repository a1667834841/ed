
from select import select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import platform
class Crawler:


    def __init__(self,chromedriver_path= r'C:\Users\16678\AppData\Local\Programs\Python\Python37\chromedriver.exe'):

        if platform.system().lower() == 'windows':
            print("windows")
        elif platform.system().lower() == 'linux':
            print("linux")
            chromedriver_path = '/opt/py/chromedriver'
        # 打开浏览器
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')

        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920x1080")


        # chromedriver的绝对路径
        driver_path = chromedriver_path
       

        # 初始化一个driver，并且指定chromedriver的路径
        self.driver = webdriver.Chrome(executable_path=driver_path,
                                chrome_options=chrome_options)
        #将浏览器最大化显示
        self.driver.maximize_window() 
    
    def get_driver(self):
        return self.driver


class Question_Bank:
    question = ""
    answers = []

    def print(self):
        "打印对象的所有属性"
        print(self.__dict__)

