from decimal import Decimal

def getRound2NearestDot05(number):
    if type(number) is not Decimal:
        number = Decimal(str(number))
    numberTmp = number
    numberTmp = int(numberTmp * 100)
    singleDigit = numberTmp % 10
    if 0 < singleDigit < 5:
        numberTmp = numberTmp / 10 * 10 + 5
        number = numberTmp / 100.0
        return Decimal(str(number))
    else:
        number = numberTmp / 100.0
        return Decimal(str(number))


def getBasicRound(number):
    if type(number) is not Decimal:
        number = Decimal(str(number))
    number = round(number, ndigits=2)
    return number


def myRound(number):
    return getRound2NearestDot05(getBasicRound(number))