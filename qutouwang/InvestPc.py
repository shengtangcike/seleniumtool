#coding=utf-8
import random
import time,datetime
from selenium import webdriver
from libs.op_keyboard import op_keyboard
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from libs.DealResource import *
from libs.MysqlDB import *
from libs.tool import *
from libs.createIdcard import *

url_login = read_resource("${urlpath}")+"/user/login"
op = op_keyboard()
class InvestPc():
    '''去投网前台的相关操作'''
    def __init__(self):
        os.system("taskkill /f /t /im 360chrome.exe") #初始化关闭360极速浏览器
        os.system("taskkill /f /t /im chromedriver.exe") #初始化关闭360极速浏览器
        # self.driver = webdriver.Chrome()
        #使用360极速浏览器（chrome内核）
        __browser_url = read_resource("${__browser_url}")
        chrome_options = Options()
        chrome_options.binary_location = __browser_url
        #保留浏览器默认配置，第一次安装浏览器的缓存位置
        chrome_options.add_argument(r"user-data-dir=%s"%read_resource("${add_argument}"))

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.implicitly_wait(20)
        self.driver.get(url_login)
        self.driver.maximize_window()

    def investlogin(self, username, password):
        self.driver.find_element_by_id("account").clear()  #录用户名清除
        self.driver.find_element_by_id("password").clear()  #登录密码清除
        self.driver.find_element_by_id("account").send_keys(username)  #输入登录用户名
        self.driver.find_element_by_id("password").send_keys(password)  #输入登录密码
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div/div[3]/div/div/div[1]/form/div[3]/div/div/span/button').click() #点击登录
        time.sleep(2)                     #//*[@id="root"]/section/div[1]/div/div[3]/div/div/div[1]/form/div[3]/div/div/span/button

    def recharge(self,amount=100):
        '''充值流程'''
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div[2]/div/div[2]/ul/li[6]/a/span').click() #点击我的账户
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div[1]/div/div/div/div/a[2]').click() #点击充值
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="amount"]').send_keys(amount)  # 输入金额
        time.sleep(2) #等待页面js
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/div/div[3]/div[1]/div[3]/div[3]/div[1]/div[2]/dl/dd/form/div[2]/div/div/span/button').click()  # 输入金额
        time.sleep(8)
        # 方法1：使用tab键定位元素，效果不佳，通过一两次，但成功率太低
        # 方法2：使用桌面分辨率定位，所以其他人使用时，电脑的分辨率要统一
        #廊坊银行的充值页面使用360极速浏览器，使用selenium拿不到内容，不知道因为什么，但谷歌能拿到
        op.click(850,580)  #发送验证码位置
        time.sleep(2)
        op.click(680, 580)  # 验证码输入框
        for i in '123456':
            op.dd(i)
        op.click(680, 645)  # 安全密码输入框
        for i in '123456':
            op.dd(i)
        op.click(745, 750)  # 确认
        #****断言写在此处****
        contents = self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/strong').text
        print(contents)
        if "充值成功" not in contents:
            raise Exception("充值失败")

    def withdraw(self,amount=100):
        '''提现流程'''
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div[2]/div/div[2]/ul/li[6]/a/span').click() #点击我的账户
        time.sleep(2)                     #//*[@id="root"]/section/div[1]/div[2]/div/div[2]/ul/li[6]/a/span
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[1]/div[2]/dl[2]/dd/p[3]/a').click() #点击提现
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="amount"]').send_keys(amount)  # 输入金额
        time.sleep(2) #等待页面js
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/div/div[3]/div[1]/div[2]/div[3]/div/div[2]/div[2]/form/div[2]/div/div/span/button').click()  # 输入金额
        time.sleep(8)
        op.click(860, 615)  # 发送验证码位置
        time.sleep(2)
        op.click(680, 615)  # 验证码输入框
        for i in '123456':
            op.dd(i)
        op.click(700, 680)  # 安全密码输入框
        for i in '123456':
            op.dd(i)
        op.click(745, 780)  # 确认
        #断言写在此处
        time.sleep(10)
        contents = self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/strong').text
        print(contents)
        if "提现成功" not in contents:
            raise Exception("提现失败")

    def forgetPwd(self):
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div/div[3]/div/div/div[1]/form/div[3]/div/div/span/a').click()  # 点击忘记密码
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="mobile"]').send_keys(read_resource("${thelenderphone}"))  # 输入手机号
        #====================
        #可以实现鼠标拖动，但效果不佳
        source = self.driver.find_element_by_xpath('//*[@id="ResetBlockUnlockSlider"]')
        ac = ActionChains(self.driver)
        ac.click_and_hold(source)
        for i in range(50):
            ac.move_by_offset(6.18,0).perform()
            text = self.driver.find_element_by_xpath('//*[@id="ResetBlockUnlockSlider"]').get_attribute("style")
            print(text)
        time.sleep(2)
        ac.release().perform()
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div/div[2]/div/div/form/div[2]/div[2]/div/div/span/button').click()  # 下一步
        #====================

    def signing(self):
        '''签约'''
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div[2]/div/div[2]/ul/li[6]/a/span').click()       #点击我的账户
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[1]/div[2]/dl[3]/dd/p[1]/a').click()   #点击我的借款
        time.sleep(1)
        userid = read_resource("${theborroweridcard}")
        db = MysqlDB()
        sqnum = db.select_return_A_data("SELECT COUNT(1) FROM qtw_loan_db.p2p_core_loan_debt_info debt LEFT JOIN qtw_loan_db.p2p_loan_return_main_info main ON main.loan_no = debt.debtcode WHERE 1=1 AND main.loan_status IS NULL AND debt.idcard = '%s';" % userid)[0]
        print("申请中借款个数%s"%sqnum)
        #点击最后页
        if int(sqnum) > 7:
            self.driver.find_element_by_css_selector("ul[unselectable='unselectable']>li:nth-last-child(2)>a").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("tr:nth-last-child(1) > td:nth-child(8) > a").click()                  #点击签约
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="qtw"]/div[3]/div/div[2]/div/div[2]/div[1]/div/p[7]/label/span[1]/input').click()#勾选
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="qtw"]/div[3]/div/div[2]/div/div[2]/div[2]/button').click()          #点击立即签约
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="qtw"]/div[4]/div/div[2]/div/div[2]/div/div/div[2]/button').click()  #立即签约-确定
        time.sleep(1)
        print("签约成功")

    def invest(self):
        '''出借'''
        bdname = read_resource("${bdname}")  # 读取标的名称
        #散标列表
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div[2]/div/div[2]/ul/li[2]/a/span').click()   #点击我要出借
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div[1]/ul/li[1]/a').click()         #点击散标列表
        time.sleep(2)
        db = MysqlDB()
        count = db.select_return_A_data("SELECT COUNT(1) FROM p2p_pact_issue t WHERE t.`bid_state` NOT IN  ('3','6','4','7','2')  AND t.`issue_test_flag`='0' AND t.tend_dead_li>=NOW()")[0]
        #点击分页控件
        num = count//7+3
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div[2]/div[3]/div[2]/div/ul/li[%s]' %num).click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[text()='%s']/parent::p/parent::div"%bdname).click()   #查询标的名称，并点击标的
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div/form/div[1]/div/div/span/div[2]/span').click()  # 点击全投
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div/form/div[3]/button').click()          #点击立即出借
        time.sleep(2)
        #标的详情页面
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div/div/p/label[1]/span/input').click()  # 勾选协议
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div/div/div[4]/button').click()  # 确认出借
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="qtw"]/div[4]/div/div[2]/div/div[2]/div/div/div[2]/button').click()  # 确认阅读协议
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div/div/div[4]/button').click()  # 确认出借
        time.sleep(2)
        print("全部投满")

    def repayment(self,num,amount = None):
        '''借款系统还款'''
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div[2]/div/div[2]/ul/li[6]/a/span').click()       #点击我的账户
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[1]/div[2]/dl[3]/dd/p[1]/a').click()  # 点击我的借款
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/div[2]').click()  # 点击借款记录
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div/div/div/div/div/div/div/table/tbody/tr/td[9]/a').click()  # 点击第一个散标的详情
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div[4]/div/div/div/div/div/div/table/tbody/tr[%s]/td[7]/a'%num).click()  # 点击还款
        time.sleep(2)
        if amount != None:
            self.driver.find_element_by_xpath('//*[@id="multiReturnSum"]').clear()  # 部分还款金额
            self.driver.find_element_by_xpath('//*[@id="multiReturnSum"]').send_keys(amount)  # 部分还款金额
            time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="qtw"]/div[3]/div/div[2]/div/div[2]/div[1]/div/form/div[2]/button').click()  # 还款确认
        time.sleep(5)
        res = self.driver.find_element_by_xpath('//*[@id="qtw"]/div[5]/div/div[2]/div/div[2]/div/div/div[1]/div/div/p[2]/span').text  #还款结果
        print(res)
        self.driver.find_element_by_xpath('//*[@id="qtw"]/div[5]/div/div[2]/div/div[2]/button/span').click()  # 关闭弹框
        time.sleep(2)
    def earlyRepaymentOperation(self):
        '''全部提前结清'''
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div[2]/div/div[2]/ul/li[6]/a/span').click()       #点击我的账户
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[1]/div[2]/dl[3]/dd/p[1]/a').click()  # 点击我的借款
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/div[2]').click()  # 点击借款记录
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/div/div[3]/div[2]/div[2]/div/div/div/div/div/div/div/table/tbody/tr/td[9]/a').click()  # 点击第一个散标的详情
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div[3]/div[2]/div[5]/button').click()  # 点击全部提前结清
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="qtw"]/div[3]/div/div[2]/div/div[2]/div[1]/div/p[6]/button').click()  # 点击全部提前结清确认
        time.sleep(2)
    def changedebtplan(self):
        '''
        :param bidNocore: 标的编号
        :return: 更改放款时间和回款计划表
        '''
        debtCode = read_resource("${entry_code}")
        db = MysqlDB()
        bidNocore = db.select_return_A_data("SELECT pactissue_no FROM p2p_pact_issue  WHERE credit_id = '%s';" % debtCode)[0]
        #更改已满标的的放款时间，放款时间向前提前3个月2018-09-01
        now_year = datetime.datetime.now().year
        now_month = datetime.datetime.now().month
        if now_month - 3 <= 0:
            month = str(12 + now_month - 3)
            if len(month) == 1:
                month = "0"+ month
            date0 = str(now_year-1)+"-"+month+"-"+"01"
        else:
            month = str(now_month-3)
            if len(month) == 1:
                month = "0"+ month
            date0 = str(now_year) + "-" + month + "-" + "01"

        if now_month - 2 <= 0:
            month = str(12 + now_month - 2)
            if len(month) == 1:
                month = "0"+ month
            date1 = str(now_year-1)+"-"+month+"-"+"01"
        else:
            month = str(now_month - 2)
            if len(month) == 1:
                month = "0"+ month
            date1 = str(now_year) + "-" + month + "-" + "01"

        if now_month - 1 <= 0:
            month = str(12 + now_month - 1)
            if len(month) == 1:
                month = "0"+ month
            date2 = str(now_year-1)+"-"+month+"-"+"01"
        else:
            month = str(now_month - 1)
            if len(month) == 1:
                month = "0"+ month
            date2 = str(now_year) + "-" + month + "-" + "01"
        if len(str(now_month)) == 1:
            month = "0" + str(now_month)
        else:
            month = str(now_month)
        date3 = str(now_year) + "-" + month + "-" + "01"
        #==============================
        if now_month + 1 > 12:
            month = str(now_month + 1 - 12)
            if len(month) == 1:
                month = "0"+ month
            date4 = str(now_year+1)+"-"+month+"-"+"01"
        else:
            month = str(now_month + 1)
            if len(month) == 1:
                month = "0"+ month
            date4 = str(now_year) + "-" + month + "-" + "01"

        if now_month + 2 > 12:
            month = str(now_month + 2 - 12)
            if len(month) == 1:
                month = "0"+ month
            date5 = str(now_year+1)+"-"+month+"-"+"01"
        else:
            month = str(now_month + 2)
            if len(month) == 1:
                month = "0"+ month
            date5 = str(now_year) + "-" + month + "-" + "01"
        if now_month + 3 > 12:
            month = str(now_month + 3 - 12)
            if len(month) == 1:
                month = "0"+ month
            date6 = str(now_year+1)+"-"+month+"-"+"01"
        else:
            month = str(now_month + 3)
            if len(month) == 1:
                month = "0"+ month
            date6 = str(now_year) + "-" + month + "-" + "01"
        #更改放款时间
        db = MysqlDB()
        db.sql_update('UPDATE qtw_invest_db.p2p_pact_issue SET fk_time = "%s" where pactissue_no = "%s"' % (date0,bidNocore))
        #更改还款计划
        db = MysqlDB()
        db.sql_update('UPDATE qtw_invest_db.p2p_invest_return_plan SET open_date = "%s" where pactissue_no = "%s" AND term_num = 1' % (date1,bidNocore))
        db = MysqlDB()
        db.sql_update('UPDATE qtw_invest_db.p2p_invest_return_plan SET open_date = "%s" where pactissue_no = "%s" AND term_num = 2' % (date2,bidNocore))
        db = MysqlDB()
        db.sql_update('UPDATE qtw_invest_db.p2p_invest_return_plan SET open_date = "%s" where pactissue_no = "%s" AND term_num = 3' % (date3,bidNocore))
        db = MysqlDB()
        db.sql_update('UPDATE qtw_invest_db.p2p_invest_return_plan SET open_date = "%s" where pactissue_no = "%s" AND term_num = 4' % (date4,bidNocore))
        db = MysqlDB()
        db.sql_update('UPDATE qtw_invest_db.p2p_invest_return_plan SET open_date = "%s" where pactissue_no = "%s" AND term_num = 5' % (date5,bidNocore))
        db = MysqlDB()
        db.sql_update('UPDATE qtw_invest_db.p2p_invest_return_plan SET open_date = "%s" where pactissue_no = "%s" AND term_num = 6' % (date6,bidNocore))
        time.sleep(5)

    def investTranferDebtConfirm(self):
        '''申请变现'''
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div[2]/div/div[2]/ul/li[6]/a/span').click()       #点击我的账户
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[1]/div[2]/dl[3]/dd/p[3]/a').click()  # 点击我的散标
        time.sleep(2)                     #//*[@id="root"]/section/div[2]/div/div/div[1]/div[2]/dl[3]/dd/p[3]/a
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/ul/li[4]/a').click()  # 点击还款中
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/table/tbody/tr[1]/td[10]/div/p/a[2]').click()  # 点击申请变现
        time.sleep(2)
        # 获取打开的多个窗口句柄
        windows = self.driver.window_handles
        # 切换到当前最新打开的窗口
        self.driver.switch_to.window(windows[-1])
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/p[1]/label[1]/span/input').click()  # 勾选已阅读
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/button').click()  # 确认
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="qtw"]/div[4]/div/div[2]/div/div[2]/div/div/div[2]/button[2]').click()  # 再次确认
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="qtw"]/div[4]/div/div[2]/div/div[2]/div/div/div[2]/button').click()  # 再次确认
        time.sleep(2)
        zzbidname = self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/table/tbody/tr/td[1]/a').text
        write_resourse("${zzbidname}",zzbidname)

    def investzzbid(self):
        '''债转出借'''
        zzbidname = read_resource("${zzbidname}")  # 读取标的名称
        #散标列表
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div[2]/div/div[2]/ul/li[2]/a/span').click()   #点击我要出借
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div[1]/ul/li[2]/a').click()         #点击债转列表
        time.sleep(2)
        self.driver.find_element_by_xpath("//*[text()='%s']/parent::p/parent::div"%zzbidname).click()   #查询标的名称，并点击标的
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div/div[1]/div[2]/div[2]/div/form/div[1]/div/div/span/div[2]/span').click()  # 点击全投
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div/div[1]/div[2]/div[2]/div/form/div[3]/button').click()          #点击立即出借
        time.sleep(2)
        #标的详情页面
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div/div/p/label[1]/span/input').click()  # 勾选协议
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div/div/div[4]/button').click()  # 确认出借
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="qtw"]/div[4]/div/div[2]/div/div[2]/div/div/div[2]/button').click()  # 确认阅读协议
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div/div/div[4]/button').click()  # 确认出借
        time.sleep(8)
        for i in range(5):
            op.click(1913, 1000)  #下拉滚动条
        op.click(840, 580)  # 发送验证码位置
        time.sleep(2)
        op.click(700, 580)  # 验证码输入框
        for i in '123456':
            op.dd(i)
        op.click(700, 650)  # 安全密码输入框
        for i in '123456':
            op.dd(i)
        op.click(740, 815)  # 确认
        # # 断言写在此处
        # time.sleep(10)
    def close(self):
        self.driver.quit()

    def userregister(self,num = "1"):
        '''
        :param num:  “2”表示注册借款人
        :return:
        '''
        #注册
        CI = CreateIdCard()
        idcard = CI.gennerator()  #身份证号码
        phone = phone_time()  # 注册的手机号
        list1 = ["自","赵","修","钱","孙","是","李","行","周","吴","郑","王","看","秒","人","场","我","间","生","时"]
        name = ""
        for i in range(5):
            name += random.choice(list1)

        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div/div[3]/div/div/div[2]/a').click()
        time.sleep(1)
        # if num == "2":
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div/div[3]/div/div/div[1]/div[1]/strong[2]').click()
        time.sleep(1)
        self.driver.find_element_by_id("mobile").send_keys(phone)  # 输入用户名
        time.sleep(1)
        self.driver.find_element_by_id("password").send_keys("a1234567")  # 输入密码
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div/div[3]/div/div/div[1]/form/div[3]/div/div/span/div/div/a/span').click()
        time.sleep(1)
        bd = MysqlDB()
        phonecode = bd.select_return_A_data("SELECT mes_body FROM qtw_invest_db.p2p_sms_record WHERE receive_address='%s' ORDER BY send_time DESC LIMIT 1;" %phone)[0]
        phonecode = regular("验证码：(.*?)，有",phonecode)
        print(phonecode)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div/div[3]/div/div/div[1]/form/div[3]/div/div/span/div/span/input').send_keys(phonecode)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="xieyi"]/label/span[1]/input').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div/div[3]/div/div/div[1]/form/div[4]/div/div/span/button').click()
        #开户                             #//*[@id="root"]/section/div[1]/div/div[3]/div/div/div[1]/form/div[4]/div/div/span/button
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div/a').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="cifName"]').send_keys(name)
        self.driver.find_element_by_xpath('//*[@id="idNum"]').send_keys(idcard)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/form/div[3]/div/div/span/button').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div/div/form/div/div[3]/div/div/div/span/button').click()
        time.sleep(10)
        #   处理廊坊页面
        for i in range(7):
            op.click(1913, 1000)  #下拉滚动条
        op.click(690, 150)        #银行卡
        for i in '6214920205490001':
            op.dd(i)
        op.click(690, 280)  # 手机号
        for i in phone:
            op.dd(i)
        op.click(840, 350)  # 验证码按钮
        op.click(690, 350)  # 验证码输入框
        for i in '123456':
            op.dd(i)
        op.click(690, 655)  # 密码输入框
        for i in '123456':
            op.dd(i)
        op.click(690, 720)  # 密码输入框
        for i in '123456':
            op.dd(i)
        op.click(540, 770)  # 已阅读
        op.click(690, 850)  # 确认开户
        time.sleep(5)
        self.khname = name

        print("注册手机号：%s"%phone)
        print("注册姓名：%s"%name)
        print("注册身份证号码：%s"%idcard)
        current_path = os.path.abspath(__file__)
        datapath = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'resourse\\data.txt')
        datapath = datapath.replace("\\", "/")
        usernamepath = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'resourse\\username.txt')
        usernamepath = usernamepath.replace("\\", "/")

        write_resourse("${theborrowerphone}",phone)
        write_resourse("${theborrowername}",name)
        write_resourse("${theborroweridcard}",idcard)

        with open(usernamepath,"w",encoding="utf-8") as f:
            f.write(phone)
            f.close()
        with open(datapath,"a+",encoding="utf-8") as f:
            f.write("${theborrowerphone}    %s\n"%phone)
            f.write("${theborrowername}    %s\n"%name)
            f.write("${theborrowerphone_pwd}    a1234567\n")
            f.write("${theborroweridcard}    %s\n"%idcard)
            f.write("=================================================\n")
            f.close()
        self.close()
    def anxinqian(self):
        #开通安心签，开通风险测评
        self.__init__()
        current_path = os.path.abspath(__file__)
        usernamepath = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'resourse\\username.txt')
        usernamepath = usernamepath.replace("\\", "/")
        with open(usernamepath,"r",encoding="utf-8") as f:
                name = f.read()
        self.investlogin(name,"a1234567")
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[1]/div[2]/div/div[2]/ul/li[6]/a/span').click()  # 点击我的账户
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[1]/div[1]/p[2]/a/img').click()  # 点击头像
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="root"]/section/div[2]/div/div/div[2]/div/div/div[1]/ul[2]/li[3]/a').click()  # 点击安心签
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="qtw"]/div[3]/div/div[2]/div/div[2]/div[3]/div/button[2]').click()
        time.sleep(7)                     #//*[@id="qtw"]/div[4]/div/div[2]/div/div[2]/button/span
        self.driver.find_element_by_xpath('//*[@id="qtw"]/div[4]/div/div[2]/div/div[2]/button/span').click()
        time.sleep(1)
        self.driver.quit()
        print("借款人注册成功请充值")




if __name__=="__main__":

    # obj = InvestPc()  # 资金前台Pc登录
    # # obj.userregister()
    # obj.anxinqian()
    pass



    # obj.withdraw(100)
    # obj.investzzbid()
    # obj.close()
