import sys
import unittest
from qutouwang.InvestPc import *
from qutouwang.LoanSystem import *
from qutouwang.CoreSystem import *
#cmd命令行执行执行脚本出错时的解决方法
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

class qtw(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    # @unittest.skip("continue")
    def test001(self):
        '''注册借款人'''
        invest = InvestPc()  # 资金前台Pc登录
        invest.userregister(2)
        invest.anxinqian()
        invest.close()
    def test002(self):
        '''充值'''
        phone = read_resource("${theborrowerphone}")
        password = read_resource("${theborrowerphone_pwd}")
        obj = InvestPc()  # 资金前台Pc登录
        obj.investlogin(phone, password)
        obj.recharge(8000)     #在这里输入充值金额
        obj.close()
    # @unittest.skip("continue")
    def test003(self):
        '''提现'''
        phone = read_resource("${thelenderphone}")
        password = read_resource("${thelenderphone_pwd}")
        obj = InvestPc()  # 资金前台Pc登录
        obj.investlogin(phone, password)
        obj.withdraw(100)
        obj.close()
    def test004(self):
        '''散标流程,正常还款回款'''
        # 借款系统进件
        phone = read_resource("${theborrowerphone}")
        idcard = read_resource("${theborroweridcard}")
        name = read_resource("${theborrowername}")
        jkname = "鑫优贷B"
        rate = "0.1"
        month = "6"
        money = "10000"
        loan = LoanSystem()
        loan.loanlogin()
        loan.IntoEntry(phone,idcard,name,rate,month,money,jkname)
        loan.close()
        # 去投网借款签约
        invest = InvestPc()
        phone = read_resource("${theborrowerphone}")
        password = read_resource("${theborrowerphone_pwd}")
        invest.investlogin(phone,password)
        invest.signing()
        invest.close()
        #借款系统债权编辑、债权审核
        loan1 = LoanSystem()
        loan1.loanlogin()
        loan1.editdebtCode()
        loan1.chechdebtCode()
        loan1.close()
        #核心系统发标，并审核
        core = CoreSystem()
        core.corelogin()
        core.bidding()
        core.biddingcheck()
        core.close()
        #去投网出借,并判断满标
        phone = read_resource("${thelenderphone}")
        password = read_resource("${thelenderphone_pwd}")
        invest1 = InvestPc()  # 资金前台Pc登录
        invest1.investlogin(phone, password)
        invest1.invest()
        invest1.close()
        #借款系统放款
        loan3 = LoanSystem()
        loan3.loanlogin()
        loan3.loan_fk()
        loan3.close()
        # 正常还款
        phone = read_resource("${theborrowerphone}")
        password = read_resource("${theborrowerphone_pwd}")
        invest2 = InvestPc()  # 资金前台Pc登录
        invest2.investlogin(phone, password)
        invest2.repayment(1)               #还款
        CoreSystem.corereturnedmoney(1)    #手工回款
        invest2.repayment(2)               #还款
        CoreSystem.corereturnedmoney(2)    #手工回款
        invest2.repayment(3)               #还款
        CoreSystem.corereturnedmoney(3)    #手工回款
        invest2.repayment(4)               #还款
        CoreSystem.corereturnedmoney(4)    #手工回款
        invest2.repayment(5)               #还款
        CoreSystem.corereturnedmoney(5)    #手工回款
        invest2.repayment(6)               #还款
        CoreSystem.corereturnedmoney(6)    #手工回款
        invest2.close()

    def test005(self):
        '''散标流程,还款回款,逾期还款，提前结清'''
        # 借款系统进件
        phone = read_resource("${theborrowerphone}")
        idcard = read_resource("${theborroweridcard}")
        name = read_resource("${theborrowername}")
        jkname = "鑫优贷B"
        rate = "0.11"
        month = "12"
        money = "10000"
        loan = LoanSystem()
        loan.loanlogin()
        loan.IntoEntry(phone, idcard, name, rate, month, money,jkname)
        loan.close()
        # 去投网借款签约
        invest = InvestPc()
        phone = read_resource("${theborrowerphone}")
        password = read_resource("${theborrowerphone_pwd}")
        invest.investlogin(phone,password)
        invest.signing()
        invest.close()
        #借款系统债权编辑、债权审核
        loan1 = LoanSystem()
        loan1.loanlogin()
        loan1.editdebtCode()
        loan1.chechdebtCode()
        loan1.close()
        #核心系统发标，并审核
        core = CoreSystem()
        core.corelogin()
        core.bidding()
        core.biddingcheck()
        core.close()
        # #去投网出借,并判断满标
        # phone = read_resource("${thelenderphone}")
        # password = read_resource("${thelenderphone_pwd}")
        # invest1 = InvestPc()  # 资金前台Pc登录
        # invest1.investlogin(phone, password)
        # invest1.invest()
        # invest1.close()
        # #借款系统放款
        # loan3 = LoanSystem()
        # loan3.loanlogin()
        # loan3.loan_fk()
        # loan3.close()
        # # 第一期正常还款，一次还清
        # phone = read_resource("${theborrowerphone}")
        # password = read_resource("${theborrowerphone_pwd}")
        # invest2 = InvestPc()  # 资金前台Pc登录
        # invest2.investlogin(phone, password)
        # invest2.repayment(1)               #还款
        # CoreSystem.corereturnedmoney(1)    #手工回款
        # invest2.close()
        # # 第二期正常还款，部分还款
        # phone = read_resource("${theborrowerphone}")
        # password = read_resource("${theborrowerphone_pwd}")
        # invest2 = InvestPc()  # 资金前台Pc登录
        # invest2.investlogin(phone, password)
        # invest2.repayment(2,100)               #还款
        # invest2.repayment(2,100)               #还款
        # invest2.repayment(2)               #还款
        # CoreSystem.corereturnedmoney(2)    #手工回款
        # invest2.close()
        # 第三期逾期还款，宽限期外逾期8天，一次还清
        # loan4 = LoanSystem()
        # loan4.loanlogin()
        # loan4.overdueoneday(3)
        # loan4.applyReport()     #申请垫付
        # loan4.padPay()          #执行垫付
        # loan4.overduemanyday(3,8)
        # loan4.close()
        # phone = read_resource("${theborrowerphone}")
        # password = read_resource("${theborrowerphone_pwd}")
        # invest4 = InvestPc()  # 资金前台Pc登录
        # invest4.investlogin(phone, password)
        # invest4.repayment(3)
        # 第四期逾期还款，宽限期外逾期8天，部分还款
        # loan4 = LoanSystem()
        # loan4.loanlogin()
        # loan4.overdueoneday(4)
        # loan4.applyReport()  # 申请垫付
        # loan4.padPay()  # 执行垫付
        # loan4.overduemanyday(4, 8)
        # loan4.close()
        # phone = read_resource("${theborrowerphone}")
        # password = read_resource("${theborrowerphone_pwd}")
        # invest4 = InvestPc()  # 资金前台Pc登录
        # invest4.investlogin(phone, password)
        # invest4.repayment(4,20)
        # invest4.repayment(4,20)
        # invest4.repayment(4,80)
        # invest4.repayment(4)
        # #第五期，逾期还款，逾期5天，一次还清
        # loan4 = LoanSystem()
        # loan4.loanlogin()
        # loan4.overdueoneday(5)
        # loan4.applyReport()  # 申请垫付
        # loan4.padPay()  # 执行垫付
        # loan4.overduemanyday(5, 2)
        # loan4.close()
        # phone = read_resource("${theborrowerphone}")
        # password = read_resource("${theborrowerphone_pwd}")
        # invest4 = InvestPc()  # 资金前台Pc登录
        # invest4.investlogin(phone, password)
        # invest4.repayment(5)
        # # 第六期，逾期还款，逾期2天，部分还款
        # loan4 = LoanSystem()
        # loan4.loanlogin()
        # loan4.overdueoneday(6)
        # loan4.applyReport()  # 申请垫付
        # loan4.padPay()  # 执行垫付
        # loan4.overduemanyday(6, 2)
        # loan4.close()
        # phone = read_resource("${theborrowerphone}")
        # password = read_resource("${theborrowerphone_pwd}")
        # invest4 = InvestPc()  # 资金前台Pc登录
        # invest4.investlogin(phone, password)
        # invest4.repayment(6,100)
        # invest4.repayment(6,100)
        # invest4.repayment(6)
        #
        # #部分还款手动结清
        # invest4.repayment(7, 20)
        # invest4.earlyRepaymentOperation()
        # invest4.close()

    def test006(self):
        '''申请债权转让'''
        # 借款系统进件
        phone = read_resource("${theborrowerphone}")
        idcard = read_resource("${theborroweridcard}")
        name = read_resource("${theborrowername}")
        rate = "0.1"
        month = "6"
        money = "10000"
        jkname = "鑫优贷B"
        loan = LoanSystem()
        loan.loanlogin()
        loan.IntoEntry(phone, idcard, name, rate, month, money,jkname)
        loan.close()
        # 去投网借款签约
        invest = InvestPc()
        phone = read_resource("${theborrowerphone}")
        password = read_resource("${theborrowerphone_pwd}")
        invest.investlogin(phone,password)
        invest.signing()
        invest.close()
        #借款系统债权编辑、债权审核
        loan1 = LoanSystem()
        loan1.loanlogin()
        loan1.editdebtCode()
        loan1.chechdebtCode()
        loan1.close()
        #核心系统发标，并审核
        core = CoreSystem()
        core.corelogin()
        core.bidding()
        core.biddingcheck()
        core.close()
        #去投网出借,并判断满标
        phone = read_resource("${thelenderphone}")
        password = read_resource("${thelenderphone_pwd}")
        invest1 = InvestPc()  # 资金前台Pc登录
        invest1.investlogin(phone, password)
        invest1.invest()
        invest1.close()
        #借款系统放款
        loan3 = LoanSystem()
        loan3.loanlogin()
        loan3.loan_fk()
        loan3.close()
        #正常还款
        phone = read_resource("${theborrowerphone}")
        password = read_resource("${theborrowerphone_pwd}")
        invest2 = InvestPc()  # 资金前台Pc登录
        invest2.investlogin(phone, password)
        invest2.repayment(1)  # 还款
        CoreSystem.corereturnedmoney(1)  # 手工回款
        invest2.repayment(2)  # 还款
        CoreSystem.corereturnedmoney(2)  # 手工回款
        invest2.repayment(3)  # 还款
        CoreSystem.corereturnedmoney(3)  # 手工回款
        invest2.close()
        #申请债转
        phone = read_resource("${thelenderphone}")
        password = read_resource("${thelenderphone_pwd}")
        invest3 = InvestPc()  # 资金前台Pc登录
        invest3.investlogin(phone, password)
        invest3.changedebtplan()
        invest3.investTranferDebtConfirm()
        invest3.close()
        #承接债转
        phone = read_resource("${thelrecipientphone}")
        password = read_resource("${thelrecipientphone_pwd}")
        invest4 = InvestPc()  # 资金前台Pc登录
        invest4.investlogin(phone, password)
        invest4.investzzbid()
        invest4.close()
    def test007(self):
        '''手工回款'''
        debtcode = "jj2019092000003"  #债权编号
        tremnum = 5                  #回款期数
        CoreSystem.corereturnedmoney(tremnum,debtcode)  # 手工回款

if __name__ == '__main__':
    unittest.main()
