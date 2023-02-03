import os
from metrics import Metrics
from all_entity_instances import AllEntityInstances 
from unique_entity_instances import UniqueEntityInstances 
from amp.file_handler import *
from itertools import chain

class Classifier():
    def __init__(self, test_case, entity_types, ground_truth_entities):
        self.entity_keys = read_json_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entity_keys.json"))
        self.metrics = Metrics()
        self.entity_types = entity_types
        if test_case == 'all_entity_instances_tool_specified':
            self.instance = AllEntityInstances(self.entity_keys, 'tool_specified', ground_truth_entities)
        elif test_case == 'unique_entity_instances_tool_specified':
            self.instance = UniqueEntityInstances(self.entity_keys, 'tool_specified', ground_truth_entities)
        elif test_case == 'all_entity_instances_mapped':
            self.instance = AllEntityInstances(self.entity_keys, 'mapped', ground_truth_entities)
        elif test_case == 'unique_entity_instances_mapped':
            self.instance = UniqueEntityInstances(self.entity_keys, 'mapped', ground_truth_entities)
        

    def evaluate(self, ground_truth_file, mgm_output_file, tool, type_match=False):
        types = []
        if self.entity_types != None  and self.entity_types != '':
            types = self.entity_types.split(",")
        comparisons = self.instance.evaluate(ground_truth_file, mgm_output_file, tool, types, type_match)
        scores = self.scores(comparisons)
        return scores, comparisons['tp'] + comparisons['fp'] + comparisons['fn']

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

    def get_headers(self, comparisons):
        headers = read_json_file('headers.json')
        unique_headers = list(set(chain.from_iterable(sub.keys() for sub in comparisons)))
        output = []
        for header in headers:
            if header['field'] in unique_headers:
                output.append(header)
        return output
