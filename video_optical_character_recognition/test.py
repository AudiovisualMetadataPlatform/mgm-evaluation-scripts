import pytest
import os
from classifier import Classifier as VOCR

def test_case_1():
    ground_truth_file = os.path.join("sample_data", "sample_gt.csv")
    mgm_output_file = os.path.join("sample_data", "sample_azure.json")
    scores, output_data = VOCR('unique_text').evaluate(ground_truth_file, mgm_output_file)
    assert scores['Overall Precision'] == 0.234375
    assert scores['Overall Recall'] == 0.4838709677419355
    assert scores['Overall F1'] == 0.3157894736842105
    assert scores['Overall Accuracy'] == 0.4838709677419355
    assert scores['Total GT'] == 31
    assert scores['Total MGM'] == 64
    assert scores['True Positive'] == 15
    assert scores['False Positive'] == 49
    assert scores['False Negative'] == 16

def test_case_2():
    ground_truth_file = os.path.join("sample_data", "sample_gt.csv")
    mgm_output_file = os.path.join("sample_data", "sample_azure.json")
    scores, output_data = VOCR('each_text').evaluate(ground_truth_file, mgm_output_file)
    assert scores['Overall Precision'] == 0.24939467312348668
    assert scores['Overall Recall'] == 0.8583333333333333
    assert scores['Overall F1'] == 0.3864915572232645
    assert scores['Overall Accuracy'] == 0.8583333333333333
    assert scores['Total GT'] == 120
    assert scores['Total MGM'] == 413
    assert scores['True Positive'] == 103
    assert scores['False Positive'] == 310
    assert scores['False Negative'] == 17
    
test_case_1()
test_case_2()
    