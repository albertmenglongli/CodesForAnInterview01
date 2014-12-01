from decimal import Decimal
from myUtils import myRound
from copy import deepcopy

class Goods(object):
    def __init__(self, itemDes="", cnt=1, price=0, taxRate=0):
        super(Goods, self).__init__()
        self.__itemDes = itemDes
        self.__priceEach = Decimal(str(price))
        self.__taxRate = Decimal(str(taxRate))
        self.__taxCal = None
        self.__cnt = cnt
        # an empty goods is very important when we can not parse the goods correctly
        self.isEmpty = False

    def setAsEmpty(self):
        self.isEmpty = True
        self.__itemDes = ""
        self.__cnt = 0
        self.__priceEach = 0
        self.__taxRate = 0
        self.__taxCal = 0

    def updateTaxRateIncreasedBy(self, rate):
        if type(rate) is not Decimal:
            rate = Decimal(rate)
        self.__taxRate += rate
        self.__taxCal = None

    @property
    def priceEach(self):
        return self.__priceEach

    @property
    def price(self):
        return self.__priceEach * self.__cnt

    @property
    def des(self):
        return self.__itemDes

    @property
    def cnt(self):
        return self.__cnt

    @property
    def tax(self):
        if self.__taxCal is None:
            self.__taxCal = myRound(self.__taxRate * self.__priceEach)
        return self.__taxCal * self.__cnt

    @property
    def priceWithTax(self):
        return Decimal(myRound((1 + self.__taxRate ) * self.__priceEach) * self.__cnt)


class NormalGoods(Goods):
    def __init__(self, itemDes="", cnt=1, price=0, taxRate=0.1):
        super(NormalGoods, self).__init__(itemDes, cnt, price, taxRate)


class ExemptGoods(Goods):
    def __init__(self, itemDes="", cnt=1, price=0):
        super(ExemptGoods, self).__init__(itemDes, cnt, price, taxRate=0)


class ImportedGoods(Goods):
    def __init__(self, goods, extraImportedRate=0.05):
        self.__goods = deepcopy(goods)
        self.__goods.updateTaxRateIncreasedBy(extraImportedRate)

    def __getattr__(self, item):
        return self.__goods.__getattribute__(item)