import pytest
import os
from classifier import Classifier as ApplauseDetection

def test_by_seconds_scores():
    ground_truth_file = os.path.join("sample_data", "sample_gt.csv")
    mgm_output_file = os.path.join("sample_data", "sample_mgm.json")
    scores, output_data = ApplauseDetection('by_seconds').evaluate(ground_truth_file, mgm_output_file)
    assert scores['overall_precision'] == 0.9470980996404725
    assert scores['overall_recall'] == 0.9470980996404725
    assert scores['overall_f1'] == 0.9470980996404725
    assert scores['overall_accuracy'] == 0.9384223918575063
    assert scores['total_gt'] == 1965
    assert scores['total_mgm'] == 1947
    assert scores['true_positive'] == 1844
    assert scores['false_positive'] == 103
    assert scores['false_negative'] == 103
    assert scores['gt_non-applause'] == 1863
    assert scores['gt_applause'] == 102
    assert scores['mgm_non-applause'] == 1896
    assert scores['mgm_applause'] == 51
    assert scores['true_positive_non-applause'] == 1819
    assert scores['true_positive_applause'] == 25
    assert scores['accuracy_applause'] == 0.24509803921568626
    assert scores['accuracy_non-applause'] == 0.97638217928073

def test_by_segments_scores():
    ground_truth_file = os.path.join("sample_data", "sample_gt.csv")
    mgm_output_file = os.path.join("sample_data", "sample_mgm.json")
    scores, output_data = ApplauseDetection('by_segments').evaluate(ground_truth_file, mgm_output_file, 2)
    assert scores['overall_precision'] == 0.11764705882352941 
    assert scores['overall_recall'] == 0.08 
    assert scores['overall_f1'] == 0.09523809523809526 
    assert scores['overall_accuracy'] == 0.08 
    assert scores['total_gt'] == 25 
    assert scores['total_mgm'] == 17 
    assert scores['true_positive'] == 2 
    assert scores['false_positive'] == 15 
    assert scores['false_negative'] == 23 
    assert scores['accuracy_applause'] == 0.08333333333333333 
    assert scores['accuracy_non-applause'] == 0.07692307692307693 
    assert scores['analysis_threshold'] == 2
    
test_by_segments_scores()
test_by_seconds_scores()
    