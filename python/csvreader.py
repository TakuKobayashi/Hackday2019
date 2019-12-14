import json
import csv
import glob

allData = {}

def loadMasterData():
    json_list = []
    with open('mst/MstProducts.csv', 'r') as f:
        for row in csv.DictReader(f):
            json_list.append(row)
    return json_list

def loadAllFiles():
    file_list = glob.glob('mst/**/*.csv')
    for filename in file_list:
        json_list = []
        with open(filename, 'r') as f:
            for row in csv.DictReader(f):
                json_list.append(row)
        allData[filename] = json_list
