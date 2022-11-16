import logging
from amp.file_handler import *

def ampJsonToDicts(amp_json):
    """Convert AMP JSON file to a Python list of dicts in a common evaluation format: start (in seconds), end, label"""
    logging.info("Convert AMP JSON file to a Python list of dicts in a common evaluation format: start (in seconds), end, label")
    mgm_output_json = read_json_file(amp_json)
    mgm_output = []
    for s in mgm_output_json['segments']:
        seg = {}
        seg['start'] = float(s['start'])
        seg['end'] = float(s['end'])
        seg['label'] = s['label']
        mgm_output.append(seg)
    return mgm_output

def ignoreGender(data):
    logging.info("Update data to ignore gender")
    temp = []
    temp.append(data[0])
    for d in data[1:]:
        if d['label'] == 'speech' and temp[-1]['label'] == 'speech':
            temp[-1]['end'] = d['end']
        else:
            temp.append(d)
    return temp
