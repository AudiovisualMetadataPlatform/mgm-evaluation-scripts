import pytest
import os
from classifier import Classifier as NER

comprehend_gt = os.path.join("sample_data", "sample_aws_gt.csv")
comprehend_mgm = os.path.join("sample_data", "sample_aws.json")


spacy_gt = os.path.join("sample_data", "sample_spacy_gt.csv")
spacy_mgm = os.path.join("sample_data", "sample_spacy.json")


## test all entities with spacy and match types false
def test_case_1():
    use_case = "all_entity_instances_tool_specified"
    tool = "spacy"
    entity_type = None
    match_types = False
    ground_truth_entities = "spacy"
    ner = NER(use_case, entity_type, ground_truth_entities)
    scores, output_data = ner.evaluate(spacy_gt, spacy_mgm, tool, match_types)
    assert scores['precision'] == 0.6571428571428571
    assert scores['recall'] == 0.6388888888888888
    assert scores['f1'] == 0.647887323943662
    assert scores['accuracy'] == 0.6388888888888888
    assert scores['gt_count'] == 72
    assert scores['mgm_count'] == 70
    assert scores['true_pos'] == 46
    assert scores['false_pos'] == 24
    assert scores['false_neg'] == 26


## test unique entity instances with entity set common and match types false
def test_case_2():
    use_case = "unique_entity_instances_mapped"
    tool = None
    match_types = False
    ground_truth_entities = "spacy"
    ner = NER(use_case, None, ground_truth_entities)
    scores, output_data = ner.evaluate(spacy_gt, spacy_mgm, tool, match_types)
    assert scores['precision'] == 0.53125
    assert scores['recall'] == 0.38636363636363635
    assert scores['f1'] == 0.4473684210526316
    assert scores['accuracy'] == 0.38636363636363635
    assert scores['gt_count'] == 44
    assert scores['mgm_count'] == 32
    assert scores['true_pos'] == 17
    assert scores['false_pos'] == 15
    assert scores['false_neg'] == 27

## test unique entity instances with entity set common and match types true failed
def test_case_3():
    use_case = "all_entity_instances_tool_specified"
    tool = "spacy"
    entity_type = None
    match_types = True
    ground_truth_entities = "spacy"
    ner = NER(use_case, entity_type, ground_truth_entities)
    scores, output_data = ner.evaluate(spacy_gt, spacy_mgm, tool, match_types)
    assert scores['precision'] == 0.6142857142857143
    assert scores['recall'] == 0.5972222222222222
    assert scores['f1'] == 0.6056338028169014
    assert scores['accuracy'] == 0.5972222222222222
    assert scores['gt_count'] == 72
    assert scores['mgm_count'] == 70
    assert scores['true_pos'] == 43
    assert scores['false_pos'] == 27
    assert scores['false_neg'] == 29
    
## test unique entity instances with entity set common and match types false, gt file format spacy
def test_case_4():
    use_case = "unique_entity_instances_mapped"
    match_types = False
    ground_truth_entities = "spacy"
    ner = NER(use_case, None, ground_truth_entities)
    scores, output_data = ner.evaluate(spacy_gt, comprehend_mgm, None, match_types)
    assert scores['precision'] == 0.5
    assert scores['recall'] == 0.5454545454545454
    assert scores['f1'] == 0.5217391304347826
    assert scores['accuracy'] == 0.5454545454545454 
    assert scores['gt_count'] == 44
    assert scores['mgm_count'] == 48 
    assert scores['true_pos'] == 24
    assert scores['false_pos'] == 24
    assert scores['false_neg'] == 20

def test_case_5():
    use_case = "all_entity_instances_mapped"
    tool = "comprehend"
    entity_set = None
    match_types = True
    ground_truth_entities = "spacy"
    ner = NER(use_case, entity_set, ground_truth_entities)
    scores, output_data = ner.evaluate(spacy_gt, comprehend_mgm, tool, match_types)
    assert scores['precision'] == 0.46774193548387094
    assert scores['recall'] == 0.4027777777777778
    assert scores['f1'] == 0.4328358208955224
    assert scores['accuracy'] == 0.4027777777777778 
    assert scores['gt_count'] == 72
    assert scores['mgm_count'] == 62
    assert scores['true_pos'] == 29
    assert scores['false_pos'] == 33
    assert scores['false_neg'] == 43

test_case_1()
test_case_2()
test_case_3()
test_case_4()
test_case_5()