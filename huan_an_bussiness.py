from typing import List
from selenium.webdriver.common.by import By
from time import sleep
from api import *
from crawler import Crawler
import json
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import comLogger
import traceback
from selenium.webdriver.common.keys import Keys



logger = comLogger.get_logger()




def project_root_path(project_name=None, print_log=True):
    """
    获取当前项目根路径
    :param project_name: 项目名称
                            1、可在调用时指定
                            2、[推荐]也可在此方法中直接指定 将'XmindUitl-master'替换为当前项目名称即可（调用时即可直接调用 不用给参数）
    :param print_log: 是否打印日志信息
    :return: 指定项目的根路径
    """
    p_name = 'XmindUitl-master' if project_name is None else project_name
    project_path = os.path.abspath(os.path.dirname(__file__))
    # Windows
    if project_path.find('\\') != -1: separator = '\\'
    # Mac、Linux、Unix
    if project_path.find('/') != -1: separator = '/'

    root_path = project_path[:project_path.find(f'{p_name}{separator}') + len(f'{p_name}{separator}')]
    # if print_log: print(f'当前项目名称：{p_name}\r\n当前项目根路径：{root_path}')
    return root_path

number_key = {
    '0': Keys.NUMPAD0,
    '1': Keys.NUMPAD1,
    '2': Keys.NUMPAD2,
    '3': Keys.NUMPAD3,
    '4': Keys.NUMPAD4,
    '5': Keys.NUMPAD5,
    '6': Keys.NUMPAD6,
    '7': Keys.NUMPAD7,
    '8': Keys.NUMPAD8,
    '9': Keys.NUMPAD9
}


def getNumberKey(number):
    """
    将season映射为字符串
    :param season:
    :return:
    """
    return number_key[number]


'''
登录获取cookies
'''
def login(user_name="32030519841022041x",password="22041x",login_url="https://jshazj.59iedu.com/index",driver=None):
   

    # 请求网页
    while(True):
        try:
            logger.info("请求网址: %s",login_url)
            driver.get(login_url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'identify'))
            )

            # 获取输入框
            driver.find_element(By.NAME, 'identify').send_keys(user_name)
            driver.find_element(By.NAME, 'passWord').send_keys(password)
            picValidateCode = driver.find_element(By.NAME, 'picValidateCode')
            picValidateCode.click()
            sleep(1)
            logger.info("输入账号 %s 密码:*******完成",user_name)
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
            continue
        break


    # 无头模式获取验证码
    get_captcha_head_less(driver)
    # get_captcha_head(driver)

    # 读取验证码图片，并识别
    cap_number = ocr_captcha('img/captcha.png')

    count = 0
    while(True):
        picValidateCode.clear()
        # 赋值 picValidateCode
        for n in cap_number:
            print(n)
            number_key = getNumberKey(n)
            picValidateCode.send_keys(number_key)
        sleep(1)
        picValidateCode.click()
        login_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div/div/div/form/ul/li[4]/button')
        login_button_class = login_button.get_attribute('class')
        print("login_button_class:",login_button_class)
        if 'disabled' in login_button_class:
            sleep(0.2)
            continue
        elif count > 10:
            break
        else:
            break
        count = count+1

    logger.info("获取验证码：%s",cap_number)
    # 点击登录
    picValidateCode.send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[1]/div/div/div/form/ul/li[4]/button').click()
    # 获取cookie
    cookies = get_cookies_dict(driver)
    # logger.info("cookies: %s",cookies)

    WebDriverWait(driver, 30).until(
         EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[2]/div/div[1]/div[1]/div/div/ul/li[1]/a/span'))
    )

    driver.save_screenshot('img/index.png')
    return cookies
        


def choose_course(my_course_url = "https://jshazj.59iedu.com/center/myStudy/goods/detail?year=2020",driver=None):
    count = 0

    try:
        logger.info("my_course_url:%s",my_course_url)
        driver.get(my_course_url)
        sleep(6)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"div.tit-2 a"))
        )
        
        test_button = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div[4]/div[3]/table/tbody/tr/td[1]/div[2]/div[1]/a") #课后测验
        test_button.click()
        find_success = False
        sleep(5)
        while(True):
            handle = driver.window_handles[count%len(driver.window_handles)]
            count = count+1
            # 切换到新的页面
            driver.switch_to.window(handle)

            # print(driver.current_url)
            # 跳转到考试页面
            if "exam/#/fighting" in driver.current_url:
                logger.info("进入考试页面")
                find_success = True
                break
            if  "home/home/detail" in driver.current_url:
                driver.find_elements(By.CSS_SELECTOR,".course-text-btn")[2].click()
                sleep(4)
                for handle in driver.window_handles:
                    driver.switch_to.window(handle)
                    if "exam/#/fighting" in driver.current_url:
                        logger.info("进入考试页面")
                        find_success = True
                        break
                # driver.switch_to_window(driver.window_handles[1])
            # if count > 3:
            #     break
            # if len(driver.window_handles) > 3:
            #     driver.switch_to.window(driver.window_handles[0])
            #     driver.close()
            if find_success:
                break
            
        # pageSource = driver.page_source
        
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
    logger.info("driver.current_url:%s",driver.current_url)
    return driver.current_url


def answer_exam(driver=None):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME,"exam-tit"))
    )
    exams = driver.find_elements(By.CLASS_NAME,"exam-tit")
    answer_options = driver.find_elements(By.CLASS_NAME,"answer")
    logger.info("题目数量：%s",len(exams))
    for index in range(len(exams)):
        exam = exams[index]
        answer_option = answer_options[index]
        # 定位题目
        # print(exam.text)
        # 查找答案
        answers = check_answer(exam.text)
        # 选择答案 并点击
        options = answer_option.find_elements(By.CLASS_NAME,"ans-b-1")
        for answer in answers:
            sleep(0.2)
            options[int(answer)].find_element(By.TAG_NAME,"input").click()
        
    
    # print(driver.page_source)
    sleep(3)
    # driver.execute_script("document.body.style.zoom='0.5'")
    driver.save_screenshot('img/test.png')
    # 提交测验
    a_links = driver.find_elements(By.CSS_SELECTOR,".exam-q-num a")
    # for a in a_links:
    #     print(a.is_displayed(),":",a.location["x"],",",a.location["y"])
    #     # a.click()
    #     ActionChains(driver).move_to_element(a).move_by_offset(5,5).click().perform()
        
    # submit_button = driver.find_elements(By.CSS_SELECTOR,".ico")
    # print("Element is visible before? " + str(submit_button.is_displayed()))

    driver.execute_script("arguments[0].click();",a_links[0])
    # sleep(0.5)
    # print("Element is visible after? " + str(submit_button.is_displayed()))
    # # submit_button = driver.find_element(By.CLASS_NAME,"ico-submit")
    # submit_button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"span .ico ico-submit")))

    # submit_button.click()
    btn_center = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"btn-center"))
        )
    # btn_center = driver.find_element(By.CLASS_NAME,"btn-center")
    btn_buttons = btn_center.find_elements(By.TAG_NAME,"button")
    sleep(0.5)
    btn_buttons[0].click()
    sleep(1)

def record_answer(driver=None):
    answer_bank_list = []
    sleep(1)
    exams = driver.find_elements(By.CLASS_NAME,"exam-tit")
    answer_str_list = driver.find_elements(By.CLASS_NAME,"a-r")
    for index in range(len(exams)):
        exam = exams[index]
        answer_str = answer_str_list[index].text

        ques = {}
        ques["question"] = exam.text
        if is_all_chinese(answer_str):
            if answer_str == "正确":
                ques["answers"] = ["0"]
            else:
                ques["answers"] = ["1"]
        else:
            answers = []
            for index in range(len(answer_str)):
                a_str = answer_str[index]
                # print(a_str,":",ord(a_str))
                answers.append(str(ord(a_str) - 65))
                ques["answers"] = answers
        answer_bank_list.append(ques)

    # print(answer_bank_list)
    root_path = project_root_path()

    reset_file(root_path+'/resoures/question_bank.json',answer_bank_list)
    driver.close()
    handle = driver.window_handles[len(driver.window_handles)-1]
    # 切换到新的页面
    driver.switch_to.window(handle)


def reset_file(path,data_list):
    
    res = read_file(path)
    for data in data_list:
        res.append(data)
    # 去重
    new_res = delRepeat(res,"question")
    write_file(path,json.dumps(new_res,ensure_ascii=False))


'''
按照key 去重
'''
def delRepeat(data,key):
    new_data = [] # 用于存储去重后的list
    values = []   # 用于存储当前已有的值
    for d in data:
        if d[key] not in values:
            new_data.append(d)
            values.append(d[key])
    return new_data


def read_file(path) -> list:
    with open(path,'r',encoding='utf-8') as file_object:
        res = file_object.read()
    if res == "":
        res = "[]"
    json_data = json.loads(res)
    return json_data

def write_file(path,content):
    with open(path,'w',encoding='utf-8') as file_object:
        file_object.write(content)
        file_object.flush()





def check_answer(ques) -> List[int]:
    root_path = project_root_path()
    banks = read_file(root_path+'/resoures/question_bank.json')
    for bank in banks:
        if bank["question"] == ques:
            return bank["answers"]
    
    return ["0"]

def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def exam(user_name="32030519841022041x",password="22041x",login_url="https://jshazj.59iedu.com/index",years=[]):

    course_url = "https://jshazj.59iedu.com/center/myStudy/goods/detail?year="
    try:
        crawl = Crawler()
        driver = crawl.get_driver()

        cookies = login(user_name,password,login_url,driver)
        for year in years:
            try:
                choose_course(course_url+str(year),driver)
                answer_exam(driver)
                record_answer(driver)
                logger.info("%s 结束",str(year))
            except Exception as e:
                # logger.error(e)
                traceback.print_exc()
                info = traceback.format_exc()
                logger.error("err:%s",info)
                continue
    finally:
        driver.quit()





if __name__ == '__main__':
    while(True):
        exam(user_name='320802198107102013',password= '102013', years=["2019"])

        # driver.quit()
        # for i in range(1,10):
        #     try:
        #         crawl = Crawler()
        #         driver = crawl.driver

        #         cookies = login()
        #         choose_course()
        #         answer_exam()
        #         record_answer()
        #     finally:
        #         driver.quit()
    
    
    # print(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))) 
    
    # print(os.path.abspath(os.path.dirname(os.getcwd()))) 
    
    # print(os.path.abspath(os.path.join(os.getcwd(), ".."))) 

    # root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))



    # # write_file(root_path+'/resoures/question_bank.json',"sss")
    # res = read_file(root_path+'/resoures/question_bank.json')
    # print(res)
    # driver.quit()

