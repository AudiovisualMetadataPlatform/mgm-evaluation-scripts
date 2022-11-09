import pytest
import os
from classifier import Classifier as AudioSegmentation

def test_classifier_scores():
    ground_truth_file = os.path.join("sample_data", "sample_gt.csv")
    mgm_output_file = os.path.join("sample_data", "sample_segments.json")
    scores, output_data = AudioSegmentation('by_seconds').evaluate(ground_truth_file, mgm_output_file)
    assert scores['precision'] == 0.5893805309734513
    assert scores['recall'] == 0.5893805309734513
    assert scores['f1'] == 0.5893805309734513
    assert scores['accuracy'] == 0.5893805309734513
    assert scores['gt_count'] == 1695
    assert scores['mgm_count'] == 1695
    assert scores['true_pos'] == 999
    assert scores['false_pos'] == 696
    assert scores['false_neg'] == 696
    assert scores['gt_silence'] == 4
    assert scores['gt_music'] == 1278
    assert scores['gt_speech'] == 164
    assert scores['gt_noise'] == 249
    assert scores['mgm_silence'] == 4
    assert scores['mgm_music'] == 815
    assert scores['mgm_speech'] == 59
    assert scores['mgm_noise'] == 817
    assert scores['true_pos_silence'] == 4
    assert scores['true_pos_music'] == 754
    assert scores['true_pos_speech'] == 52
    assert scores['true_pos_noise'] == 189
    assert scores['accuracy_silence'] == 1.0
    assert scores['accuracy_speech'] == 0.3170731707317073
    assert scores['accuracy_music'] == 0.5899843505477308
    assert scores['accuracy_noise'] == 0.7590361445783133
    
test_classifier_scores()
    