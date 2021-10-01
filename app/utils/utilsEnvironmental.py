import http.client
import json
from ..constants.constants import constantsWaqiData
from statistics import mean


def getFactor(element, difference):
    if element == constantsWaqiData['PM10']:
        sigDif = int(difference/10)
        return (1.76/100)*sigDif
    elif element == constantsWaqiData['PM2.5']:
        sigDif = int(difference/10)
        return (2.24/100)*sigDif
    elif element == constantsWaqiData['O3']:
        sigDif = int(difference/10)
        return (4.76/100)*sigDif


def getWaqiData():
    pm10Total = []
    pm25Total = []
    o3Total = []

    pm10AvgTotal = []
    pm25AvgTotal = []
    o3AvgTotal = []

    for department in ['@7580', '@7577', '@7578', '@8780', '@379']:
        conn = http.client.HTTPSConnection("api.waqi.info")
        payload = ''
        headers = {}
        conn.request(
            "GET", f"/feed/{department}/?token={constantsWaqiData['TOKEN']}", payload, headers)
        res = conn.getresponse()
        data = res.read()
        jsonData = json.loads(data.decode('utf-8'))
        jsonDataFiltered = jsonData[constantsWaqiData['DATA']
                                    ][constantsWaqiData['IAQI']]
        jsonDataAvgFiltered = jsonData[constantsWaqiData['DATA']
                                       ][constantsWaqiData['FORECAST']][constantsWaqiData['DAILY']]

        for unit in [constantsWaqiData['PM10'], constantsWaqiData['PM2.5'], constantsWaqiData['O3']]:
            if unit in jsonDataFiltered.keys() and unit == constantsWaqiData['PM10']:
                pm10Total.append(jsonDataFiltered[unit]['v'])
            if unit in jsonDataFiltered.keys() and unit == constantsWaqiData['PM2.5']:
                pm25Total.append(jsonDataFiltered[unit]['v'])
            if unit in jsonDataFiltered.keys() and unit == constantsWaqiData['O3']:
                o3Total.append(jsonDataFiltered[unit]['v'])

            if unit in jsonDataAvgFiltered.keys():
                unitData = []
                for day in jsonDataAvgFiltered[unit]:
                    avg = day['avg']
                    unitData.append(avg)
                if unit == constantsWaqiData['PM10']:
                    pm10AvgTotal.append(mean(unitData))
                if unit == constantsWaqiData['PM2.5']:
                    pm25AvgTotal.append(mean(unitData))
                if unit == constantsWaqiData['O3']:
                    o3AvgTotal.append(mean(unitData))

    pm10 = mean(pm10Total)
    pm25 = mean(pm25Total)
    o3 = mean(o3Total)

    pm10Avg = mean(pm10AvgTotal)
    pm25Avg = mean(pm25AvgTotal)
    o3Avg = mean(o3AvgTotal)

    currentData = {constantsWaqiData['PM10']: pm10,
                   constantsWaqiData['PM2.5']: pm25,    constantsWaqiData['O3']: o3}
    avgData = {constantsWaqiData['PM10']: pm10Avg,
               constantsWaqiData['PM2.5']: pm25Avg, constantsWaqiData['O3']: o3Avg}

    return {'currentData': currentData, 'avgData': avgData}

def getRisk2nd(inputNumber):
    environmentalData = getWaqiData()
    increments = []
    for element in [constantsWaqiData['PM10'],constantsWaqiData['PM2.5'],constantsWaqiData['O3']]:
        difference = abs(environmentalData['currentData'][element] - environmentalData['avgData'][element])
        factor = getFactor(element,difference)
        increments.append(factor * inputNumber)
    returnNumber = inputNumber
    for increment in increments:
        returnNumber = returnNumber + increment
    return returnNumber
