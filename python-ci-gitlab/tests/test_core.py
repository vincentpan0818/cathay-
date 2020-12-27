import pytest

from cathay.sample.customer import Customer
from cathay.sample.core import CustomerDataProcess
from decimal import Decimal, ROUND_DOWN

INIT_MONEY=100.0

class TestCoreSuites:
 bank=Customer ("Test User","100-1100")
 def test_one(self):
     self.bank.deposit(0)
     assert self.bank.balance==0
 
 def test_two(self):
     self.bank.deposit(INIT_MONEY)
     assert self.bank.balance==100

 def test_three(self):
     self.bank.deposit(1000)
     assert self.bank.balance==1100
 
 def test_four(self):
     self.bank.withdraw(500)
     assert self.bank.balance==600
    
 def test_five(self):
     self.bank.withdraw(700)
     assert self.bank.balance=='balance not enough'

##########################################################################################
#
# 假設這位客戶, 名字是 Test User, 帳號為100-1100, 一開始帳戶會先存100元, 要測試下面項目: 
# 1. 之後存款1000元, 確認帳戶總金額為1100元
# 2. 接續提款500元, 確認帳戶總金額為600元
# 3. 之後提款700元, 會出現 RuntimeError
#
##########################################################################################
