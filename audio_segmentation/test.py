import pytest
import os
from classifier import Classifier as AudioSegmentation

def test_classifier_scores():
    ground_truth_file = os.path.join("sample_data", "sample_gt.csv")
    mgm_output_file = os.path.join("sample_data", "sample_segments.json")
    scores, output_data = AudioSegmentation('by_seconds').evaluate(ground_truth_file, mgm_output_file)
    assert scores['Overall Precision'] == 0.5893805309734513
    assert scores['Overall Recall'] == 0.5893805309734513
    assert scores['Overall F1'] == 0.5893805309734513
    assert scores['Overall Accuracy'] == 0.5893805309734513
    assert scores['Total GT'] == 1695
    assert scores['Total MGM'] == 1695
    assert scores['True Positive'] == 999
    assert scores['False Positive'] == 696
    assert scores['False Negative'] == 696
    assert scores['GT Silence'] == 4
    assert scores['GT Music'] == 1278
    assert scores['GT Speech'] == 164
    assert scores['GT Noise'] == 249
    assert scores['MGM Silence'] == 4
    assert scores['MGM Music'] == 815
    assert scores['MGM Speech'] == 59
    assert scores['MGM Noise'] == 817
    assert scores['True Positive Silence'] == 4
    assert scores['True Positive Music'] == 754
    assert scores['True Positive Speech'] == 52
    assert scores['True Positive Noise'] == 189
    assert scores['Accuracy Silence'] == 1.0
    assert scores['Accuracy Speech'] == 0.3170731707317073
    assert scores['Accuracy Music'] == 0.5899843505477308
    assert scores['Accuracy Noise'] == 0.7590361445783133
    
test_classifier_scores()