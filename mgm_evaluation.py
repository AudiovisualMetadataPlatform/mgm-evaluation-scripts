from audio_segmentation.by_segments import BySegments as ASBySegments
from audio_segmentation.by_seconds import BySeconds as ASBySeconds
from speech_to_text.stt import SpeechToText as STT
from helper import writeToCsv, logger
import sys, getopt, logging

class MGMEvaluation:
    def process(self, ground_truth_file,mgm_output_file, threshold, category):
        logger.log(logging.INFO, F"{'*'*10} START PROCESSING {'*'*10}")
        logger.log(logging.INFO, F"Ground Truth file: {ground_truth_file}")
        logger.log(logging.INFO, F"MGM output file: {mgm_output_file}")
        logger.log(logging.INFO, F"Category: {category}")
        logger.log(logging.INFO, F"Threshold: {threshold}")
        # try:
        #     filename = mgm_output_file[0:-5]
        if category == 'AudioSegmentationBySegments':
            audio_segmentation_by_segments = ASBySegments()
            scores, confusion_matrix = audio_segmentation_by_segments.compareFiles(ground_truth_file, mgm_output_file, threshold, gt_offset=0, ignore_gender=True)
            filename += '_by_segments_'
        elif category == 'AudioSegmentationBySeconds':
            audio_segmentation_by_seconds = ASBySeconds()
            scores, confusion_matrix = audio_segmentation_by_seconds.compareFiles(ground_truth_file, mgm_output_file)
            filename += '_by_seconds_'
        elif category == 'SpeechToText':
            STT().evaluate(ground_truth_file, mgm_output_file)
            # scoring_file = filename + 'scores.csv'
            # cf_file = filename + 'matrix_results.csv'
            # writeToCsv(scoring_file, [scores]) # creating scores file
            # logger.log(logging.INFO, F"Score file created: {scoring_file}")
            # writeToCsv(cf_file, confusion_matrix) # creating confusion matrix file
            # logger.log(logging.INFO, F"Confusion Matrix file created: {cf_file}")
        # except:
        #     logger.log(logging.ERROR,  F'{sys.exc_info()[0]} exception found')
        logger.log(logging.INFO, F"{'*'*10} END PROCESSING {'*'*10}")