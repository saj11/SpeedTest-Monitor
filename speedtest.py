from csv import writer as csvWriter
from datetime import date
from matplotlib import pyplot as plt
import numpy as np
from os import path
from pandas import read_csv


relevantKeys = ["Network:", "Date:", "Download:"]
csvHeader = ["month", "day", "time", "year", "downloadNumber", "measure"]
newTestSymbol = "="
columsName = {"month":0, "day":1, "time":2, "year":3, "downloadNumber":4, "measure":5}

def getCurrentDay():
    today = date.today()
    return int(today.strftime("%d"))

def cleanFile(fileName):
    open(fileName, "w").close()

def cleanNetwork(network):
    return [network[0]] if len(network) == 1 else [''.join(network)]

def cleanDate(date):
    dateElements = date[1:3]
    dateElements.append(':'.join(date[3].split(':')[:-1]))
    dateElements.append(date[5])
    return dateElements

def isNewTest(text):
    return True if newTestSymbol in text else False

def readSpeedTestHistory(fileName):
    file = open(fileName, 'r')
    data = file.readlines()
    file.close()
    cleanFile(fileName)
    return data

def parseData(data):
    csvLine = []
    for line in data:
        if isNewTest(line):
            createCSV(csvLine)
            csvLine = []
        
        information = line[:-1].split(' ')
        relevantData = getRelevantData(information)
        if relevantData: csvLine.extend(relevantData)
            
def getRelevantData(information):
    if information[0] in relevantKeys:
        if information[0] == "Network:": return cleanNetwork(information[1:])
        elif information[0] == "Date:": return cleanDate(information[1:])
        elif information[0] == "Download:": return information[1:]

def createCSV(csvLine):
    fileMode = ''
    newFile = False
    fileName = '{}.csv'.format(csvLine[0])
    if not path.exists(fileName):
        fileMode = 'w+'
        newFile = True
    else: fileMode = 'a'

    with open(fileName, fileMode, newline='') as file:
        writer = csvWriter(file)
        
        if newFile: writer.writerow(csvHeader)

        writer.writerow(csvLine[1:])
    
def createChart(fileName, xName, yName):
    day = getCurrentDay()
    series = read_csv(fileName).values
    series = np.array(list(filter(lambda array: array[1] == day , series)))

    x = np.array(series[:,csvHeader.index(xName)])
    y = np.array(series[:,csvHeader.index(yName)])

    plt.title("Speed Test History")
    plt.xlabel(xName)
    plt.ylabel(yName)
    plt.grid(True)
    
    plt.plot(x, y)
    plt.show()
    

file = readSpeedTestHistory('speedTestHistory.txt')
if len(file) > 0 : parseData(file)
createChart("FamSalazar.csv", "time", "downloadNumber")
