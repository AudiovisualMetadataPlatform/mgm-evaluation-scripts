import pytest
import os
from classifier import Classifier as ShotDetection

def test_classifier_scores():
    ground_truth_file = os.path.join("sample_data", "sample_gt.csv")
    mgm_output_file = os.path.join("sample_data", "sample_azure.json")
    scores, output_data = ShotDetection().evaluate(ground_truth_file, mgm_output_file, 3)
    assert scores['threshold'] == 3
    assert scores['precision'] == 0.5882352941176471
    assert scores['recall'] == 0.29411764705882354
    assert scores['f1'] == 0.3921568627450981
    assert scores['gt_count'] == 34
    assert scores['mgm_count'] == 16
    assert scores['true_pos'] == 10
    assert scores['false_pos'] == 7
    assert scores['false_neg'] == 24 
    assert scores['cut'] == 0
    assert scores['dissolve'] == 10
    assert scores['lighting change'] == 0
    assert scores['panning'] == 0
    assert scores['zoom'] == 0

test_classifier_scores()