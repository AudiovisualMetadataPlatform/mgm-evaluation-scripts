from classifiers.audio_segmentation.by_segments import BySegments as ASBySegments
from classifiers.audio_segmentation.by_seconds import BySeconds as ASBySeconds
from classifiers.applause_detection.by_segments import BySegments as ADBySegments
from classifiers.applause_detection.by_seconds import BySeconds as ADBySeconds
from classifiers.shot_detection.classifier import Classifier as ShotDetection
from classifiers.named_entity_recognition.classifier import Classifier as NER
from utils.helper import writeToCsv, fileName
import traceback
from utils.helper import logger


class MGMEvaluation:

    def process(self, **kwargs):
        ground_truth_file = kwargs['ground_truth_file']
        mgm_output_file = kwargs['mgm_output_file']
        threshold = kwargs['threshold']
        category = kwargs['category']
        entity_set = kwargs['entity_set']
        tool = kwargs['tool']
        type_match = kwargs['match_types']
        ground_truth_entities = kwargs['ground_truth_entities']
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
            elif category == 'ApplauseDetectionBySegments':
                applause_detection_by_segments = ADBySegments()
                scores, output_data = applause_detection_by_segments.compareFiles(ground_truth_file, mgm_output_file, threshold, gt_offset=0, ignore_gender=True)
                filename += '_by_segments_'
                resultFile = filename + 'matrix'
            elif category == 'ApplauseDetectionBySeconds':
                applause_detection_by_seconds = ADBySeconds()
                scores, output_data = applause_detection_by_seconds.compareFiles(ground_truth_file, mgm_output_file)
                filename += '_by_seconds_'
                resultFile = filename + 'matrix'
            elif category == 'ShotDetection':
                shot_detection = ShotDetection()
                scores, output_data = shot_detection.compareFiles(ground_truth_file, mgm_output_file, threshold)
                filename += '_'
                resultFile = filename + 'comparison'
            elif category in ['NERAllEntityInstancesToolSpecified', 'NERUniqueEntityInstancesToolSpecified', 'NERAllEntityInstancesMapped', 'NERUniqueEntityInstancesMapped']:
                case = 'all_entity_instances_tool_specified'
                if category == 'NERUniqueEntityInstancesToolSpecified':
                    case = 'unique_entity_instances_tool_specified'
                elif category == 'NERAllEntityInstancesMapped':
                    case = 'all_entity_instances_mapped'
                elif category == 'NERUniqueEntityInstancesMapped':
                    case = 'unique_entity_instances_mapped'
                ner = NER(case, entity_set, ground_truth_entities)
                scores, output_data = ner.evaluate(ground_truth_file, mgm_output_file, tool, type_match)
                filename += '_'
                resultFile = filename + 'comparison'
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

