import http.client
import json
from ..constants.constants import constantsOpenCovidData
import pandas as pd
import datetime


def CasesPer100K(inputNumber):
    if inputNumber <= 4:
        return 1
    elif inputNumber <= 9:
        return 2
    elif inputNumber <= 50:
        return 3
    elif inputNumber <= 100:
        return 4
    elif inputNumber <= 199:
        return 5
    else:
        return 6


def ConfirmedDeaths100K(inputNumber):
    if inputNumber < 0.1:
        return 2
    elif inputNumber <= 1:
        return 3
    elif inputNumber <= 2:
        return 4
    elif inputNumber <= 5:
        return 5
    else:
        return 6


def PositivityRate(inputNumber):
    if inputNumber <= 2.9:
        return 1
    elif inputNumber <= 4.9:
        return 2
    elif inputNumber <= 7.9:
        return 3
    elif inputNumber <= 10:
        return 4
    elif inputNumber <= 15:
        return 5
    else:
        return 6


def Tests100K(inputNumber):
    if inputNumber >= 5000:
        return 1
    elif inputNumber >= 3000:
        return 2
    elif inputNumber >= 2000:
        return 3
    elif inputNumber >= 1000:
        return 4
    elif inputNumber >= 500:
        return 5
    else:
        return 6


def BedsOccupied(inputNumber):
    if inputNumber <= 3:
        return 1
    elif inputNumber <= 7:
        return 2
    elif inputNumber <= 12:
        return 3
    elif inputNumber <= 15:
        return 4
    elif inputNumber <= 20:
        return 5
    else:
        return 6


def BedsUCIOccupied(inputNumber):
    if inputNumber <= 3:
        return 1
    elif inputNumber <= 7:
        return 2
    elif inputNumber <= 12:
        return 3
    elif inputNumber <= 15:
        return 4
    elif inputNumber <= 20:
        return 5
    else:
        return 6


def ConvertToScale(inputNumber, target):
    if target == 'confirmedCases100k':
        return CasesPer100K(inputNumber)
    elif target == 'appliedTests100k':
        return Tests100K(inputNumber)
    elif target == 'positivityRate':
        return PositivityRate(inputNumber)
    elif target == 'bedsOccupiedPercentage':
        return BedsOccupied(inputNumber)
    elif target == 'bedsUCIOccupiedPercentage':
        return BedsUCIOccupied(inputNumber)


def getOpenCovidPeruData(date):
    from ..utils.utils import getMonday
    mondayDate = getMonday(date)
    conn = http.client.HTTPSConnection(
        "open-covid-api-vwgk4ckqbq-uk.a.run.app")
    payload = ''
    headers = {}
    conn.request("GET", f"/api/semaforo?fecha={mondayDate}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    jsonData = json.loads(data.decode('utf-8'))
    filteredData = list(map((lambda value: {constantsOpenCovidData['REGION']: value[constantsOpenCovidData['REGION']], constantsOpenCovidData['APPLIEDTESTS']: value[constantsOpenCovidData['APPLIEDTESTS']], constantsOpenCovidData['TEST_POSITIVITY']:  value[constantsOpenCovidData['TEST_POSITIVITY']], constantsOpenCovidData['POPULATION']: value[constantsOpenCovidData['POPULATION']], constantsOpenCovidData['BEDS_OCCUPIED']: value[constantsOpenCovidData['BEDS_OCCUPIED']],
                        constantsOpenCovidData['BEDS_UCI_OCCUPIED']: value[constantsOpenCovidData['BEDS_UCI_OCCUPIED']], constantsOpenCovidData['CONFIRMED_CASES_WEEKLY']: (value[constantsOpenCovidData['POPULATION']]*value[constantsOpenCovidData['CONFIRMED_CASES_WEEKLY']])/100000, constantsOpenCovidData['DEATHS_CASES_WEEKLY']: (value[constantsOpenCovidData['POPULATION']]*value[constantsOpenCovidData['DEATHS_CASES_WEEKLY']])/100000}), jsonData[0][constantsOpenCovidData['REGIONS']]))
    df = pd.DataFrame(filteredData)
    return df


def getProcessedTable(date):
    data = getOpenCovidPeruData(date)
    regions = data[constantsOpenCovidData['REGION']]
    confirmedDeaths100k = (data[constantsOpenCovidData['DEATHS_CASES_WEEKLY']
                                ] / data[constantsOpenCovidData['POPULATION']]) * 10**6
    confirmedCases100k = (data[constantsOpenCovidData['CONFIRMED_CASES_WEEKLY']
                               ] / data[constantsOpenCovidData['POPULATION']]) * 10**6
    appliedTests100k = (data[constantsOpenCovidData['APPLIEDTESTS']] /
                        data[constantsOpenCovidData['POPULATION']]) * 10**6
    positivityRate = (data[constantsOpenCovidData['TEST_POSITIVITY']])
    bedsOccupiedPercentage = (data[constantsOpenCovidData['BEDS_OCCUPIED']])
    bedsUCIOccupiedPercentage = data[constantsOpenCovidData['BEDS_UCI_OCCUPIED']]
    finalDF = pd.concat([regions, confirmedDeaths100k, confirmedCases100k, appliedTests100k, positivityRate, bedsOccupiedPercentage, bedsUCIOccupiedPercentage], axis=1, join='inner', keys=[constantsOpenCovidData['REGIONS'], constantsOpenCovidData['CONFIRMED_DEATHS_100K'],
                        constantsOpenCovidData['CONFIRMED_CASES_100K'], constantsOpenCovidData['APPLIED_TESTS_100K'], constantsOpenCovidData['POSITIVITY_RATE'], constantsOpenCovidData['BEDS_OCCUPIED_PERCENTAGE'], constantsOpenCovidData['BEDS_UCI_OCCUPIED_PERCENTAGE']])
    finalDF = finalDF.round(2)
    return finalDF

def getIndex(city):
    from ..utils.utils import getOffSetTime
    endDate = 196 + getOffSetTime()
    rangeDates = list(range(endDate,0,-7))
    totalIndividual = ''
    currentDF = '' 
    for i in rangeDates:
        try:
            testDf = getProcessedTable(datetime.date.today()-datetime.timedelta(days=i))
            testDf = testDf[testDf[constantsOpenCovidData['REGIONS']] == city]
            del testDf[constantsOpenCovidData['REGIONS']]

            if i == rangeDates[-1]:
                currentDF = testDf

            if i == endDate:
                totalIndividual = testDf
            else:
                totalIndividual = pd.concat([totalIndividual,testDf],ignore_index=True)
        except:
            continue

    correlation_matrix = totalIndividual.corr()
    correlation_matrix_filtered = correlation_matrix['confirmedDeaths100k']
    correlation_matrix_filtered = correlation_matrix_filtered[[1,2,3,4,5]]
    correlation_matrix_filtered = correlation_matrix_filtered/sum(correlation_matrix_filtered)
    correlation_matrix_filtered = pd.DataFrame(correlation_matrix_filtered)
    correlation_matrix_filtered.columns = [city]
    
    weights_table_city = correlation_matrix_filtered
    weights_table_city = weights_table_city.transpose()
    
    totalRisk = 0
    for rate in [constantsOpenCovidData['CONFIRMED_CASES_100K'], constantsOpenCovidData['APPLIED_TESTS_100K'], constantsOpenCovidData['POSITIVITY_RATE'], constantsOpenCovidData['BEDS_OCCUPIED_PERCENTAGE'], constantsOpenCovidData['BEDS_UCI_OCCUPIED_PERCENTAGE']]:
        dataRate = float(currentDF[rate])
        riskNoWeight = ConvertToScale(dataRate,rate)
        factorWeight = float(weights_table_city[rate])
        riskWeighted = factorWeight * riskNoWeight
        totalRisk = totalRisk + riskWeighted
    
    return totalRisk
