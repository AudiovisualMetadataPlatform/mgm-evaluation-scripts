import json
import csv
import sys, os
from datetime import datetime
import time, logging
from os.path import exists
from pathlib import Path
from .logs import Logs
from itertools import groupby

logger = Logs()
def ampJsonToDicts(amp_json):
    """Convert AMP JSON file to a Python list of dicts in a common evaluation format: start (in seconds), end, label"""
    logger.info("Convert AMP JSON file to a Python list of dicts in a common evaluation format: start (in seconds), end, label")
    mgm_output_json = json.load(open(amp_json))
    mgm_output = []
    for s in mgm_output_json['segments']:
        seg = {}
        seg['start'] = float(s['start'])
        seg['end'] = float(s['end'])
        seg['label'] = s['label']
        mgm_output.append(seg)
    return mgm_output

def ignoreGender(data):
    logger.info("Update data to ignore gender")
    temp = []
    temp.append(data[0])
    for d in data[1:]:
        if d['label'] == 'speech' and temp[-1]['label'] == 'speech':
            temp[-1]['end'] = d['end']
        else:
            temp.append(d)
    return temp

def convertToTime(timestamp, format):
    try:
        timeobj = datetime.strptime(timestamp, format)
    except:
        timestamp = timestamp + '.0'
        timeobj = datetime.strptime(timestamp, format)
    return timeobj

def convertToSeconds(timestamp, format='%H:%M:%S.%f'):
    """Convert timestamp to seconds if not already in seconds"""
    if ':' in timestamp:
        timeobj = convertToTime(timestamp, format)
        zerotime = convertToTime('0:00:00.000', format)
        timeinseconds = float((timeobj - zerotime).total_seconds())
    else:
        timeinseconds = float(timestamp)
    return timeinseconds

def convertSecondsToTimestamp(seconds):
    timestamp = time.strftime('%H:%M:%S', time.gmtime(seconds))
    return timestamp


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


def readCSVFile(filename):
    logger.info(f"Reading CSV file {filename}")
    if is_file_existed(filename):
        return csv.DictReader(open(filename, 'r'))
    else:
        raise Exception(f"File {filename} not found!!")

def readJSONFile(filename):
    logger.info(f"Reading JSON file {filename}")
    if is_file_existed(filename):
        return json.load(open(filename, 'r'))
    else:
        raise Exception(f"File {filename} not found!!")

def canonicalize_dict(x):
    "Return a (key, value) list sorted by the hash of the key"
    return sorted(x.items(), key=lambda x: hash(x[0]))

def unique_and_count(lst):
    "Return a list of unique dicts with a 'count' key added"
    grouper = groupby(sorted(map(canonicalize_dict, lst)))
    return [dict(k + [("count", len(list(g)))]) for k, g in grouper]
