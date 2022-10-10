import pytest
import os
from classifier import Classifier as STT

def test_classifier_scores():
    ground_truth_file = os.path.join("sample_data", "sample_gt.txt")
    mgm_output_file = os.path.join("sample_data", "sample_aws_transcribe.json")
    scores, output_data = STT().evaluate(ground_truth_file, mgm_output_file)
    assert scores['word_error_rate'] == 0.05148514851485148
    assert scores['match_error_rate'] == 0.05128205128205128
    assert scores['word_info_loss'] == 0.07165026533048446
    assert scores['word_info_processed'] == 0.9283497346695155
    assert scores['character_error_rate'] == 0.033661593554162934
    assert scores['substitution_rate'] == 0.02079207920792079
    assert scores['insertion_rate'] == 0.0039603960396039604
    assert scores['deletion_rate'] == 0.026732673267326732

test_classifier_scores()
    