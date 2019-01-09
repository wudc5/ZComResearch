# coding=utf-8
import requests
from selenium import webdriver
from pyvirtualdisplay import Display
import time
import random
from lxml import etree
import sys
from selenium.webdriver import FirefoxOptions
reload(sys)
sys.setdefaultencoding('utf-8')

chromePath = r'/usr/home/dechao1/spider/chromedriver.exe'

opts = FirefoxOptions()
opts.add_argument("--headless")

#wd = webdriver.Chrome(executable_path=chromePath)  # 构建浏览器
#wd = webdriver.Firefox(capabilities=capabilities)
wd = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',firefox_options=opts)

def login():
    loginUrl = 'https://www.zcom.asia/pc/index.php'
    wd.get(loginUrl)  # 进入登陆界面
    wd.find_element_by_xpath('//*[@id="mobile"]').send_keys('*******')  # 输入用户名
    wd.find_element_by_xpath('//*[@id="password"]').send_keys('******')  # 输入密码
    wd.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/a').click()  # 点击登陆
    # wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').send_keys(input("输入验证码： "))
    # wd.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/a').click()#再次点击登陆
    time.sleep(5)
    req = requests.Session()  # 构建Session
    cookies = wd.get_cookies()  # 导出cookie
    for cookie in cookies:
        req.cookies.set(cookie['name'], cookie['value'])  # 转换cookies
    content = req.get('https://www.zcom.asia/pc/questionnaire.php').content
    selector = etree.HTML(content)
    wenjuanList = selector.xpath('//a[@class="wenjuan"]')
    for wj in wenjuanList:
      try:
        name = wj.text
        link = wj.xpath('@lang')
        print "wenjuanName: ", name
        print "link: ", link[0]
        if "知识问答" in name:
            wenjuan(req, link[0])
      except:
        print "error!!!!"

def getURLContent(reque, url):
    webContent = reque.get(url).content
    return webContent

def wenjuan(req, url):

    wd.get(url)  # 进入登陆界面
    while True:
        curContent = wd.page_source
        if "问卷至此结束" in curContent:
            break
        sel = etree.HTML(curContent)
        chooseList = sel.xpath('//input[@type="radio"]')
        print "选项个数：", len(chooseList)
        if len(chooseList) != 0:
            radioLabels = wd.find_elements_by_xpath('//input[@type="radio"]')
            cNum = random.randint(0, len(radioLabels)-1)
            print "选择第 ", cNum + 1, " 项"
            radioLabels[cNum].click()  # 点击选项
            time.sleep(3)
        wd.find_element_by_xpath('/html/body/div/main/div/div/form/div[3]/button').submit()  # 点击登陆
        # cookies = wd.get_cookies()  # 导出cookie
        # for cookie in cookies:
        #     req.cookies.set(cookie['name'], cookie['value'])  # 转换cookies
        time.sleep(5)



def main():
    print "do login."
    login()
    wb.close()
    wb.quit()


if __name__ == "__main__":
    print "\n*******************************************************************"
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    print "action."
    main()
