import argparse
from mgm_evaluation import MGMEvaluation

categories = [
    'AudioSegmentationBySegments', 
    'AudioSegmentationBySeconds', 
    'SpeechToText', 
    'ApplauseDetectionBySeconds', 
    'ApplauseDetectionBySegments'
    ]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--ground-truth-file", type=str, required=True, help="Ground Truth file path.")
    parser.add_argument("-m", "--mgm-output-file", type=str, required=True, help="MGM output file path.")
    parser.add_argument("-t", "--threshold", type=int, help="Threshold value.")
    parser.add_argument("-c", "--category", type=str,  required=True, help="Evaluation Category.", choices=categories)
    args = parser.parse_args()

    if (args.threshold == None or args.threshold == '') and args.category in ['AudioSegmentationBySegments', 'ApplauseDetectionBySegments']:
        parser.error("-t requires for category {}".format(args.category))
    
    MGMEvaluation().process(args.ground_truth_file,args.mgm_output_file, args.threshold, args.category)