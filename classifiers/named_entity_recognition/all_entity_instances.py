from utils.helper import *

class AllEntityInstances():
    def __init__(self, entity_keys, type, entity_set, ground_truth_entities):
        self.entity_keys = entity_keys
        self.entity_set = entity_set
        self.ground_truth_entities = ground_truth_entities
        self.type = type

    def comparison(self, gt, mgm, tool, types, type_match=False):
        gt = self.ground_truth_values(gt)
        mgm = self.mgm_output_values(mgm)
        if self.type == 'tool_specified':
            return self.tool_specified_comparisons(gt, mgm, tool, types, type_match)
        
    def ground_truth_values(self, filename):
        gt = readCSVFile(filename)
        gt = [g for g in gt]
        for g in gt:
            #convert entity type to corresponding common entity type if entity_set selected is 'common'
            if self.entity_set == 'common':
                g['type'] = self.entity_keys[self.ground_truth_entities][g['type'].upper()]
            #name type and text unique to gt
            g['gt_type'] = g.pop('type')
            g['gt_text'] = g.pop('text')
        return gt

    def mgm_output_values(self, filename):
        mgm = readJSONFile(filename)
        mgm = mgm['entities']
        for m in mgm:
            #convert entity type to corresponding common entity type if entity_set selected is 'common'
            if self.entity_set == 'common':
                m['type'] = self.entity_keys[self.entity_set][m['type'].upper()]
            #name type and text unique to mgm
        for m in mgm:
            m['mgm_type'] = m.pop('type')
            m['mgm_text'] = m.pop('text')
        return mgm

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
                    #if text is a match, check that it matches the character offsets within 3 characters
                    if g['gt_text'].lower() == m['mgm_text'].lower():
                        if (int(g['beginOffset']) - m['beginOffset'] < 10) and (int(g['beginOffset']) - m['beginOffset'] > -10):
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