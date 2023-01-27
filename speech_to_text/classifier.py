import metrics as metrics
from text_cleanup import *
import Levenshtein
from typing import Any, Dict, List, Tuple, Union
from itertools import chain
from jiwer import transforms as tr
from jiwer.transformations import wer_default, wer_standardize, cer_default_transform
from amp.file_handler import *
import logging
from itertools import chain

class Classifier():
    def __init__(self):
        logging.info("Evaluating Speech To Text")
        self.metrics = metrics.Metrics()

    def evaluate(self, ground_truth_file, mgm_output_file):
        transcript = read_text_file(ground_truth_file)
        normalized_gt = normalize(transcript)
        mgm = read_json_file(mgm_output_file)
        transcript = mgm["results"]["transcript"]
        normalized_mgm = normalize(transcript)
        output_list = self.generate_comparison_list(normalized_gt, normalized_mgm)
        errors = self.getErrorProportionPerType(output_list)
        scores = self.scoring(normalized_gt, normalized_mgm, errors)
        return scores, output_list

    def generate_comparison_list(self, normalized_gt, normalized_mgm):
        logging.info("Generating list")
        #preprocess texts
        tc, hc = self._preprocess(normalized_gt, normalized_mgm, wer_standardize, wer_standardize)

        #use Levenshtein editops to generate comparisons
        comp = Levenshtein.editops(tc[0], hc[0])

        #split ground truth and mgm output into lists of words
        new_gt = normalized_gt.split(' ')
        new_mgm = normalized_mgm.split(' ')
        #set offsets to zero
        gt_offset = 0
        mgm_offset = 0

        #iterate through each comparison and if it's a deletion or insertion, insert a blank word in the appropriate list of words to align the lists
        for c in comp:
            if c[0] == 'delete':
                new_mgm.insert(c[2]+mgm_offset, '**')
                mgm_offset += 1
            elif c[0] == 'insert':
                new_gt.insert(c[1]+gt_offset, '**')
                gt_offset += 1

        #zip the lists together into a list of tuples
        aligned = list(zip(new_gt, new_mgm))
        #convert the list of tuples to a list of dicts, adding the error type where necessary, based on presence of blank words (deletion or insertion)
        # or mismatched words (substitution)
        new_aligned = []

        for a in aligned:
            if a[0] == '**':
                new_aligned.append({'ground_truth':a[0], 'mgm':a[1], 'error':'insertion'})
            elif a[1] == '**':
                new_aligned.append({'ground_truth':a[0], 'mgm':a[1], 'error':'deletion'})
            elif a[0] != a[1]:
                new_aligned.append({'ground_truth':a[0], 'mgm':a[1], 'error':'substitution'})
            else:
                new_aligned.append({'ground_truth':a[0], 'mgm':a[1]})
        
        return new_aligned
        



    def scoring(self, normalized_gt, normalized_mgm, error_rates):
        logging.info("Preparing scores")
        wer = self.metrics.wordErrorRate(normalized_gt,normalized_mgm)
        return {
            "Word Error Rate": wer,
            "Match Error Rate": self.metrics.matchErrorRate(normalized_gt,normalized_mgm),
            "Word Info Loss": self.metrics.wordInfoLoss(normalized_gt,normalized_mgm),
            "Word Info Processed": self.metrics.wordInfoProcessed(normalized_gt,normalized_mgm),
            "Character Error Rate": self.metrics.characterErrorRate(normalized_gt,normalized_mgm),
            "Substitution Rate": self.metrics.substitutionErrorRate(wer, error_rates['substitutions']),
            "Insertion Rate": self.metrics.insertionErrorRate(wer, error_rates['insertions']),
            "Deletion Rate": self.metrics.deletionErrorRate(wer, error_rates['deletions'])
        }
    
    def _preprocess(self,
        truth: List[str],
        hypothesis: List[str],
        truth_transform: Union[tr.Compose, tr.AbstractTransform],
        hypothesis_transform: Union[tr.Compose, tr.AbstractTransform],
    ) -> Tuple[List[str], List[str]]:
        """
        Pre-process the truth and hypothesis into a form such that the Levenshtein
        library can compute the edit operations.can handle.
        :param truth: the ground-truth sentence(s) as a string or list of strings
        :param hypothesis: the hypothesis sentence(s) as a string or list of strings
        :param truth_transform: the transformation to apply on the truths input
        :param hypothesis_transform: the transformation to apply on the hypothesis input
        :return: the preprocessed truth and hypothesis
        """
        logging.info("Preprocessing data")
        # Apply transforms. The transforms should collapses input to a list of list of words
        transformed_truth = truth_transform(truth)
        transformed_hypothesis = hypothesis_transform(hypothesis)

        # tokenize each word into an integer
        vocabulary = set(chain(*transformed_truth, *transformed_hypothesis))

        if "" in vocabulary:
            raise ValueError(
                "Empty strings cannot be a word. "
                "Please ensure that the given transform removes empty strings."
            )

        word2char = dict(zip(vocabulary, range(len(vocabulary))))

        truth_chars = [
            "".join([chr(word2char[w]) for w in sentence]) for sentence in transformed_truth
        ]
        hypothesis_chars = [
            "".join([chr(word2char[w]) for w in sentence])
            for sentence in transformed_hypothesis
        ]

        return truth_chars, hypothesis_chars
    
    def getErrorProportionPerType(self, generated_list):
        #calculate insertion rate, deletion rate, and substitution rate
        s= 0
        d = 0
        i = 0
        for a in generated_list:
            if 'error' in a:
                if a['error'] == 'insertion':
                    i += 1
                elif a['error'] == 'deletion':
                    d += 1
                elif a['error'] == 'substitution':
                    s += 1
        #get proportions of each error type
        s_pc = s/(s + d + i)
        d_pc = d/(s + d + i)
        i_pc = i/(s + d + i)
        errors = { 'substitutions': s_pc, 'insertions': i_pc, 'deletions': d_pc }
        return errors

    def get_headers(self, comparisons):
        headers = read_json_file('headers.json')
        unique_headers = list(set(chain.from_iterable(sub.keys() for sub in comparisons)))
        output = []
        for header in headers:
            if header['field'] in unique_headers:
                output.append(header)
        return output


    