from amp.file_handler import *
from unique_texts import UniqueText
from metrics import Metrics
import logging

class Classifier():
    def __init__(self, use_case):
        logging.info("Evaluating Video Optical Character Recognition")
        if use_case == 'unique_text':
            self.type = UniqueText()
        self.metrics = Metrics()
    
    def scores(self, cm):
        gt = cm['tp']+cm['fn']
        mgm = cm['tp']+cm['fp']
        scores = {}
        scores['precision'] = self.metrics.precision(cm['tp'], cm['fp'])
        scores['recall'] = self.metrics.recall(cm['tp'], cm['fn'])
        scores['f1'] = self.metrics.f1(cm['tp'], cm['fp'], cm['fn'])
        scores['accuracy'] = self.metrics.accuracy(cm['tp'], gt)
        scores['gt_count'] = len(gt)
        scores['mgm_count'] = len(mgm)
        scores['true_pos'] = len(cm['tp'])
        scores['false_pos'] = len(cm['fp'])
        scores['false_neg'] = len(cm['fn'])
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
        unique_gt = self.uniqueTexts(gt_texts)

        mgm_texts = self.ampJsonToDicts(mgm_output_file)
        unique_mgm = self.uniqueTexts(mgm_texts)

        #get confusion matrix
        cmu = self.type.confusionMatrix(unique_gt, unique_mgm)
        #get counts of each unique text
        cmu_w_counts = self.counts(cmu['combined'], gt_texts, mgm_texts)

        #get scores from confusion matrix
        scores = self.scores(cmu)
        return scores, cmu_w_counts

    def uniqueTexts(self, data):
        unique = list(set([d['text'] for d in data]))
        return unique

    def gtToDicts(self, gt_file):
        gt = read_csv_file(gt_file)
        gt = [g for g in gt]
        return gt