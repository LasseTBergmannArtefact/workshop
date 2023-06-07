from os import listdir
from os.path import isfile, join
import csv
import json
from lxml import etree

col_names = ["car_model", "year_of_manufacture", "price", "fuel"]
out_path = "out.csv"


class Printer:

    def __init__(self) -> None:
        self.path = out_path
        f = open(self.path, "w")
        self.writer = csv.DictWriter(f, col_names)
        self.writer.writeheader()
        self.count_dict = {}

    def save_data(self, data: dict):
        data = clean(data)
        match = self.count_dict.get(data['car_model'])
        if match is True:
            self.writer.writerow(data)
        elif match is None:
            self.count_dict[data['car_model']] = {"count": 1, "queue": [data]}
        elif match['count'] < 3:
            self.count_dict[data['car_model']]["count"] += 1
            self.count_dict[data["car_model"]]["queue"].append(data)
        elif match['count'] == 3:
            for line in self.count_dict[data["car_model"]]["queue"]:
                self.writer.writerow(line)
            self.count_dict[data["car_model"]] = True


printer = Printer()


def clean(line: dict) -> dict:
    print(line)
    line["price"] = round(float(line["price"]), 2)
    return line


def process_csv(path: str):
    with open(path, "r") as csvfile:
        for line in csv.reader(csvfile):
            if line[0] == 'car_model':
                continue
            printer.save_data({col_names[i]: line[i] for i in range(len(col_names))})


def process_json(path: str):
    with open(path) as jsonfile:
        for line in jsonfile:
            printer.save_data(dict(json.loads(line)))


def process_xml(path: str):
    for child in etree.parse(path).getroot():
        printer.save_data({x.tag: x.text for x in child})


def process_data():
    mypath = r"dealership_data"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    for path in onlyfiles:
        match path.split(".")[1]:
            case "csv":
                process_csv(join(mypath, path))
            case "json":
                process_json(join(mypath, path))
            case "xml":
                process_xml(join(mypath, path))
