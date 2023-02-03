import pytest
import os
from classifier import Classifier as STT
import math

def test_classifier_scores():
    ground_truth_file = os.path.join("sample_data", "sample_gt.txt")
    mgm_output_file = os.path.join("sample_data", "sample_aws_transcribe.json")
    scores, output_data = STT().evaluate(ground_truth_file, mgm_output_file)
    assert round(scores['Word Error Rate'], 2) == 0.05
    assert round(scores['Match Error Rate'], 2) == 0.05
    assert round(scores['Word Info Loss'], 2) == 0.07
    assert round(scores['Word Info Processed'], 2) == 0.93
    assert round(scores['Character Error Rate'], 2) == 0.03
    assert round(scores['Substitution Rate'], 2) == 0.02
    assert round(scores['Insertion Rate'], 3) == 0.004
    assert round(scores['Deletion Rate'], 2) == 0.03

test_classifier_scores()
    