import http.client
import json
from ..constants.constants import constantsWaqiData
from statistics import mean


def getFactorV2(element, difference):
    if element == constantsWaqiData['PM2.5']:
        if difference <= 21.683:
            return 1
        elif difference <= 42.367:
            return 2
        elif difference <= 63.05:
            return 3
        elif difference <= 83.733:
            return 4
        elif difference <= 104.417:
            return 5
        else:
            return 6
    elif element == constantsWaqiData['PM10']:
        if difference <= 50.313:
            return 1
        elif difference <= 72.775:
            return 2
        elif difference <= 95.236:
            return 3
        elif difference <= 117.698:
            return 4
        elif difference <= 140.16:
            return 5
        else:
            return 6

def getCorrelationEnvironmental(element):
    if element == constantsWaqiData['PM2.5']:
        return 0.6475992758574727
    elif element == constantsWaqiData['PM10']:
        return 0.8344427809997236


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
            "GET",
            f"/feed/{department}/?token={constantsWaqiData['TOKEN']}",
            payload,
            headers)
        res = conn.getresponse()
        data = res.read()
        jsonData = json.loads(data.decode('utf-8'))
        jsonDataFiltered = jsonData[constantsWaqiData['DATA']
                                    ][constantsWaqiData['IAQI']]
        jsonDataAvgFiltered = jsonData[constantsWaqiData['DATA']
                                       ][constantsWaqiData['FORECAST']][constantsWaqiData['DAILY']]

        for unit in [
                constantsWaqiData['PM10'],
                constantsWaqiData['PM2.5'],
                constantsWaqiData['O3']]:
            if unit in jsonDataFiltered.keys(
            ) and unit == constantsWaqiData['PM10']:
                pm10Total.append(jsonDataFiltered[unit]['v'])
            if unit in jsonDataFiltered.keys(
            ) and unit == constantsWaqiData['PM2.5']:
                pm25Total.append(jsonDataFiltered[unit]['v'])
            if unit in jsonDataFiltered.keys(
            ) and unit == constantsWaqiData['O3']:
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

    currentData = {
        constantsWaqiData['PM10']: pm10,
        constantsWaqiData['PM2.5']: pm25,
        constantsWaqiData['O3']: o3}
    avgData = {
        constantsWaqiData['PM10']: pm10Avg,
        constantsWaqiData['PM2.5']: pm25Avg,
        constantsWaqiData['O3']: o3Avg}

    return {'currentData': currentData, 'avgData': avgData}
