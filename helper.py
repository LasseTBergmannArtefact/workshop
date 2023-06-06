from os import listdir
from os.path import isfile, join
import csv
import json
from lxml import etree

col_names = ["car_model", "year_of_manufacture", "price", "fuel"]


def clean(list: list) -> list:
    for line in list:
        line["price"] = round(float(line["price"]), 2)
    return list


def read_csv(path: str) -> list:
    with open(path, "r") as csvfile:
        return [{col_names[i]:x[i] for i in range(len(col_names))} for x in csv.reader(csvfile)][1:]


def read_json(path: str) -> list:
    with open(path) as jsonfile:
        return [dict(json.loads(line)) for line in jsonfile]


def read_xml(path: str) -> list:
    return [{x.tag: x.text for x in child} for child in etree.parse(path).getroot()]


def read_data() -> list:
    mypath = r"dealership_data"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    data = []
    for path in onlyfiles:
        match path.split(".")[1]:
            case "csv":
                data.extend(clean(read_csv(join(mypath, path))))
            case "json":
                data.extend(clean(read_json(join(mypath, path))))
            case "xml":
                data.extend(clean(read_xml(join(mypath, path))))
    return data


def save_data(data: list):
    with open("out.csv", "w") as f:
        writer = csv.DictWriter(f, col_names)
        writer.writeheader()
        for dict in data:
            writer.writerow(dict)
