import pytest
import os
from classifier import Classifier as ShotDetection

def test_classifier_scores():
    ground_truth_file = os.path.join("sample_data", "sample_gt.csv")
    mgm_output_file = os.path.join("sample_data", "sample_azure.json")
    scores, output_data = ShotDetection().evaluate(ground_truth_file, mgm_output_file, 3)
    assert scores['Overall Precision'] == 0.5882352941176471
    assert scores['Overall Recall'] == 0.29411764705882354
    assert scores['Overall F1'] == 0.3921568627450981
    assert scores['Total GT'] == 34
    assert scores['Total MGM'] == 16
    assert scores['True Positive'] == 10
    assert scores['False Positive'] == 7
    assert scores['False Negative'] == 24 
    assert scores['True Positive Cut'] == 0
    assert scores['True Positive Dissolve'] == 10
    assert scores['True Positive Lighting Change'] == 0
    assert scores['True Positive Panning'] == 0
    assert scores['True Positive Zoom'] == 0

test_classifier_scores()