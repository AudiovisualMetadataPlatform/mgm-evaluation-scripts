## Video Optical Character Recognition MGM Evaluation

Python script to evaluate Video Optical Character Recognition MGM output by comparing with ground truth and calculate performance metrics.

### Pre-requisite 
- Python3.9

## Options available to run script from CLI

| Options   |      short      |  full | Possible Values |
|----------|:-------------:|------:|------:|
| Ground Truth File |  -g | --ground-truth-file | any string |
| MGM output File |  -m | --mgm-output-file | any string |
| Use Case |  -u | --use-case| unique_text, each_text |
| Output File Path |  -o | --output-file-path | any string |
| Help |  -h | | |

## Sample commands

### Test case 1
```bash
$ amp_python.sif video_optical_character_recognition.py -g sample_data/sample_gt.csv -m sample_data/sample_azure.json -u unique_text -o outputs
```

### Test case 2
```bash
$ amp_python.sif video_optical_character_recognition.py -g sample_data/sample_gt.csv -m sample_data/sample_azure.json -u each_text -o outputs
```