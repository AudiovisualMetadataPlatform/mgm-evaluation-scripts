import metrics
from utils.text_cleanup import *

class SpeechToText:
    def __init__(self):
        self.metrics = metrics.Metrics()

    def evaluate(self, ground_truth_file, mgm_output_file):
        normalized_gt = normalize(ground_truth_file)
        normalized_mgm = normalize(mgm_output_file)
        scores = self.scoring(normalized_gt, normalized_mgm)
        print(scores)

    def scoring(self, normalized_gt, normalized_mgm):
        return {
            "word_error_rate": self.metrics.wordErrorRate(normalized_gt,normalized_mgm),
            "match_error_rate": self.metrics.matchErrorRate(normalized_gt,normalized_mgm),
            "word_info_loss": self.metrics.wordInfoLoss(normalized_gt,normalized_mgm),
            "word_info_processed": self.metrics.wordInfoProcessed(normalized_gt,normalized_mgm),
            "character_error_rate": self.metrics.characterErrorRate(normalized_gt,normalized_mgm)
        }

    