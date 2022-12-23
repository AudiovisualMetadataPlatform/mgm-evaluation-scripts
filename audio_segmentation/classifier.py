import metrics as metrics
from amp.time_convertor import *
from by_seconds import ASBySeconds
from by_segments import ASBySegments

class Classifier:
    def __init__(self, type):
        self.metrics = metrics.Metrics()
        self.type = type
        self.labels = ['silence', 'speech', 'music', 'noise']

    def evaluate(self, ground_truth_file, mgm_output_file, threshold=2, gt_offset=0, ignore_gender=True):
        if self.type == "by_seconds":
            return ASBySeconds(self).evaluate(ground_truth_file, mgm_output_file)
        else:
            return ASBySegments(self).evaluate(ground_truth_file, mgm_output_file, threshold, gt_offset=0, ignore_gender=True)


    def accuracyByLabel(self, tp, gt):
        if self.type == 'by_seconds':
            gtbl = self.secondsByLabel(gt, 'gt', 'label')
            tpbl = self.secondsByLabel(tp, 'tp', 'gt_label')
        elif self.type == 'by_segments':
            gtbl = self.segmentsByLabel(gt, 'gt')
            tpbl = self.segmentsByLabel(tp, 'tp')
        accbl = {}
        for l in self.labels:
            accbl_key = 'accuracy_' + l
            tpbl_key = 'tp_' + l
            gtbl_key = 'gt_' + l
            #create an empty list for label if not in true positives
            if tpbl_key not in tpbl:
                tpbl[tpbl_key] = []
            if gtbl_key in gtbl.keys():
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
            new_k = second_type.replace(' ', '_') + '_' + k
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
            new_k = segment_type.replace(' ', '_') + '_' + k
            new_bl[new_k] = v
        return new_bl

    def scoring(self, cf, gt, mgm):
        scores = {}
        scores['precision'] = self.metrics.precision(cf[0], cf[1])
        scores['recall'] = self.metrics.recall(cf[0], cf[2])
        scores['f1'] = self.metrics.f1(cf[0], cf[1], cf[2])
        scores['accuracy'] = self.metrics.accuracy(cf[0], gt)
        scores['gt_count'] = cf[3]
        scores['mgm_count'] = cf[4]
        scores['true_pos'] = len(cf[0])
        scores['false_pos'] = len(cf[1])
        scores['false_neg'] = len(cf[2])
        if self.type == 'by_seconds':
            #add counts of gt by label
            gtbl = self.secondsByLabel(gt, 'gt', 'label')
            for k, v in gtbl.items():
                scores[k] = len(v)
            #add counts of mgm by label
            mgmbl = self.secondsByLabel(mgm, 'mgm', 'label')
            for k, v in mgmbl.items():
                scores[k] = len(v)
            #add counts of true positives by label
            tpbl = self.secondsByLabel(cf[0], 'true_pos', 'gt_label')
            for k, v in tpbl.items():
                scores[k] = len(v)
        elif type == 'by_segments':
            #add counts of gt by label
            gtbl = self.segmentsByLabel(gt, 'gt')
            for k, v in gtbl.items():
                scores[k] = len(v)
            #add counts of mgm by label
            mgmbl = self.segmentsByLabel(mgm, 'mgm')
            for k, v in mgmbl.items():
                scores[k] = len(v)
            #add counts of true positives by label
            tpbl = self.segmentsByLabel(cf[0], 'true_pos')
            for k, v in tpbl.items():
                scores[k] = len(v)
        #get accuracy by label
        accbl = self.accuracyByLabel(cf[0], gt)
        for k, v in accbl.items():
            scores[k] = v
        return scores
