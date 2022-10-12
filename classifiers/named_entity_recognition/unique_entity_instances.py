from utils.helper import *

class UniqueEntityInstances():
    def __init__(self, entity_keys, type):
        self.entity_keys = entity_keys
        self.type = type

    def comparison(self, gt, mgm, tool, types, type_match=False):
        gt = self.ground_truth_values(gt, tool, types)
        mgm = self.mgm_output_values(mgm, tool, types)
        if self.type == 'tool_specified':
            return self.tool_specified_comparisons(gt, mgm, tool, types, type_match)

    def ground_truth_values(self, filename, tool, types):
        gt = readCSVFile(filename)
        new_gt = []
        for g in gt:
            if len(types) == 0:
                types = [k for k, v in self.entity_keys[tool].items()]
                types = [t.upper() for t in types]
            if g['type'].upper() in types:
                new_g = {}
                #uppercase entity types in case they are not already upper
                new_g['gt_type'] = g['type'].upper()
                #name type and text unique to gt
                new_g['gt_text'] = g['text']
                new_gt.append(new_g)
        #get unique list of dicts and counts
        unique_gt = unique_and_count(new_gt)
        for u in unique_gt:
            u['gt_count'] = u.pop('count')
        return unique_gt

    def mgm_output_values(self, filename, tool, types):
        mgm = readJSONFile(filename)
        mgm = mgm['entities']
        new_mgm = []
        if len(types) == 0:
            types = [k for k, v in self.entity_keys[tool].items()]
            types = [t.upper() for t in types]
        #name type and text unique to mgm
        for m in mgm:
            if m['type'].upper() in types:
                new_m = {}
                new_m['mgm_type'] = m['type'].upper()
                new_m['mgm_text'] = m['text']
                new_mgm.append(new_m)
        #get unique list of dicts and counts
        unique_mgm = unique_and_count(new_mgm)
        for u in unique_mgm:
            u['mgm_count'] = u.pop('count')
        return unique_mgm

    def tool_specified_comparisons(self, gt, mgm, tool, types, type_match=False):
        """Takes the ground truth and MGM for a document and gets the confusion matrix based on tool selected and entity types specified"""
        true_pos = []
        false_neg = []
        false_pos = []
        total_gt = 0
        total_mgm = 0
        if len(types) == 0:
            types = [k for k, v in self.entity_keys[tool].items()]
        types = [t.upper() for t in types]
        #compare each gt term with each mgm to determine if tp or fn
        for g in gt:
            if g['gt_type'] in types:
                #track number of relevant gt entities
                total_gt += 1
                for m in mgm:
                    if g['gt_text'].lower() == m['mgm_text'].lower():
                    #track number of relevant mgm entities
                    #if types match OR if type_match is False, then count as tp even if entity types don't match
                        if g['gt_type'] == m['mgm_type'] or type_match == False:
                            tp = {}
                            tp['comparison'] = 'true positive'
                            g['comparison'] = 'true positive'
                            if g['gt_type'] == m['mgm_type']:
                                tp['text_and_type'] = True
                            else:
                                tp['text_and_type'] = False
                            total_mgm += 1
                            tp.update(g)
                            tp.update(m)
                            m['comparison'] = 'true positive'
                            true_pos.append(tp)
                        #if you require entity types to match then only count as tp if type matches
                        elif g['gt_type'] == m['mgm_type'] and type_match == True:
                            tp = {}
                            tp['comparison'] = 'true positive'
                            g['comparison'] = 'true positive'
                            tp['text_and_type'] = True
                            total_mgm += 1
                            tp.update(g)
                            tp.update(m)
                            m['comparison'] = 'true positive'
                            true_pos.append(tp)
                    #if no match then count the gt as a false negative
                if 'comparison' not in g:
                    g['comparison'] = 'false negative'
                    fn = g
                    false_neg.append(fn)
    #compare ml to gt to find false positives
        for m in mgm:
            if 'comparison' not in m:
                if m['mgm_type'] in types:
                    total_mgm += 1
                    m['comparison'] = 'false positive'
                    fp = m
                    false_pos.append(fp)
        return {'tp':true_pos, 'fn':false_neg, 'fp':false_pos}