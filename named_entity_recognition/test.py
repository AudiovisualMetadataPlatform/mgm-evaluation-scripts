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
    assert scores['Overall Precision'] == 0.6619718309859155
    assert scores['Overall Recall'] == 0.6527777777777778
    assert scores['Overall F1'] == 0.6573426573426574
    assert scores['Overall Accuracy'] == 0.6527777777777778
    assert scores['Total GT'] == 72
    assert scores['Total MGM'] == 71
    assert scores['True Positive'] == 47
    assert scores['False Positive'] == 24
    assert scores['False Negative'] == 25


## test unique entity instances with entity set common and match types false
def test_case_2():
    use_case = "unique_entity_instances_mapped"
    tool = None
    match_types = False
    ground_truth_entities = "spacy"
    ner = NER(use_case, None, ground_truth_entities)
    scores, output_data = ner.evaluate(spacy_gt, spacy_mgm, tool, match_types)
    assert scores['Overall Precision'] == 0.5588235294117647
    assert scores['Overall Recall'] == 0.41304347826086957
    assert scores['Overall F1'] == 0.475
    assert scores['Overall Accuracy'] == 0.41304347826086957
    assert scores['Total GT'] == 46
    assert scores['Total MGM'] == 34
    assert scores['True Positive'] == 19
    assert scores['False Positive'] == 15
    assert scores['False Negative'] == 27

## test unique entity instances with entity set common and match types true failed
def test_case_3():
    use_case = "all_entity_instances_tool_specified"
    tool = "spacy"
    entity_type = None
    match_types = True
    ground_truth_entities = "spacy"
    ner = NER(use_case, entity_type, ground_truth_entities)
    scores, output_data = ner.evaluate(spacy_gt, spacy_mgm, tool, match_types)
    
    assert scores['Overall Precision'] == 0.6197183098591549
    assert scores['Overall Recall'] == 0.6111111111111112
    assert scores['Overall F1'] == 0.6153846153846154
    assert scores['Overall Accuracy'] == 0.6111111111111112
    assert scores['Total GT'] == 72
    assert scores['Total MGM'] == 71
    assert scores['True Positive'] == 44
    assert scores['False Positive'] == 27
    assert scores['False Negative'] == 28
    
## test unique entity instances with entity set common and match types false, gt file format spacy
def test_case_4():
    use_case = "unique_entity_instances_mapped"
    match_types = False
    ground_truth_entities = "spacy"
    ner = NER(use_case, None, ground_truth_entities)
    scores, output_data = ner.evaluate(spacy_gt, comprehend_mgm, None, match_types)
    
    assert scores['Overall Precision'] == 0.5806451612903226
    assert scores['Overall Recall'] == 0.6428571428571429
    assert scores['Overall F1'] == 0.6101694915254238
    assert scores['Overall Accuracy'] == 0.6428571428571429 
    assert scores['Total GT'] == 56
    assert scores['Total MGM'] == 62
    assert scores['True Positive'] == 36
    assert scores['False Positive'] == 26
    assert scores['False Negative'] == 20

def test_case_5():
    use_case = "all_entity_instances_mapped"
    tool = "comprehend"
    entity_set = None
    match_types = True
    ground_truth_entities = "spacy"
    ner = NER(use_case, entity_set, ground_truth_entities)
    scores, output_data = ner.evaluate(spacy_gt, comprehend_mgm, tool, match_types)
    
    assert scores['Overall Precision'] == 0.47619047619047616
    assert scores['Overall Recall'] == 0.4166666666666667
    assert scores['Overall F1'] == 0.4444444444444445
    assert scores['Overall Accuracy'] == 0.4166666666666667 
    assert scores['Total GT'] == 72
    assert scores['Total MGM'] == 63
    assert scores['True Positive'] == 30
    assert scores['False Positive'] == 33
    assert scores['False Negative'] == 42

test_case_1()
test_case_2()
test_case_3()
test_case_4()
test_case_5()