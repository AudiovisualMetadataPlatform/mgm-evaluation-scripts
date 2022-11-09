import math
from helper import *
from amp.time_convertor import *
from amp.file_handler import *
import logging

class ADBySeconds():
    def __init__(self, parent):
        logging.info("Evaluating Applause Detection By Seconds")
        self.parent = parent
        pass

    def labelBySecond(self, segments):
        new_list = []
        for s in segments:
            if ':' in str(s['end']):
                start = convertToSeconds(s['start'])
                end = convertToSeconds(s['end'])
            else:
                start = s['start']
                end = s['end']
            num_sec = (math.floor(float(end) - 1) - math.floor(float(start))) +1
            second = math.floor(float(start))
            n = 0
            while n < num_sec:
                lbs = {}
                lbs['second'] = second
                lbs['label'] = s['label']
                new_list.append(lbs)
                second += 1
                n += 1
        return new_list


    def confusionMatrix(self, mgm, gdata):
        logging.info("Generating confusion matrix")
        """Get true positives, false positives, and false negatives"""
        #True positives are counted for every gt second that matches one or more mgm second
        true_pos = []
        #False positives are mgm second that match zero gt seconds
        false_pos = []
        #False negatives are gt seconds that match zero mgm seconds
        false_neg = []
        #iterate through ground truth seconds to find matches with mgm
        for g in gdata:
            for m in mgm:
                if g['second'] == m['second']:
                    if g['label'] == m['label']:
                        tp = {}
                        tp['gt_second'] = g['second']
                        tp['mgm_second'] = m['second']
                        tp['gt_label'] = g['label']
                        tp['mgm_label'] = m['label']
                        tp['comparison'] = 'true_positive'
                        true_pos.append(tp)
                    else:
                        fp = {}
                        fp['mgm_second'] = m['second']
                        fp['gt_second'] = g['second']
                        fp['gt_label'] = g['label']
                        fp['mgm_label'] = m['label']
                        fp['comparison'] = 'false_positive'
                        false_pos.append(fp)
                        fn = {}
                        fn['mgm_second'] = m['second']
                        fn['gt_second'] = g['second']
                        fn['gt_label'] = g['label']
                        fn['mgm_label'] = m['label']
                        fn['comparison'] = 'false_negative'
                        false_neg.append(fn)
        gt_seconds = len(gdata)
        mgm_seconds = len(mgm)
        return (true_pos, false_pos, false_neg, gt_seconds, mgm_seconds)



    def evaluate(self,ground_truth_file, mgm_output_file):
        logging.info("Comparing ground truth and MGM output files")
        """Compare each mgm with the ground truth to get precision, recall, and f1 scores for each 
        and output a spreadsheet with confusion matrix results. Return scores as a dict."""
        all_scores = []

        #read in gt csv files
        gt = read_csv_file(ground_truth_file)
        #convert generator to list
        gt = [g for g in gt]

        #read in mgm json file and convert to list of dicts
        mgm = ampJsonToDicts(mgm_output_file)

        #convert segments to labels by second
        gt = self.labelBySecond(gt)
        mgm = self.labelBySecond(mgm)

        # compare mgm with ground truth to get true positives, false positives, and false negatives
        cf = self.confusionMatrix(mgm, gt)

        #compile the confusion matrix results into a csv file for viewing in a spreadsheet
        matrix_output = cf[0] + cf [1] + cf[2]
        #sort by second
        sorted_mo = sorted(matrix_output, key=lambda k: float(k['mgm_second']))
        #now that the list is sorted, remove the seconds property (they are already represented in gt_second or mgm_second)
        for sm in sorted_mo:
            #convert all the time in seconds to timestamps for easier reading in a spreadsheet
            for k, v in sm.items():
                if k in ['gt_second', 'mgm_second']:
                    sm[k] = convertSecondsToTimestamp(v)
        scores = self.parent.scoring(cf, gt, mgm)
        return scores, sorted_mo

