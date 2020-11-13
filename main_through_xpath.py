from bs4 import BeautifulSoup
import requests
import re
from lxml import etree
import time
from selenium import webdriver
from tkinter import messagebox
import datetime
from PIL import Image
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

username='XXXXXXXXXX' # Your Student Number
password='000' # Initial Password


is_login=0
url = 'http://10.203.97.155/book/notice/act_id/XXXX/type/4/lib/11'  # 以基础图书馆为例

# 伪装请求UA
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}

def appoint(username,password):

    pass

def re_request():
    global req,html,soup,element,appointed_xpath,url
    req = requests.get(url,headers=headers)
    req.close()
    req.encoding = 'utf-8'
    html = req.text
    soup = BeautifulSoup(html, features="html.parser")
    element = etree.HTML(str(soup))
    appointed_xpath = element.xpath('/html/body/div[4]/div[1]/div[2]/div[2]')



req = requests.get(url,headers=headers)
req.close()
if req.status_code!=requests.codes.ok:
    print('Status Code Error')
req.encoding = 'utf-8'
html = req.text
soup = BeautifulSoup(html,features="html.parser")
# print(str(soup))
element=etree.HTML(str(soup))
# res=etree.tostring(element)
# print(res.decode('utf-8'))
appointed_xpath=element.xpath('/html/body/div[4]/div[1]/div[2]/div[2]')  # 预约人数的xpath地址
# for tr in appointed_xpath:
#     print(etree.tostring(tr,encoding='utf-8').decode("utf-8"))
appointed_xpath_str=etree.tostring(appointed_xpath[0],encoding='utf-8').decode("utf-8")
print(re.findall(r"\[[^\[\]]+\]",appointed_xpath_str)[0])
available_number=int(re.findall(r"\d+",appointed_xpath_str)[1])-int(re.findall(r"\d+",appointed_xpath_str)[0])
print(available_number)


# if available_number >= 1:
#     # username=input('Input your username:')
#     # password = input('Input your password:')
#     username='3190105838'
#     password='000'
#     appoint(username,password)

# while 1:
#     print(appointed_xpath_str[-15:-8])
#     available_number = int(appointed_xpath_str[-11:-8]) - int(appointed_xpath_str[-15:-12])
#     print(available_number)
#     time.sleep(1)


opt = webdriver.ChromeOptions()                 #创建浏览器
# opt.set_headless()                            #无窗口模式
driver = webdriver.Chrome(options=opt)          #创建浏览器对象
# driver.get("https://www.baidu.com")   #打开网页
driver.get(url)
# driver.maximize_window()                      #最大化窗口

# 报错 Message: javascript error: Failed to execute 'elementsFromPoint' on 'Document': The provided double value is non-finite.
# fnd_element = driver.find_element(by='xpath',value='/html/body/div[4]/div[1]/div[3]')
# ActionChains(driver).move_to_element(fnd_element).perform()

# 报错 Message: element not interactable
# driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[3]").send_keys(Keys.ENTER)

# 再尝试，这回终于OK
login_button = driver.find_element(by='xpath',value='/html/body/div[2]/div[1]/ul/li[3]/a')
driver.execute_script("arguments[0].click();",login_button)
driver.find_element_by_xpath("/html/body/div[9]/div/table/tbody/tr[2]/td/div/div/div[1]/input").send_keys(username)
driver.find_element_by_xpath("/html/body/div[9]/div/table/tbody/tr[2]/td/div/div/div[2]/input").send_keys(password)
# code_href=driver.find_element_by_xpath('/html/body/div[2]/div[1]/ul/li[3]')  # 找到验证码对应的xpath,并检测是否已经登录
code_href=driver.find_element_by_xpath('/html/body/div[2]/div[1]/ul/li[2]') # logout_control
print(code_href.get_attribute("style"))

time.sleep(6)
is_login=1
# while 1:
#     code_href = driver.find_element_by_class_name('logout-control')
#     if code_href.get_attribute("style")!= "display: none;":
#         is_login=1
#         print('this is ok')
#         break

# time.sleep(10)
# is_login=1


# 登录完成
while 1:
    try:
        req = requests.get(url,headers=headers)
        time.sleep(0.1)
        req.close()
        req.encoding = 'utf-8'
        html = req.text
        soup = BeautifulSoup(html, features="html.parser")
        element = etree.HTML(str(soup))
        appointed_xpath = element.xpath('/html/body/div[4]/div[1]/div[2]/div[2]')
        # print(len(appointed_xpath))
        while len(appointed_xpath) == 0:
            print("oops! You need 2 refresh!")
            re_request()
        appointed_xpath_str = etree.tostring(appointed_xpath[0], encoding='utf-8').decode("utf-8")
        # 更新available_number
        try:
            available_number = int(re.findall(r"\d+", appointed_xpath_str)[1]) - int(re.findall(r"\d+", appointed_xpath_str)[0])
        except:
            continue
        # print(available_number)
        print(available_number, re.findall(r"\d+", appointed_xpath_str)[0], re.findall(r"\d+", appointed_xpath_str)[1])
        print(str(datetime.datetime.now())[:-7])
        # time.sleep(0.4)
        if is_login==1 and available_number >= 1 :
            while driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/button[3]').get_attribute("style")!="margin-top: 20px; padding-left: 40px; padding-right: 40px;":
                driver.refresh()
                time.sleep(0.5)
                try:
                    iwanna_label=driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/button[1]')
                except:
                    continue
                if iwanna_label.get_attribute("style")=="margin-top: 20px; padding-left: 40px; padding-right: 40px;":
                    try:
                        appoint_button = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/button[1]')
                        driver.execute_script("arguments[0].click();", appoint_button) # 点击“我要预约”按钮
                        final_button=driver.find_element_by_xpath('/html/body/div[9]/div/table/tbody/tr[3]/td/div[2]/button[2]')
                    except:
                        continue
                    driver.execute_script("arguments[0].click();", final_button)  # 点击“确定”按钮
                    driver.refresh()

            if (driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/button[3]').get_attribute("style")=="margin-top: 20px; padding-left: 40px; padding-right: 40px;"
                    or driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/button[2]').get_attribute("style")=="margin-top:20px; padding-left:40px; padding-right:40px;"):
                messagebox.showinfo("提示", "预约成功\n"+str(datetime.datetime.now())[:-7])
                print("OK!")
                driver.quit()
    except:
        continue
