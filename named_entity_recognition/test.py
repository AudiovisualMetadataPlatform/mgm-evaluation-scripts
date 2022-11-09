import pytest
import os
from classifier import Classifier as NER

comprehend_gt = os.path.join("sample_data", "sample_aws_gt.csv")
comprehend_mgm = os.path.join("sample_data", "sample_aws.json")


spacy_gt = os.path.join("sample_data", "sample_spacy_gt.csv")
spacy_mgm = os.path.join("sample_data", "sample_spacy.json")


## test all entities with spacy and match types false
def test_all_entity_instances_tool_specified():
    ner = NER("all_entity_instances_tool_specified", "spacy", "spacy")
    scores, output_data = ner.evaluate(spacy_gt, spacy_mgm, "spacy", False)
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
def test_unique_entity_instances_mapped_n():
    ner = NER("unique_entity_instances_mapped", "common", "spacy")
    scores, output_data = ner.evaluate(spacy_gt, spacy_mgm, "spacy", False)
    assert scores['precision'] == 0.46875
    assert scores['recall'] == 0.6818181818181818
    assert scores['f1'] == 0.5555555555555556
    assert scores['accuracy'] == 0.6818181818181818
    assert scores['gt_count'] == 22
    assert scores['mgm_count'] == 32
    assert scores['true_pos'] == 15
    assert scores['false_pos'] == 17
    assert scores['false_neg'] == 7

## test unique entity instances with entity set common and match types true failed
def test_unique_entity_instances_mapped_y():
    ner = NER("all_entity_instances_mapped", "common", "spacy")
    scores, output_data = ner.evaluate(spacy_gt, spacy_mgm, "spacy", True)
    print(scores)
    # assert scores['precision'] == 0.46875
    # assert scores['recall'] == 0.6818181818181818
    # assert scores['f1'] == 0.5555555555555556
    # assert scores['accuracy'] == 0.6818181818181818
    # assert scores['gt_count'] == 22
    # assert scores['mgm_count'] == 32
    # assert scores['true_pos'] == 15
    # assert scores['false_pos'] == 17
    # assert scores['false_neg'] == 7
    
## test unique entity instances with entity set common and match types false, gt file format spacy
def test_aws_unique_entity_instances_mapped_y():
    ner = NER("unique_entity_instances_mapped", "common", "spacy")
    scores, output_data = ner.evaluate(spacy_gt, comprehend_mgm, "comprehend", False)
    assert scores['precision'] == 0.4583333333333333
    assert scores['recall'] == 0.6111111111111112
    assert scores['f1'] == 0.5238095238095238
    assert scores['accuracy'] == 0.6111111111111112 
    assert scores['gt_count'] == 36
    assert scores['mgm_count'] == 48 
    assert scores['true_pos'] == 22 
    assert scores['false_pos'] == 26
    assert scores['false_neg'] == 14


def test_aws_all_entity_instances_mapped_y():
    ner = NER("all_entity_instances_mapped", "common", "comprehend")
    scores, output_data = ner.evaluate(comprehend_gt, comprehend_mgm, "comprehend", True)
    print(scores)
    # assert scores['precision'] == 0.4583333333333333
    # assert scores['recall'] == 0.6111111111111112
    # assert scores['f1'] == 0.5238095238095238
    # assert scores['accuracy'] == 0.6111111111111112 
    # assert scores['gt_count'] == 36
    # assert scores['mgm_count'] == 48 
    # assert scores['true_pos'] == 22 
    # assert scores['false_pos'] == 26
    # assert scores['false_neg'] == 14



test_aws_all_entity_instances_mapped_y()