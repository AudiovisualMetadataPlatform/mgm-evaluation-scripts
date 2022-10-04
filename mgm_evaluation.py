from classifiers.audio_segmentation.by_segments import BySegments as ASBySegments
from classifiers.audio_segmentation.by_seconds import BySeconds as ASBySeconds
from classifiers.speech_to_text.stt import SpeechToText as STT
from utils.helper import writeToCsv, fileName
import traceback
from utils.helper import logger


class MGMEvaluation:

    def process(self, ground_truth_file,mgm_output_file, threshold, category):
        logger.info(f"{'*'*10} START PROCESSING {'*'*10}")
        logger.info(f"Ground Truth file: {ground_truth_file}")
        logger.info(f"MGM output file: {mgm_output_file}")
        logger.info(f"Category: {category}")
        logger.info(f"Threshold: {threshold}")
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
            logger.error(traceback.format_exc())
        logger.info(f"{'*'*10} END PROCESSING {'*'*10}")

    def generateScoringFile(self, scores, filename):
        scoring_file = filename + 'scores.csv'
        writeToCsv(scoring_file, [scores]) # creating scores file
        logger.info(f"Score file created: {scoring_file}")
        return scoring_file

    def generateResultFile(self, data, filename):
        result_file = filename + '_results.csv'
        writeToCsv(result_file, data) # creating output result file
        logger.info(f"Output Result file created: {result_file}")
        return result_file

