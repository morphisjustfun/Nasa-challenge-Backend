import datetime
from .utilsOpenCovid import getIndex
from .utilsEnvironmental import getRisk2nd
from .utilsVaccine import getVaccineEffect

def getMonday(dateNow):
    today = dateNow
    today = today + datetime.timedelta(days=-today.weekday(), weeks=-1)
    return today.strftime("%d-%m-%Y")

def getOffSetTime():
    x = datetime.date(2021,9,29)
    return int((x - (datetime.date.today())).days/7)

def getRisk3ndComplete(city, dose, brand):
    first = getIndex(city)
    second = getRisk2nd(first)
    third = getVaccineEffect (dose, brand, second)
    return third
