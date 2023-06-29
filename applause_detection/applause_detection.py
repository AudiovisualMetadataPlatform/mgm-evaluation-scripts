#!/bin/env amp_python.sif

import argparse
from classifier import Classifier as ApplauseDetection
import traceback
from amp.logging import *
import logging
from amp.file_handler import *
import datetime

setup_logging('applause_detection_evaluation', True)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--ground-truth-file", type=str, required=True, help="Ground Truth file path.")
    parser.add_argument("-m", "--mgm-output-file", type=str, required=True, help="MGM output file path.")
    parser.add_argument("-t", "--threshold", type=int, help="Threshold value.")
    parser.add_argument("-u", "--use-case", type=str,  required=True, help="Use Case either we want applause detection by segments/seconds.", choices=["by_seconds", "by_segments"])
    parser.add_argument("-o", "--output-file-path", type=str, required=True, help="Test output file path.")
    args = parser.parse_args()

    if (args.threshold == None or args.threshold == '') and args.use_case  == 'by_segments':
        parser.error("-t requires for Applause Detection By Segments")
    
    try:
        current = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename =  get_file_name(args.mgm_output_file) + current + ".json"
        output_path = os.path.join(args.output_file_path, 'applause_detection')
        ad = ApplauseDetection(args.use_case)
        scores, comparisons = ad.evaluate(args.ground_truth_file, args.mgm_output_file, args.threshold)
        headers = ad.get_headers(comparisons)
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