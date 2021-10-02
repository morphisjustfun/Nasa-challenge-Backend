import http.client
import json
from ..constants.constants import constantsWaqiData, constantsRegions
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


def getCorrelationEnvironmental(element, region):
    if region not in constantsRegions:
        return 0

    if element == constantsWaqiData['PM10']:
        if region == "AMAZONAS":
            return 0.5627566916528904
        elif region == 'ANCASH':
            return 0.8173273010971982
        elif region == 'APURIMAC':
            return 0.6474805023725039
        elif region == 'AREQUIPA':
            return 0.00781619824387759
        elif region == 'AYACUCHO':
            return 0.784757253846917
        elif region == "CAJAMARCA":
            return 0.74164612953903
        elif region == "CALLAO":
            return 0.8970919031887599
        elif region == "CUSCO":
            return 0.6718167999215203
        elif region == "HUANCAVELICA":
            return 0.8545300238837067
        elif region == "HUANUCO":
            return 0.9363674742541704
        elif region == "ICA":
            return 0.8883159356278151
        elif region == "JUNIN":
            return 0.7652728444671624
        elif region == "LA LIBERTAD":
            return 0.6901790433435225
        elif region == "LAMBAYEQUE":
            return 0.8001240125250154
        elif region == "LIMA METROPOLITANA":
            return 0.8955054530573233
        elif region == "LIMA REGION":
            return 0.7958334419289006
        elif region == "LORETO":
            return 0.7671243231065161
        elif region == "MADRE DE DIOS":
            return 0.043260562569202896
        elif region == "MOQUEGUA":
            return 0.8344427809997235
        elif region == "PASCO":
            return 0.7625866761983898
        elif region == "PIURA":
            return 0.7023301190768831
        elif region == "PUNO":
            return 0.5806501532836558
        elif region == "SAN MARTIN":
            return 0.27776696450063176
        elif region == "TACNA":
            return 0.9045187208137486
        elif region == "TUMBES":
            return 0.7165344039171333
        elif region == "UCAYALI":
            return 0.8326786517830622
    elif element == constantsWaqiData['PM2.5']:
        if region == "AMAZONAS":
            return 0.40523407228920016
        elif region == 'ANCASH':
            return 0.7353143421541393
        elif region == 'APURIMAC':
            return 0.510662452478387
        elif region == 'AREQUIPA':
            return 0.16232971893474246
        elif region == 'AYACUCHO':
            return 0.7521570003812963
        elif region == "CAJAMARCA":
            return 0.7064733203187411
        elif region == "CALLAO":
            return 0.8339499318238698
        elif region == "CUSCO":
            return 0.6994352173522465
        elif region == "HUANCAVELICA":
            return 0.8874905177687646
        elif region == "HUANUCO":
            return 0.7973598139768272
        elif region == "ICA":
            return 0.8389716317612844
        elif region == "JUNIN":
            return 0.7590791983766971
        elif region == "LA LIBERTAD":
            return 0.6778450625588925
        elif region == "LAMBAYEQUE":
            return 0.8293440823355036
        elif region == "LIMA METROPOLITANA":
            return 0.8184922730359367
        elif region == "LIMA REGION":
            return 0.7705467316337936
        elif region == "LORETO":
            return 0.6375692707379668
        elif region == "MADRE DE DIOS":
            return 0.23364576244812807
        elif region == "MOQUEGUA":
            return 0.6475992758574727
        elif region == "PASCO":
            return 0.7006550351215404
        elif region == "PIURA":
            return 0.7091754212637819
        elif region == "PUNO":
            return 0.6328545758367168
        elif region == "SAN MARTIN":
            return 0.047983266778415384
        elif region == "TACNA":
            return 0.8473840577109811
        elif region == "TUMBES":
            return 0.751373239144744
        elif region == "UCAYALI":
            return 0.8211500120056971


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
