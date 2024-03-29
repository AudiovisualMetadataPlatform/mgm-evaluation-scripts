#!/bin/env amp_python.sif

import argparse
from classifier import Classifier as NER
import traceback
from amp.logging import *
import logging
from amp.file_handler import * 
import datetime

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
    parser.add_argument("--entity-types", type=str, help="Entity types to include in scoring")
    parser.add_argument("--ground-truth-entities", type=str, help="Ground truth entities of Named Entity Recognition", choices=['spacy', 'comprehend', 'common'])
    parser.add_argument("--tool", type=str, help="MGM Tool used for Named Entity Recognition output.", choices=['spacy', 'comprehend'])
    parser.add_argument("--match-types", type=str2bool, help="Entity or Entity type should match", default=False)
    parser.add_argument("-u", "--use-case", type=str,  required=True, help="Use Case for evaluation", choices=['all_entity_instances_tool_specified', 'unique_entity_instances_tool_specified', 'all_entity_instances_mapped', 'unique_entity_instances_mapped'])
    parser.add_argument("-o", "--output-file-path", type=str, required=True, help="Test output file path.")
    args = parser.parse_args()

    if args.use_case in ['unique_entity_instances_tool_specified', 'all_entity_instances_tool_specified'] and (args.tool == None or args.tool == ''):
        parser.error("--tool required for category {}".format(args.category))

    if args.use_case in ['unique_entity_instances_mapped', 'all_entity_instances_mapped']:
        if (args.ground_truth_entities == None or args.ground_truth_entities == ''):
            parser.error("--ground-truth-entities required for category {}".format(args.category))

    try:
        current = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename =  get_file_name(args.mgm_output_file) + current + ".json"
        output_path = os.path.join(args.output_file_path, 'ner')
        ner = NER(args.use_case, args.entity_types, args.ground_truth_entities)
        scores, comparisons = ner.evaluate(args.ground_truth_file, args.mgm_output_file, args.tool, args.match_types)
        headers = ner.get_headers(comparisons)
        data = {
            "scores": scores,
            "headers": headers,
            "comparison": comparisons
        }
        abs_path = create_json_file(output_path, filename, data)
        print("success:" + abs_path)
    except:
        logging.error(traceback.format_exc())
        print(traceback.format_exc())