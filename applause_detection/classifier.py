import metrics as metrics
from amp.time_convertor import *
from by_seconds import ADBySeconds
from by_segments import ADBySegments
from amp.file_handler import read_json_file
from itertools import chain

class Classifier:
    def __init__(self, type):
        self.metrics = metrics.Metrics()
        self.type = type
        self.labels = ['applause', 'non-applause']

    def evaluate(self, ground_truth_file, mgm_output_file, threshold=2, gt_offset=0, ignore_gender=True):
        if self.type == "by_seconds":
            return ADBySeconds(self).evaluate(ground_truth_file, mgm_output_file)
        else:
            return ADBySegments(self).evaluate(ground_truth_file, mgm_output_file, threshold, gt_offset=0, ignore_gender=True)


    def accuracyByLabel(self, tp, gt):
        if self.type == 'by_seconds':
            gtbl = self.secondsByLabel(gt, 'GT', 'label')
            tpbl = self.secondsByLabel(tp, 'TP', 'gt_label')
        elif self.type == 'by_segments':
            gtbl = self.segmentsByLabel(gt, 'GT')
            tpbl = self.segmentsByLabel(tp, 'TP')
        accbl = {}
        for l in self.labels:
            accbl_key = 'Accuracy ' + l.capitalize()
            tpbl_key = 'TP ' + l.capitalize()
            gtbl_key = 'GT ' + l.capitalize()
            #create an empty list for label if not in true positives
            if tpbl_key not in tpbl:
                tpbl[tpbl_key] = []
            accbl[accbl_key] = self.metrics.accuracy(tpbl[tpbl_key], gtbl[gtbl_key])
        return accbl

    def secondsByLabel(self, seconds, second_type, label_key):
        """Split out seconds by label into a dict with labels as keys. second type is a string that gets prepended to the key."""
        bl = {}
        for t in seconds:
            if t[label_key] in bl:
                bl[t[label_key]].append(t)
            else:
                bl[t[label_key]] = [t]
        new_bl = {}
        for k, v in bl.items():
            new_k = second_type + ' ' + k.capitalize()
            new_bl[new_k] = v
        return new_bl
    
    def segmentsByLabel(self,segments, segment_type):
        """Split out segments by label into a dict with labels as keys. Segment type is a string that gets prepended to the key."""
        bl = {}
        for t in segments:
            if t['label'] in bl:
                bl[t['label']].append(t)
            else:
                bl[t['label']] = [t]
        new_bl = {}
        for k, v in bl.items():
            new_k = segment_type + ' ' + k.capitalize()
            new_bl[new_k] = v
        return new_bl

    def scoring(self, cf, gt, mgm):
        scores = {}
        scores['Overall Precision'] = self.metrics.precision(cf[0], cf[1])
        scores['Overall Recall'] = self.metrics.recall(cf[0], cf[2])
        scores['Overall F1'] = self.metrics.f1(cf[0], cf[1], cf[2])
        scores['Overall Accuracy'] = self.metrics.accuracy(cf[0], gt)
        scores['Total GT'] = cf[3]
        scores['Total MGM'] = cf[4]
        scores['True Positive'] = len(cf[0])
        scores['False Positive'] = len(cf[1])
        scores['False Negative'] = len(cf[2])
        if self.type == 'by_seconds':
            #add counts of gt by label
            gtbl = self.secondsByLabel(gt, 'GT', 'label')
            for k, v in gtbl.items():
                scores[k] = len(v)
            #add counts of mgm by label
            mgmbl = self.secondsByLabel(mgm, 'MGM', 'label')
            for k, v in mgmbl.items():
                scores[k] = len(v)
            #add counts of true positives by label
            tpbl = self.secondsByLabel(cf[0], 'True Positive', 'gt_label')
            for k, v in tpbl.items():
                scores[k] = len(v)
        elif type == 'by_segments':
            #add counts of gt by label
            gtbl = self.segmentsByLabel(gt, 'GT')
            for k, v in gtbl.items():
                scores[k] = len(v)
            #add counts of mgm by label
            mgmbl = self.segmentsByLabel(mgm, 'MGM')
            for k, v in mgmbl.items():
                scores[k] = len(v)
            #add counts of true positives by label
            tpbl = self.segmentsByLabel(cf[0], 'True Positive')
            for k, v in tpbl.items():
                scores[k] = len(v)
        #get accuracy by label
        accbl = self.accuracyByLabel(cf[0], gt)
        for k, v in accbl.items():
            scores[k] = v
        return scores

    def get_headers(self, comparisons):
        headers = read_json_file('headers.json')
        unique_headers = list(set(chain.from_iterable(sub.keys() for sub in comparisons)))
        output = []
        for header in headers:
            if header['field'] in unique_headers:
                output.append(header)
        return output
