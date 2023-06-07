from os import listdir
from os.path import isfile, join
import csv
import json
from lxml import etree

col_names = ["car_model", "year_of_manufacture", "price", "fuel"]
in_path = r"dealership_data"
out_path = "out.csv"


class Printer:

    def __init__(self) -> None:
        self.path = out_path
        f = open(self.path, "w")
        self.writer = csv.DictWriter(f, col_names)
        self.writer.writeheader()
        self.count_dict = {}

    def save_data(self, line: dict):
        line = clean(line)
        match = self.count_dict.get(line['car_model'])
        if match is True:
            self.writer.writerow(line)
        elif match is None:
            self.count_dict[line['car_model']] = {"count": 1, "queue": [line]}
        elif match['count'] < 3:
            self.count_dict[line['car_model']]["count"] += 1
            self.count_dict[line["car_model"]]["queue"].append(line)
        elif match['count'] == 3:
            for line in self.count_dict[line["car_model"]]["queue"]:
                self.writer.writerow(line)
            self.writer.writerow(line)
            self.count_dict[line["car_model"]] = True


printer = Printer()


def clean(line: dict) -> dict:
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


def list_dir(path: str) -> list:
    return [f for f in listdir(path) if isfile(join(path, f))]


def process_data():
    for path in list_dir(in_path):
        match path.split(".")[1]:
            case "csv":
                process_csv(join(in_path, path))
            case "json":
                process_json(join(in_path, path))
            case "xml":
                process_xml(join(in_path, path))
