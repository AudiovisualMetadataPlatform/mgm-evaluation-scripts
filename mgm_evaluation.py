from audio_segmentation.by_segments import BySegments as ASBySegments
from audio_segmentation.by_seconds import BySeconds as ASBySeconds
from speech_to_text.stt import SpeechToText as STT
from helper import writeToCsv, logger, fileName
import sys, getopt, logging

class MGMEvaluation:
    def process(self, ground_truth_file,mgm_output_file, threshold, category):
        logger.log(logging.INFO, F"{'*'*10} START PROCESSING {'*'*10}")
        logger.log(logging.INFO, F"Ground Truth file: {ground_truth_file}")
        logger.log(logging.INFO, F"MGM output file: {mgm_output_file}")
        logger.log(logging.INFO, F"Category: {category}")
        logger.log(logging.INFO, F"Threshold: {threshold}")
        try:
            filename = fileName(mgm_output_file)
            resultFile = ''
            if category == 'AudioSegmentationBySegments':
                audio_segmentation_by_segments = ASBySegments()
                scores, output_data = audio_segmentation_by_segments.compareFiles(ground_truth_file, mgm_output_file, threshold, gt_offset=0, ignore_gender=True)
                filename += '_by_segments_'
                resultFile = filename + 'matrix'
            elif category == 'AudioSegmentationBySeconds':
                audio_segmentation_by_seconds = ASBySeconds()
                scores, output_data = audio_segmentation_by_seconds.compareFiles(ground_truth_file, mgm_output_file)
                filename += '_by_seconds_'
                resultFile = filename + 'matrix'
            elif category == 'SpeechToText':
                scores, output_data = STT().evaluate(ground_truth_file, mgm_output_file)
                filename += "_"
                resultFile = filename + '_comparison'
            self.generateScoringFile(scores, filename)
            self.generateResultFile(output_data, resultFile)
        except:
            logger.log(logging.ERROR,  F'{sys.exc_info()[0]} exception found')
        logger.log(logging.INFO, F"{'*'*10} END PROCESSING {'*'*10}")

    def generateScoringFile(self, scores, filename):
        scoring_file = filename + 'scores.csv'
        writeToCsv(scoring_file, [scores]) # creating scores file
        logger.log(logging.INFO, F"Score file created: {scoring_file}")
        return scoring_file

    def generateResultFile(self, data, filename):
        result_file = filename + '_results.csv'
        writeToCsv(result_file, data) # creating output result file
        logger.log(logging.INFO, F"Output Result file created: {result_file}")
        return result_file

