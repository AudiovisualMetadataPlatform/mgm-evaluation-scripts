import argparse
from mgm_evaluation import MGMEvaluation

categories = [
    'AudioSegmentationBySegments', 
    'AudioSegmentationBySeconds', 
    'SpeechToText', 
    'ApplauseDetectionBySeconds', 
    'ApplauseDetectionBySegments',
    'ShotDetection',
    'NERAllEntityInstancesToolSpecified',
    'NERUniqueEntityInstancesToolSpecified'
    ]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--ground-truth-file", type=str, required=True, help="Ground Truth file path.")
    parser.add_argument("-m", "--mgm-output-file", type=str, required=True, help="MGM output file path.")
    parser.add_argument("-t", "--threshold", type=int, help="Threshold value.")
    parser.add_argument("-c", "--category", type=str,  required=True, help="Evaluation Category.", choices=categories)
    parser.add_argument("--types", type=str, help="Types of Named Entity Recognition")
    parser.add_argument("--tool", type=str, help="MGM Tool used Named Entity Recognition output.", choices=['spacy', 'comprehend'])
    parser.add_argument("--type-match", type=bool, help="Entity or Entity type should match", default=False)

    args = parser.parse_args()
    print(args)

    if (args.threshold == None or args.threshold == '') and args.category in ['AudioSegmentationBySegments', 'ApplauseDetectionBySegments', 'ShotDetection']:
        parser.error("-t requires for category {}".format(args.category))

    if args.category in ['NERAllEntityInstancesToolSpecified'] and (args.tool == None or args.tool == ''):
        parser.error("--tool requires for category {}".format(args.category))
    
    MGMEvaluation().process(**vars(args))