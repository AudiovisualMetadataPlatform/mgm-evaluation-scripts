import metrics as metrics
from amp.file_handler import *
from amp.time_convertor import *
import logging

class Classifier():
    def __init__(self):
        logging.info("Evaluating Shot Detection")
        self.metrics = metrics.Metrics()

    def getConfusionMatrix(self, mgm, gt, threshold, shot_type):
        logging.info("Creating confusion matrix")
        """Get true positives, false positives, and false negatives"""
        #True positives are counted for every gt transition that matches one or more mgm transition
        true_pos = []
        #False positives are mgm transitions that match zero gt transitions
        false_pos = []
        #False negatives are gt transitions that match zero mgm transitions
        false_neg = []
        for g in gt:
            tp = []
            for m in mgm:
            #get the distance between ground truth and mgm transition
                distance = abs(float(g['end']) - float(m['end']))
                if distance <= threshold:
                    true_p = {}
                    true_p['type'] = shot_type
                    true_p['gt_start'] = g['start']
                    true_p['gt_end'] = g['end']
                    true_p['start'] = m['start']
                    true_p['end'] = m['end']
                    true_p['distance'] = distance
                    true_p['transition_type'] = g['transition_type']
                    tp.append(true_p)
            if len(tp) > 0:
            # for t in tp:
            #   t['count'] = len(tp)
                true_pos.extend(tp)
            else:
                false_neg.append(g.copy())
        for m in mgm:
            fp = True
            for t in true_pos:
                if t['end'] == m['end']:
                    fp = False
            if fp == True:
                false_pos.append(m.copy())
        for tp in true_pos:
            tp['comparison'] = 'true positive'
        for fp in false_pos:
            fp['comparison'] = 'false positive'
        for fn in false_neg:
            fn['comparison'] = 'false negative'
        return (true_pos, false_pos, false_neg)

    def countTpTransitions(self, tp, t_type):
        gt_end = []
        for t in tp:
            if t['transition_type'] == t_type:
                gt_end.append(t['gt_end'])
        t_counts = len(list(set(gt_end)))
        return t_counts

    def countTruePos(self, true_pos):
        gt_transitions = list(set([t['gt_end'] for t in true_pos if 'gt_end' in t]))
        #subtract one tp for the end of the file, which will always count as a transition
        tp_count = len(gt_transitions) - 1
        return tp_count

    def evaluate(self, gtfile, mgmfile, threshold):
        """Compare each mgm with the ground truth to get precision, recall, and f1 scores
        and output a csv file with confusion matrix results. Output scores as a csv file."""
        logging.info("Comparing ground truth and MGM output files")
        shot_type='shot'
        gt = csv.DictReader(open(gtfile, 'r'))
        gt = [g for g in gt]
        #covert timestamps to seconds
        for g in gt:
            for k, v in g.items():
                if k in ['start', 'end']:
                    g[k] = convertToSeconds(v)
        gtcount = len(gt) - 1

        mgm = json.load(open(mgmfile, 'r'))
        mgm = mgm['shots']
        mgmcount = len(mgm) - 1

        # compare mgm with ground truth to get true positives, false positives, and false negatives
        cf = self.getConfusionMatrix(mgm, gt, threshold, shot_type)

        #compile the confusion matrix results into a csv file for viewing in a spreadsheet
        matrix_output = []
        for c in cf:
            for row in c:
                matrix_output.append(row)

        #sort by transition time
        sorted_mo = sorted(matrix_output, key=lambda k: float(k['end'])) 
        #move false negatives to gt_ columns for cleaner display
        for s in sorted_mo:
            if s['comparison'] == 'false negative':
                s['gt_start'] = s['start']
                s['start'] = ''
                s['gt_end'] = s['end']
                s['end'] = ''
            for k,v in s.items():
                if k in ['gt_start', 'gt_end', 'end', 'start'] and v != '':
                    s[k] = convertSecondsToTimestamp(v)
        #get scores
        scores = {}
        scores['threshold'] = threshold
        scores['precision'] = self.metrics.precision(self.countTruePos(cf[0]), cf[1])
        scores['recall'] = self.metrics.recall(self.countTruePos(cf[0]),cf[2])
        scores['f1'] = self.metrics.f1(self.countTruePos(cf[0]), cf[1], cf[2])
        scores['gt_count'] = gtcount
        scores['mgm_count'] = mgmcount
        scores['true_pos'] = self.countTruePos(cf[0])
        scores['false_pos'] = len(cf[1])
        scores['false_neg'] = len(cf[2])
        scores['cut'] = self.countTpTransitions(cf[0], 'cut')
        scores['dissolve'] = self.countTpTransitions(cf[0], 'dissolve')
        scores['lighting change'] = self.countTpTransitions(cf[0], 'lighting change')
        scores['panning'] = self.countTpTransitions(cf[0], 'panning')
        scores['zoom'] = self.countTpTransitions(cf[0], 'zoom in') + self.countTpTransitions(cf[0], 'zoom out')
        if sorted_mo[-1]['comparison'] == 'true positive':
            scores[sorted_mo[-1]['transition_type']] -= 1

        return scores, sorted_mo


    