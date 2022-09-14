from audio_segmentation.by_segments import BySegments as ASBySegments
from audio_segmentation.by_seconds import BySeconds as ASBySeconds
from helper import writeToCsv, logger
import sys, getopt, logging

def parseArguments(argv):
    ground_truth_file = ''
    mgm_output_file = ''
    threshold = ''
    category = ''
    categories = ['AudioSegmentationBySegments', 'AudioSegmentationBySeconds']
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
        main(ground_truth_file,mgm_output_file, threshold, category)

def main(ground_truth_file,mgm_output_file, threshold, category):
    logger.log(logging.INFO, F"{'*'*10} START PROCESSING {'*'*10}")
    logger.log(logging.INFO, F"Ground Truth file: {ground_truth_file}")
    logger.log(logging.INFO, F"MGM output file: {mgm_output_file}")
    logger.log(logging.INFO, F"Category: {category}")
    logger.log(logging.INFO, F"Threshold: {threshold}")
    try:
        filename = mgm_output_file[0:-5]
        if category == 'AudioSegmentationBySegments':
            audio_segmentation_by_segments = ASBySegments()
            scores = audio_segmentation_by_segments.compareFiles(ground_truth_file, mgm_output_file, threshold, gt_offset=0, ignore_gender=True)
        elif category == 'AudioSegmentationBySeconds':
            audio_segmentation_by_seconds = ASBySeconds()
            scores, confusion_matrix = audio_segmentation_by_seconds.compareFiles(ground_truth_file, mgm_output_file)
            filename += '_by_seconds_'
        scoring_file = filename + 'scores.csv'
        cf_file = filename + 'matrix_results.csv'
        writeToCsv(scoring_file, [scores]) # creating scores file
        logger.log(logging.INFO, F"Score file created: {scoring_file}")
        writeToCsv(cf_file, confusion_matrix) # creating confusion matrix file
        logger.log(logging.INFO, F"Confusion Matrix file created: {cf_file}")
    except:
        logger.log(logging.ERROR,  F'{sys.exc_info()[0]} exception found')
    logger.log(logging.INFO, F"{'*'*10} END PROCESSING {'*'*10}")

if __name__ == '__main__':
    parseArguments(sys.argv[1:])
    # python3 main.py -g gloria-gibson-hudson-segments-gt.csv -m 'for-testing-gloria-gibson-hudson-segments.json' -t 2 -c 'AudioSegmentationBySegments'
    # python3 main.py -g little_500_gt.csv -m little_500_segments.json -c 'AudioSegmentationBySecvd'