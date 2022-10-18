from utils.helper import *
from classifiers.metrics import Metrics
from .all_entity_instances import AllEntityInstances 
from .unique_entity_instances import UniqueEntityInstances 

class Classifier():
    def __init__(self, test_case, entity_set, ground_truth_entities):
        self.entity_keys = readJSONFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entity_keys.json"))
        self.metrics = Metrics()
        if test_case == 'all_entity_instances_tool_specified':
            self.instance = AllEntityInstances(self.entity_keys, 'tool_specified', entity_set, ground_truth_entities)
        elif test_case == 'unique_entity_instances_tool_specified':
            self.instance = UniqueEntityInstances(self.entity_keys, 'tool_specified', entity_set, ground_truth_entities)
        elif test_case == 'all_entity_instances_mapped':
            self.instance = AllEntityInstances(self.entity_keys, 'mapped', entity_set, ground_truth_entities)
        elif test_case == 'unique_entity_instances_mapped':
            self.instance = UniqueEntityInstances(self.entity_keys, 'mapped', entity_set, ground_truth_entities)
        

    def evaluate(self, ground_truth_file, mgm_output_file, tool, type_match=False):
        types = []
        comparisons = self.instance.evaluate(ground_truth_file, mgm_output_file, tool, types, type_match)
        scores = self.scores(comparisons)
        return scores, comparisons['tp'] + comparisons['fp'] + comparisons['fn']

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