from goodsFactory import GoodsFactory

class Handler(object):
    def __init__(self):
        pass

    @staticmethod
    def getOutputFromReceipt(receipt):
        goodsList = []
        goodsFactory = GoodsFactory()
        for info in receipt.split("\n"):
            goods = goodsFactory.getGoods(info)
            goodsList.append(goods)
        priceWithoutTax = 0
        total = 0
        lstOutPutText = []
        for item in goodsList:
            priceWithoutTax += item.price
            total += item.priceWithTax
            strItemPriceWithTax = "%.2f" % item.priceWithTax
            lstOutPutText += [str(item.cnt), " ", item.des, ": ", strItemPriceWithTax, "\n"]
        salesTaxes = total - priceWithoutTax
        lstOutPutText += ["Sales Taxes: ", "%.2f" % salesTaxes, "\n", "Total: ", "%.2f" % total]
        outPutText = "".join(lstOutPutText)
        return outPutText