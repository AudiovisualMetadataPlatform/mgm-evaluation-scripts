#!/bin/env amp_python.sif

import argparse
from classifier import Classifier as AudioSegmentation
import traceback
from amp.logging import *
import logging
from amp.file_handler import *


setup_logging('audio_segmentation_evaluation', True)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--ground-truth-file", type=str, required=True, help="Ground Truth file path.")
    parser.add_argument("-m", "--mgm-output-file", type=str, required=True, help="MGM output file path.")
    parser.add_argument("-t", "--threshold", type=int, help="Threshold value.")
    parser.add_argument("-u", "--use-case", type=str,  required=True, help="Use Case either we want audio segmentation by segments/seconds.", choices=["by_seconds", "by_segments"])

    args = parser.parse_args()

    if (args.threshold == None or args.threshold == '') and args.use_case  == 'by_segments':
        parser.error("-t requires for Audio Segmentation By Segments")
    
    try:
        filename = get_file_name(args.mgm_output_file)
        scores, output_data = AudioSegmentation(args.use_case).evaluate(args.ground_truth_file, args.mgm_output_file, args.threshold)
        create_csv_from_dict(f"{filename}_scores_{args.use_case}.csv", [scores])
        create_csv_from_dict(f"{filename}_comparison_results_{args.use_case}.csv", output_data)
    except:
        logging.error(traceback.format_exc())