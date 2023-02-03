from helper import *
from amp.time_convertor import *
import logging

class ASBySegments():
    def __init__(self, parent):
        logging.info("Evaluating Audio Segmentation By Segments")
        self.parent = parent
        pass

    def confusionMatrix(self, mgm, gdata, threshold, gt_offset):
        logging.info("Generating confusion matrix")
        """Get true positives, false positives, and false negatives"""
        #True positives are counted for every gt segment that matches one or more mgm segment
        true_pos = []
        #False positives are mgm segments that match zero gt segments
        false_pos = []
        #False negatives are gt segments that match zero mgm segments
        false_neg = []
        #iterate through ground truth segments to find matches with mgm
        for g in gdata:
            tp = []
            #for each gt segment, iterate through mgm segments to see if segment times match within threshold
            for m in mgm:
                #get the distance between ground truth and mgm start
                s_distance = abs(convertToSeconds(g['start']) - m['start'])
                #get the distance between ground truth and mgm end
                e_distance = abs(convertToSeconds(g['end']) - m['end'])
                #true positive if both start and end are within threshold and labels match
                if s_distance <= threshold and e_distance <= threshold and m['label'] == (g['label']):
                    true_p = {}
                    true_p['gt_start'] = convertToSeconds(g['start']) - gt_offset
                    true_p['gt_end'] = convertToSeconds(g['end']) - gt_offset
                    true_p['start'] = m['start']
                    true_p['end'] = m['end']
                    true_p['s_distance'] = s_distance
                    true_p['e_distance'] = e_distance
                    true_p['label'] = m['label']
                    tp.append(true_p)
            #add match(es) to the true_pos list
            if len(tp) > 0:
                true_pos.extend(tp)
            #add to the false_neg list if not matched
            else:
                false_n = {}
                false_n['gt_start'] = convertToSeconds(g['start']) - gt_offset
                false_n['gt_end'] = convertToSeconds(g['end']) - gt_offset
                #add the start time under 'start' for sorting the timestamps--this will get removed after sorting
                false_n['start'] = convertToSeconds(g['start']) - gt_offset
                false_n['label'] = g['label']
                false_neg.append(false_n)
        #iterate through mgm segments to find any false positives
        for m in mgm:
            fp = True
            for t in true_pos:
                #if it's not already in the true pos list, then it's a false positive
                if t['end'] - gt_offset == m['end']:
                    fp = False
            if fp == True:
                false_pos.append(m.copy())
        for tp in true_pos:
            tp['comparison'] = 'true positive'
        for fp in false_pos:
            fp['comparison'] = 'false positive'
        for fn in false_neg:
            fn['comparison'] = 'false negative'
        gt_counts = len(gdata)
        mgm_counts = len(mgm)
        return (true_pos, false_pos, false_neg, gt_counts, mgm_counts)

    def evaluate(self, ground_truth_file, mgm_output_file, threshold, gt_offset=0, ignore_gender=True):
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

        #if ignore_gender = True, combine all contiguous speech segments
        if ignore_gender == True:
            mgm = ignoreGender(mgm)

        # compare mgm with ground truth to get true positives, false positives, and false negatives
        cf = self.confusionMatrix(mgm, gt, threshold, gt_offset)
        #compile the confusion matrix results into a csv file for viewing in a spreadsheet
        matrix_output = cf[0] + cf [1] + cf[2]
        #sort by start time
        sorted_mo = sorted(matrix_output, key=lambda k: float(k['start']))
        #now that the list is sorted, remove the start and end times for all false negatives (they are already represented in gt_start)
        for sm in sorted_mo:
            if 's_distance' not in sm and 'gt_start' in sm:
                del sm['start']
            #also convert all the time in seconds to timestamps for easier reading in a spreadsheet
            for k, v in sm.items():
                if k in ['gt_start', 'gt_end', 'start', 'end']:
                    sm[k] = convertSecondsToTimestamp(v)
        scores = self.parent.scoring(cf, gt, mgm)
        return scores, sorted_mo