from goods import  ExemptGoods, NormalGoods, ImportedGoods
from decimal import Decimal

class Parser(object):
    def __init__(self):
        pass

    @staticmethod
    def getGoodsDetails(info):
        strCnt_desc, strPriceEach = info.split(" at ")
        strCnt = strCnt_desc.split(" ")[0]
        cnt = int(strCnt)
        strDesc = strCnt_desc[len(strCnt) + 1::]
        priceEach = Decimal(strPriceEach.rstrip(" "))
        return cnt, strDesc, priceEach


class GoodsFactory(object):
    exemptGoodsDict = {"food": ["chocolates", "chocolate", "banana"], "books": ["book"], "medical product": ["pills"]}
    normalGoodsDict = {"normal": ["perfume", "necklace", "CD"]}

    def __init__(self):
        super(GoodsFactory, self).__init__()
        pass

    @staticmethod
    def updateExemptGoodsDict(classDesc, itemDes):
        if classDesc in GoodsFactory.exemptGoodsDict.keys():
            GoodsFactory.exemptGoodsDict.update({classDesc: GoodsFactory.exemptGoodsDict[classDesc] + [itemDes]})
        else:
            GoodsFactory.exemptGoodsDict.update({classDesc: [itemDes]})


    @staticmethod
    def updateNormalGoodsDict(classDesc, itemDes):
        if classDesc in GoodsFactory.normalGoodsDict.keys():
            GoodsFactory.normalGoodsDict.update({classDesc: GoodsFactory.normalGoodsDict[classDesc] + [itemDes]})
        else:
            GoodsFactory.normalGoodsDict.update({classDesc: [itemDes]})

    def __getExemptGoods(self, strDesc, cnt, priceEach):
        strDescList = strDesc.split(" ")
        allValues = []
        for key in GoodsFactory.exemptGoodsDict.keys():
            allValues += GoodsFactory.exemptGoodsDict[key]
        for word in strDescList:
            if word in allValues:
                goods = ExemptGoods(strDesc, cnt, priceEach)
                return goods
        goods = ExemptGoods()
        goods.setAsEmpty()
        return goods

    def __getNormalGoods(self, strDesc, cnt, priceEach):
        strDescList = strDesc.split(" ")
        allValues = []
        for key in GoodsFactory.normalGoodsDict.keys():
            allValues += GoodsFactory.normalGoodsDict[key]
        for word in strDescList:
            if word in allValues:
                goods = NormalGoods(strDesc, cnt, priceEach, 0.1)
                return goods
        goods = NormalGoods()
        goods.setAsEmpty()
        return goods

    def getGoods(self, info):
        cnt, strDesc, priceEach = Parser.getGoodsDetails(info)
        strDescList = strDesc.split(" ")
        goods = None

        goodsHandlersChainOfResponsibility = [self.__getExemptGoods, self.__getNormalGoods]
        for handler in goodsHandlersChainOfResponsibility:
            goods = handler(strDesc, cnt, priceEach)
            if not goods.isEmpty:
                break

        # check is imported or not
        if not goods.isEmpty:
            if "imported" in strDescList:
                goods = ImportedGoods(goods)

        return goods