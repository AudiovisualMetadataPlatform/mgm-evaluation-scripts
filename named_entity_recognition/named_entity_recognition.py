#!/bin/env amp_python.sif

import argparse
from classifier import Classifier as NER
import traceback
from amp.logging import *
import logging
from amp.file_handler import * 

setup_logging('ner_evaluation', True)

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--ground-truth-file", type=str, required=True, help="Ground Truth file path.")
    parser.add_argument("-m", "--mgm-output-file", type=str, required=True, help="MGM output file path.")
    parser.add_argument("--entity-set", type=str, help="Entity set of Named Entity Recognition", choices=['spacy', 'comprehend', 'common'])
    parser.add_argument("--ground-truth-entities", type=str, help="Ground truth entities of Named Entity Recognition", choices=['spacy', 'comprehend', 'common'])
    parser.add_argument("--tool", type=str, help="MGM Tool used for Named Entity Recognition output.", choices=['spacy', 'comprehend'])
    parser.add_argument("--match-types", type=str2bool, help="Entity or Entity type should match", default=False)
    parser.add_argument("-u", "--use-case", type=str,  required=True, help="Use Case for evaluation", choices=['all_entity_instances_tool_specified', 'unique_entity_instances_tool_specified', 'all_entity_instances_mapped', 'unique_entity_instances_mapped'])
    args = parser.parse_args()

    if args.use_case in ['unique_entity_instances_tool_specified', 'all_entity_instances_tool_specified'] and (args.tool == None or args.tool == ''):
        parser.error("--tool required for category {}".format(args.category))

    if args.use_case in ['unique_entity_instances_mapped', 'all_entity_instances_mapped']:
        if (args.entity_set == None or args.entity_set == ''):
            parser.error("--entity-set required for category {}".format(args.category))
        
        if (args.ground_truth_entities == None or args.ground_truth_entities == ''):
            parser.error("--ground-truth-entities required for category {}".format(args.category))

    try:
        filename = get_file_name(args.mgm_output_file)
        ner = NER(args.use_case, args.entity_set, args.ground_truth_entities)
        scores, output_data = ner.evaluate(args.ground_truth_file, args.mgm_output_file, args.tool, args.match_types)
        create_csv_from_dict(filename + '_' + args.use_case + '_' +  str(args.match_types) + '_scores.csv', [scores])
        create_csv_from_dict(filename + '_' + args.use_case + '_' +  str(args.match_types) + '_comparison_results.csv', output_data)
    except:
        logging.error(traceback.format_exc())