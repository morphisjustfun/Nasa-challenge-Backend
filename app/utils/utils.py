import datetime
from .utilsOpenCovid import getIndex
from .utilsVaccine import getVaccineEffect


def getMonday(dateNow):
    today = dateNow
    today = today + datetime.timedelta(days=-today.weekday(), weeks=-1)
    return today.strftime("%d-%m-%Y")


def getOffSetTime():
    x = datetime.date(2021, 9, 29)
    return int((x - (datetime.date.today())).days / 7)

def getReinfectionRate (covidBefore, risk):
    if covidBefore:
        return risk * 0.16
    else:
        return risk

def getRisk3ndComplete(city, dose, brand, covidBefore):
    first = getIndex(city)
    second = getVaccineEffect(dose, brand, first)
    third = getReinfectionRate(covidBefore,second)
    return third
