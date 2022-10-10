import csv
from os.path import exists
from pathlib import Path
from logs import Logs

logger = Logs()

def writeToCsv(filename, data):
    logger.info(f"Creating file {filename}")
    longestlen = 0
    longestlenindex = 0
    for i, t in enumerate(data):
        if len(t) > longestlen:
            longestlen = len(t)
            longestlenindex = i
    if len(data[longestlenindex]) > 0:
        fieldnames = data[longestlenindex].keys()
    writer = csv.DictWriter(open(filename, 'w'), fieldnames=fieldnames)
    writer.writeheader()
    for d in data:
        writer.writerow(d)
    logger.info(f"File created: {filename}")

def is_file_existed(file_path):
    logger.info(f"Checking if file {file_path} existed.")
    if not exists(file_path):
        raise Exception(F"File {file_path} doesn't exists.")
    return True

def readFile(file_path):
    logger.info(f"Reading file {file_path}")
    data = ""
    if is_file_existed(file_path):
        with open(file_path, "r") as f:
            data = f.read()
    return data

def fileName(file_path):
    return Path(file_path).stem
