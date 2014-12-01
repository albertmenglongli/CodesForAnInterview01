from goods import *
from goodsFactory import GoodsFactory, Parser
from myUtils import  getBasicRound
from handler import Handler


def testHandler():
    # test Input1
    input1 = """1 book at 12.49
1 music CD at 14.99
1 chocolate bar at 0.85"""

    output1 = Handler.getOutputFromReceipt(input1)
    assert output1 == """1 book: 12.49
1 music CD: 16.49
1 chocolate bar: 0.85
Sales Taxes: 1.50
Total: 29.83"""

    # test Input2
    input2 = """1 imported box of chocolates at 10.00
1 imported bottle of perfume at 47.50"""

    output2 = Handler.getOutputFromReceipt(input2)

    assert output2 == """1 imported box of chocolates: 10.50
1 imported bottle of perfume: 54.65
Sales Taxes: 7.65
Total: 65.15"""

    # test Input3
    input3 = """1 imported bottle of perfume at 27.99
1 bottle of perfume at 18.99
1 packet of headache pills at 9.75
1 box of imported chocolates at 11.25"""

    output3 = Handler.getOutputFromReceipt(input3)

    assert output3 == """1 imported bottle of perfume: 32.19
1 bottle of perfume: 20.89
1 packet of headache pills: 9.75
1 box of imported chocolates: 11.85
Sales Taxes: 6.70
Total: 74.68"""


def testFactory():
    goodsFactory = GoodsFactory()

    # very basic goods test, item "book"
    info = "1 book at 12.49"
    goods = goodsFactory.getGoods(info)
    assert isinstance(goods, ExemptGoods)
    assert goods.cnt == 1
    assert goods.price == Decimal("12.49")

    # basic goods test with description more than one word like "music CD"
    info = "1 music CD at 3000"
    goods = goodsFactory.getGoods(info)
    assert isinstance(goods, NormalGoods)

    # if one item cannot be interpreted, an empty goods should be generate
    info = "1 goodsUnknown at 12.49"
    goods = goodsFactory.getGoods(info)
    assert goods.isEmpty

    # new items added for expansion
    info = "1 banana at 3.0"
    goods = goodsFactory.getGoods(info)
    assert isinstance(goods, ExemptGoods)

    # add an item belongs to food without tax when running
    GoodsFactory.updateExemptGoodsDict("food", "orange")
    info = "2 orange at 4.0"
    goods = goodsFactory.getGoods(info)
    assert goods.price == Decimal("8")
    assert goods.des == "orange"

    # add an item belongs to no key in the exemptGoods when running
    GoodsFactory.updateExemptGoodsDict("water", "coke")
    info = "2 bottle of coke at 3.0"
    goods = goodsFactory.getGoods(info)
    assert goods.price == Decimal("6.0")

    goodsFactory.updateNormalGoodsDict("normal", "light")
    info = "1 light at 10.0"
    goods = goodsFactory.getGoods(info)
    assert goods.priceWithTax == Decimal("11")


    # test imported stuff
    info = "1 imported bottle of perfume at 27.99"
    goods = goodsFactory.getGoods(info)
    assert isinstance(goods, ImportedGoods)
    assert goods.priceWithTax == Decimal("32.19")


def testParser():
    info = "1 book at 12.49"
    cnt, desc, priceEach = Parser.getGoodsDetails(info)
    assert cnt == 1
    assert desc == "book"
    assert priceEach == Decimal("12.49")

    info = "2 imported box of chocolates at 10.00"
    cnt, desc, priceEach = Parser.getGoodsDetails(info)
    assert cnt == 2
    assert desc == "imported box of chocolates"
    assert priceEach == Decimal("10.00")


def testGoodsPriceWithTax():
    # an empty goods
    goods = ExemptGoods("")
    goods.setAsEmpty()
    assert goods.price == 0

    # exempt goods without tax
    books = ExemptGoods("book", price=10)
    assert books.priceWithTax == Decimal("10")

    # normal goods with tax rate 10%
    cd = NormalGoods("cd", price=14.99, taxRate=0.1)
    assert cd.priceWithTax == Decimal(str(16.49))

    # imported exempt goods with tax updated from 0% to 5%
    importedBooks = ImportedGoods(ExemptGoods("book", cnt=1, price=10))
    assert importedBooks.tax == Decimal("0.5")
    assert importedBooks.priceWithTax == Decimal("10.5")

    # import normal goods with tax updated from 10% to 15%
    perfume = ImportedGoods(NormalGoods("perfume", price=47.5, taxRate=0.1))
    assert perfume.priceWithTax == Decimal("54.65")

    # two exempt goods without tax
    books = ExemptGoods("books", cnt=2, price=10)
    assert books.priceWithTax == Decimal("20")

    # two imported exempt good with tax 0.05
    books = ImportedGoods(ExemptGoods("books", cnt=2, price=10))
    assert books.priceWithTax == Decimal("21")

    # goods imported many times from one country to another and then the third country
    aFromUSAtoUK = ImportedGoods(NormalGoods("necklace", cnt=1, price=100, taxRate=0.1))
    assert aFromUSAtoUK.priceWithTax == Decimal("115")
    bFromUKtoChina = ImportedGoods(aFromUSAtoUK)
    assert bFromUKtoChina.priceWithTax == Decimal("120")

    # many goods imported many times from one country to second and then to the third country
    aFromUSAtoUK = ImportedGoods(NormalGoods("necklace", cnt=2, price=100, taxRate=0.1))
    assert aFromUSAtoUK.priceWithTax == Decimal("230")
    bFromUKtoChina = ImportedGoods(aFromUSAtoUK)
    assert bFromUKtoChina.priceWithTax == Decimal("240")


def testBasicRound():
    assert getBasicRound(1.499) == Decimal(str(1.50))
    assert getBasicRound(10.5) == Decimal(str(10.5))


def testMyRound():
    assert myRound(14.99 * 0.1) == Decimal("1.5")
    assert myRound(16.487) == Decimal("16.49")
    assert myRound(1.234) == Decimal("1.25")


if __name__ == "__main__":
    testHandler()
    testFactory()
    testParser()
    testGoodsPriceWithTax()
    testBasicRound()
    testMyRound()