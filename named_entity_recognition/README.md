## Named Entity Recognition MGM Evaluation

Python scripts to evaluate NER MGM output by comparing with ground truth and calculate performance metrics.

### Pre-requisite 
- Python3.9

## Options available to run script from CLI

| Options   |      short      |  full | Possible Values |
|----------|:-------------:|------:|------:|
| Ground Truth File |  -g | --ground-truth-file | any string |
| MGM output File |  -m | --mgm-output-file | any string |
| Threshold |  -t | --threshold | integer |
| Use Case |  -u | --use-case | all_entity_instances_tool_specified, unique_entity_instances_tool_specified, all_entity_instances_mapped, unique_entity_instances_mapped |
| Tool | | --tool | spacy, comprehend |
| Entity Types | | --entity-types | comma separated string |
| Ground Truth Entities | | --ground-truth-entities | spacy, comprehend, common |
| Match Types | | --match-types | Boolean | Default is False
| Help |  -h | | |

## Sample commands

### Test Case 1
```bash
$ amp_python.sif named_entity_recognition.py -g sample_data/sample_spacy_gt.csv -m sample_data/sample_spacy.json -u all_entity_instances_tool_specified --tool spacy
```

### Test Case 2
```bash
$ amp_python.sif named_entity_recognition.py -g sample_data/sample_spacy_gt.csv -m sample_data/sample_spacy.json -u unique_entity_instances_mapped --ground-truth-entities spacy
```

### Test Case 3
```bash
$ amp_python.sif named_entity_recognition.py -g sample_data/sample_spacy_gt.csv -m sample_data/sample_spacy.json -u all_entity_instances_tool_specified --tool spacy --match-types y
```

### Test Case 4
```bash
$ amp_python.sif named_entity_recognition.py -g sample_data/sample_spacy_gt.csv -m sample_data/sample_aws.json -u unique_entity_instances_mapped --ground-truth-entities spacy --match-types n
```

### Test Case 5
```bash
$ amp_python.sif named_entity_recognition.py -g sample_data/sample_spacy_gt.csv -m sample_data/sample_aws.json -u all_entity_instances_mapped --ground-truth-entities spacy --match-types y
```