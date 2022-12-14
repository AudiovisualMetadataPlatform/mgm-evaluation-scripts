import pytest
import os
from classifier import Classifier as VOCR

def test_case_1():
    ground_truth_file = os.path.join("sample_data", "sample_gt.csv")
    mgm_output_file = os.path.join("sample_data", "sample_azure.json")
    scores, output_data = VOCR('unique_text').evaluate(ground_truth_file, mgm_output_file)
    assert scores['precision'] == 0.234375
    assert scores['recall'] == 0.4838709677419355
    assert scores['f1'] == 0.3157894736842105
    assert scores['accuracy'] == 0.4838709677419355
    assert scores['gt_count'] == 31
    assert scores['mgm_count'] == 64
    assert scores['true_pos'] == 15
    assert scores['false_pos'] == 49
    assert scores['false_neg'] == 16

def test_case_2():
    ground_truth_file = os.path.join("sample_data", "sample_gt.csv")
    mgm_output_file = os.path.join("sample_data", "sample_azure.json")
    scores, output_data = VOCR('each_text').evaluate(ground_truth_file, mgm_output_file)
    assert scores['precision'] == 0.24939467312348668
    assert scores['recall'] == 0.8583333333333333
    assert scores['f1'] == 0.3864915572232645
    assert scores['accuracy'] == 0.8583333333333333
    assert scores['gt_count'] == 120
    assert scores['mgm_count'] == 413
    assert scores['true_pos'] == 103
    assert scores['false_pos'] == 310
    assert scores['false_neg'] == 17
    
test_case_1()
test_case_2()
    