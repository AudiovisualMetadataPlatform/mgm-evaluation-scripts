import argparse
from classifier import Classifier as STT
import traceback
from helper import * 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--ground-truth-file", type=str, required=True, help="Ground Truth file path.")
    parser.add_argument("-m", "--mgm-output-file", type=str, required=True, help="MGM output file path.")
    args = parser.parse_args()
    try:
        filename = fileName(args.mgm_output_file)
        scores, output_data = STT().evaluate(args.ground_truth_file, args.mgm_output_file)
        writeToCsv(filename + '_scores.csv', [scores])
        writeToCsv(filename + '_comparison_results.csv', output_data)
    except:
        logger.error(traceback.format_exc())