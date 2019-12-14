import json
import csv


def loadMasterData():
    json_list = []
    with open('mst/MstProducts.csv', 'r') as f:
        for row in csv.DictReader(f):
            json_list.append(row)
    return json_list