import pytest
import os
from classifier import Classifier as ApplauseDetection

def test_by_seconds_scores():
    ground_truth_file = os.path.join("sample_data", "sample_gt.csv")
    mgm_output_file = os.path.join("sample_data", "sample_mgm.json")
    scores, output_data = ApplauseDetection('by_seconds').evaluate(ground_truth_file, mgm_output_file)
    assert scores['Overall Precision'] == 0.9470980996404725
    assert scores['Overall Recall'] == 0.9470980996404725
    assert scores['Overall F1'] == 0.9470980996404725
    assert scores['Overall Accuracy'] == 0.9384223918575063
    assert scores['Total GT'] == 1965
    assert scores['Total MGM'] == 1947
    assert scores['True Positive'] == 1844
    assert scores['False Positive'] == 103
    assert scores['False Negative'] == 103
    assert scores['GT Non-applause'] == 1863
    assert scores['GT Applause'] == 102
    assert scores['MGM Non-applause'] == 1896
    assert scores['MGM Applause'] == 51
    assert scores['True Positive Non-applause'] == 1819
    assert scores['True Positive Applause'] == 25
    assert scores['Accuracy Applause'] == 0.24509803921568626
    assert scores['Accuracy Non-applause'] == 0.97638217928073

def test_by_segments_scores():
    ground_truth_file = os.path.join("sample_data", "sample_gt.csv")
    mgm_output_file = os.path.join("sample_data", "sample_mgm.json")
    scores, output_data = ApplauseDetection('by_segments').evaluate(ground_truth_file, mgm_output_file, 2)
    assert scores['Overall Precision'] == 0.11764705882352941 
    assert scores['Overall Recall'] == 0.08 
    assert scores['Overall F1'] == 0.09523809523809526 
    assert scores['Overall Accuracy'] == 0.08 
    assert scores['Total GT'] == 25 
    assert scores['Total MGM'] == 17 
    assert scores['True Positive'] == 2 
    assert scores['False Positive'] == 15 
    assert scores['False Negative'] == 23 
    assert scores['Accuracy Applause'] == 0.08333333333333333 
    assert scores['Accuracy Non-applause'] == 0.07692307692307693
    
test_by_segments_scores()
test_by_seconds_scores()
    