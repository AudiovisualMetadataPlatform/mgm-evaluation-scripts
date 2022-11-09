#!/bin/env amp_python.sif

import argparse
from classifier import Classifier as STT
import traceback
from amp.logging import *
import logging
from amp.file import * 

setup_logging('speech_to_text_evaluation', True)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--ground-truth-file", type=str, required=True, help="Ground Truth file path.")
    parser.add_argument("-m", "--mgm-output-file", type=str, required=True, help="MGM output file path.")
    args = parser.parse_args()
    try:
        filename = get_file_name(args.mgm_output_file)
        scores, output_data = STT().evaluate(args.ground_truth_file, args.mgm_output_file)
        create_csv_from_dict(filename + '_scores.csv', [scores])
        create_csv_from_dict(filename + '_comparison_results.csv', output_data)
    except:
        logging.error(traceback.format_exc())