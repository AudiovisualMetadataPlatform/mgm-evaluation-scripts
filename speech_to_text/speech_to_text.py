#!/bin/env amp_python.sif

import argparse
from classifier import Classifier as STT
import traceback
from amp.logging import *
import logging
from amp.file_handler import * 
import datetime

setup_logging('speech_to_text_evaluation', True)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--ground-truth-file", type=str, required=True, help="Ground Truth file path.")
    parser.add_argument("-m", "--mgm-output-file", type=str, required=True, help="MGM output file path.")
    parser.add_argument("-o", "--output-file-path", type=str, required=True, help="Test output file path.")
    args = parser.parse_args()
    try:
        current = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename =  get_file_name(args.mgm_output_file) + current + ".json"
        output_path = os.path.join(args.output_file_path, 'speech_to_text')
        stt = STT()
        scores, comparisons = stt.evaluate(args.ground_truth_file, args.mgm_output_file)
        headers = stt.get_headers(comparisons)
        data = {
            "scores": scores,
            "headers": headers,
            "comparison": comparisons
        }
        abs_path = create_json_file(output_path, filename, data)
        print("success:" + abs_path)
    except:
        logging.error(traceback.format_exc())
        print(traceback.format_exc())