#coding=utf-8
import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from libs.DealResource import *
from libs.MysqlDB import *
class CoreSystem():
    def __init__(self):
        '''核心系统相关操作'''
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
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)
        self.driver.get("http://192.168.1.77:84/controlPanel/login.html#")

    def corelogin(self):
        '''核心系统登录'''
        self.driver.find_element_by_id("userAccount").send_keys("sysadmin")  # 输入用户名
        self.driver.find_element_by_id("password").send_keys("123abc")  # 输入密码
        self.driver.find_element_by_id("code").send_keys("0000")  # 输入验证码
        self.driver.find_element_by_link_text("登录").click()  # 点击登录
        time.sleep(2)
        db = MysqlDB()
        debtcode = read_resource("${entry_code}")
        stutas = db.select_return_A_data("SELECT CASE WHEN ( projectId IS NULL OR projectId = '' ) THEN '未推送' ELSE '已推送' END as '推送状态' FROM qtw_core_db.core_loan_debt_info WHERE debtCode = '%s'"%debtcode)[0]
        print("您操作的这条债权状态：%s"%stutas)
        if stutas == "未推送":
            raise Exception("您操作的这条债权未推送，请手动添加廊坊存管")
            # self.driver.find_element_by_link_text('债权管理').click()
            # time.sleep(1)
            # self.driver.find_element_by_link_text('所有债权').click()  # 点击全部标的
            # time.sleep(1)
            # self.driver.find_element_by_id("debtCode").send_keys(debtcode)  # 新建散标-查询进件
            # self.driver.find_element_by_link_text('查询').click()
            # time.sleep(2)
            # self.driver.find_element_by_xpath('//*[@id="debtTbody"]/tr/td[15]/a[4]').click()   #点击存管
            # time.sleep(2)
            # web_alert = self.driver.switch_to.alert
            # web_alert.accept()
            # time.sleep(1)

    def bidding(self):
        '''核心系统发标'''
        entry_code = read_resource("${entry_code}")
        self.driver.find_element_by_link_text('出借管理').click()
        time.sleep(1)
        self.driver.find_element_by_link_text('全部标的').click()   #点击全部标的
        time.sleep(1)
        self.driver.find_element_by_link_text('新建散标').click()   #全部标的-新建散标
        time.sleep(1)
        self.driver.find_element_by_id("debtCode").send_keys(entry_code)   #新建散标-查询进件
        self.driver.find_element_by_link_text('查询').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="box"]').click()   #勾选债权
        self.driver.find_element_by_xpath('//*[@id="standardCreate"]/div/div[4]/ul/li/a').click()   #点击下一步
        time.sleep(3)
        # 确定alert
        web_alert = self.driver.switch_to.alert
        web_alert.accept()
        time.sleep(2)
        # 如果下面这行报错了，查看一下是否借款人的借款金额已经达到廊坊银行上限（债权管理——债权还款——添加到存管）
        self.driver.find_element_by_xpath('//*[@id="effectTime"]').send_keys("7")
        self.driver.find_element_by_xpath('//*[@id="confirmSubmit"]').click()
        time.sleep(2)
        # 【核心】点击出借管理-全部标的-新建散标-勾选债权-点击下一步-确定alert-发布设置-确定alert
        web_alert = self.driver.switch_to.alert
        web_alert.accept()
        time.sleep(1)
        web_alert.accept()
        time.sleep(5)
        self.driver.find_element_by_id("debtCode").send_keys(entry_code)
        self.driver.find_element_by_link_text('查询').click()
        time.sleep(2)
        bdname = self.driver.find_element_by_xpath('//*[@id="scatteredPubTbody"]/tr/td[4]/a').text
        print("创建散标成功，核心标的名称：" + bdname)
        write_resourse("${bdname}", bdname)
        time.sleep(1)

    def biddingcheck(self):
        '''散标待审核'''
        entry_code = read_resource("${entry_code}")
        self.driver.find_element_by_link_text('散标待审核').click()
        time.sleep(1)
        self.driver.find_element_by_id("debtCode").send_keys(entry_code)   #通过债权编号查询出数据
        self.driver.find_element_by_xpath('//*[@id="queryBtn"]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="scatteredPubTbody"]/tr/td[10]/a[2]').click()  #审核
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="qtw-main"]/div/div[2]/div[1]/ul/li/a').click()  #确认
        #alert弹窗
        time.sleep(2)
        a1 = self.driver.switch_to.alert  # 通过switch_to.alert切换到alert
        a1.accept()  # alert“确认”
        time.sleep(5)
        print("散标审核通过，发标到前台")

    @staticmethod
    def corereturnedmoney(term_num,dc=None):
            '''
            :param debtCode: 债权
            :param term_num: 回款期数
            :return: 回款
            '''
            if dc == None:
                debtCode = read_resource("${entry_code}")
            else:
                debtCode = dc
            db = MysqlDB()
            should_date = db.select_return_A_data('SELECT should_date FROM qtw_loan_db.p2p_borrower_return_plan WHERE debtcode = "%s" AND term_num = %s' % (debtCode, term_num))
            should_date = str(should_date[0])
            # print("=================跑手工任务给回款第%s期，给出借人，时间%s====================" % (term_num, should_date))
            coreurlbase = "http://192.168.1.77:84/core-admin-api"
            core = requests.Session()
            url1 = coreurlbase + "/random"
            data1 = {"cacheid": "0.49101218522027756"}
            header1 = {"Content-Type": "application/json"}
            core.get(url1, params=data1, headers=header1)
            url2 = coreurlbase + "/rest/user/back/accountLogin"
            data2 = {'callback': 'jQuery17209220007142597262_1541401333724', 'jsonParams': ''
                                                                                           '{"method":"login","params":{"userAccount":"sysadmin","password":"123abc","randnumber":'
                                                                                           '"0000","randnumKey":"0.49101218522027756","autoLogin":"FALSE","serviceUrl":null}}',
                     '_': '1541401341903'}
            resl = core.get(url2, params=data2, headers=header1)
            # print(resl.text)
            url3 = coreurlbase + "/rest/testCrontabJob/testAutoCashBack"
            # print(url3)
            header1 = {"Content-Type": "application/json"}
            data3 = {'jsonParams': '{"method":"testAutoCashBack","params":{"cashBackDate":%s,"debtCode":"%s"}}\n' % (
                should_date, debtCode), '_': '1542807282908', 'callback': 'jQuery17204517549754820951_1542806876216\n',
                     't': '1542807282907\n'}
            # print(data3)
            rels = core.get(url3, params=data3, headers=header1)
            # print(rels.text)
            if "SUCCESS" in rels.text:
                print("核心交易执行手工正常回款任务成功")
            else:
                raise Exception("核心交易执行手工正常回款任务失败")
            print("正在回款，请稍后。。。")
            repayStatus = "0"
            for i in range(10):
                time.sleep(15)
                url4 = coreurlbase + "/rest/settle/queryDebtRepayPage"
                header1 = {"Content-Type": "application/json"}
                data4 = {'callback': 'jQuery17206316655256710433_1562162797078\n', '_': '1562162810402',
                         't': '1562162810402\n',
                         'jsonParams': '{"method":"queryDebtRepayPage","params":{"page":{"conditions":"{\\"debtCode\\":\\"%s\\"}","pageNum":1,"pageSize":10}}}\n' % debtCode}
                rels = core.get(url4, params=data4, headers=header1)
                # print(rels.text)
                rStatus = regular('periodSeq":%s,"planRepayDate(.+?)}' % term_num, rels.text)
                repayStatus = regular('repayStatus":"(.+?)"', rStatus)
                # print(repayStatus)
                if repayStatus == "10":
                    print("回款成功")
                    break
            if repayStatus != "10":
                raise Exception("回款失败")

    def close(self):
        self.driver.close()

if __name__=="__main__":
    core = CoreSystem()
    core.corelogin()
    # a.biddingcheck()