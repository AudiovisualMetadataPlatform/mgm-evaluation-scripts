from amp.file_handler import *
from text import Text
from metrics import Metrics
import logging,os
from itertools import chain

class Classifier():
    def __init__(self, use_case):
        logging.info("Evaluating Video Optical Character Recognition")
        if use_case == 'unique_text':
            self.type = Text('unique')
        elif use_case == 'each_text':
            self.type = Text('each')

        self.metrics = Metrics()
    
    def scores(self, cm):
        gt = cm['tp']+cm['fn']
        mgm = cm['tp']+cm['fp']
        scores = {}
        scores['Overall Precision'] = self.metrics.precision(cm['tp'], cm['fp'])
        scores['Overall Recall'] = self.metrics.recall(cm['tp'], cm['fn'])
        scores['Overall F1'] = self.metrics.f1(cm['tp'], cm['fp'], cm['fn'])
        scores['Overall Accuracy'] = self.metrics.accuracy(cm['tp'], gt)
        scores['Total GT'] = len(gt)
        scores['Total MGM'] = len(mgm)
        scores['True Positive'] = len(cm['tp'])
        scores['False Positive'] = len(cm['fp'])
        scores['False Negative'] = len(cm['fn'])
        return scores

    def counts(self, cmu_combined, gt, mgm):
        gt = [g['text'] for g in gt]
        mgm = [m['text'] for m in mgm]
        for c in cmu_combined:
            c['gt_counts'] = gt.count(c['text'])
            c['mgm_counts'] = mgm.count(c['text'])
        return cmu_combined

    def ampJsonToDicts(self, amp_json):
        """Convert AMP JSON file to a Python list of dicts"""
        mgm_output_json = read_json_file(amp_json)
        mgm_output = []
        for f in mgm_output_json['frames']:
            for o in f['objects']:
                obj = {}
                obj['start'] = float(f['start'])
                obj['text'] = o['text']
                mgm_output.append(obj)
        return mgm_output

    def evaluate(self, ground_truth_file, mgm_output_file):
        logging.info("Comparing ground truth and MGM output files")
        gt_texts = self.gtToDicts(ground_truth_file)
        mgm_texts = self.ampJsonToDicts(mgm_output_file)
        #get confusion matrix
        cmu = self.type.confusionMatrix(gt_texts, mgm_texts)
        #get counts of each unique text
        cmu_w_counts = self.counts(cmu['combined'], gt_texts, mgm_texts)
        #get scores from confusion matrix
        scores = self.scores(cmu)
        return scores, cmu_w_counts

    def gtToDicts(self, gt_file):
        gt = read_csv_file(gt_file)
        gt = [g for g in gt]
        return gt

    def get_headers(self, comparisons):
        current_file_path = os.path.abspath(__file__)
        current_file_directory = os.path.dirname(current_file_path)
        headers = read_json_file(os.path.join(current_file_directory, "headers.json"))
        unique_headers = list(set(chain.from_iterable(sub.keys() for sub in comparisons)))
        output = []
        for header in headers:
            if header['field'] in unique_headers:
                output.append(header)
        return output