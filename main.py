from utils.helper import writeToCsv, logger
import sys, getopt, logging
from mgm_evaluation import MGMEvaluation

def parseArguments(argv):
    ground_truth_file = ''
    mgm_output_file = ''
    threshold = ''
    category = ''
    categories = ['AudioSegmentationBySegments', 'AudioSegmentationBySeconds', 'SpeechToText']
    try:
        opts, args = getopt.getopt(argv,"hm:t:g:c:",["ground-truth-file=","mgm-output-file=", "threshold=", "category="])
    except getopt.GetoptError as e:
        logger.log(logging.ERROR, e)
        print('main.py -g <groundTruthFile> -m <mgmOutputFile> -c <category> -t <threshold>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Options available:')
            print('-g\t--ground-truth-file\tGround Truth file path.')
            print('-m\t--mgm-output-file\tMGM output file path.')
            print('-t\t--threshold\t\tThreshold value.')
            print('-c\t--category\t\tEvaluation Category.')
            sys.exit()
        elif opt in ("-g", "--ground-truth-file"):
            ground_truth_file = arg
        elif opt in ("-m", "--mgm-output-file"):
            mgm_output_file = arg
        elif opt in ("-t", "--threshold"):
            threshold = int(arg)
        elif opt in ("-c", "--category"):
            category = arg
        else:
            print(F"Invalid option {opt} run -h to check available options.")
    if ground_truth_file == '':
        logger.log(logging.ERROR, "Ground Truth file is required")
    elif mgm_output_file == '':
        logger.log(logging.ERROR, "MGM output file is required.")
    elif threshold == '' and category in ['AudioSegmentationBySegments']:
        logger.log(logging.ERROR, "Threshold is required.")
    elif category == '' or category not in categories:
        logger.log(logging.ERROR, "Category is required. Valid categories are {}".format(", ".join(categories)))
    else:
        MGMEvaluation().process(ground_truth_file,mgm_output_file, threshold, category)

if __name__ == '__main__':
    parseArguments(sys.argv[1:])