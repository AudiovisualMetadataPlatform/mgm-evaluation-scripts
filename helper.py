import json
import csv
import sys
from datetime import datetime
import time, logging
from os.path import exists

def ampJsonToDicts(amp_json):
    """Convert AMP JSON file to a Python list of dicts in a common evaluation format: start (in seconds), end, label"""
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


def create_logger():
    logger = logging.getLogger('mgm_evaluation')
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('mgm_tests.log')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] %(levelname)8s --- %(message)s ' +
                                  '(%(filename)s:%(lineno)s)',datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

logger = create_logger()

def is_file_existed(file_path):
    if not exists(file_path):
        raise Exception(F"File {file_path} doesn't exists.")
    return True

def readFile(file_path):
    data = ""
    if is_file_existed(file_path):
        with open(file_path, "r") as f:
            data = f.read()
    return data
