## Speech-To-Text MGM Evaluation

Python script to evaluate Speech-To-Text MGM output by comparing with ground truth and calculate performance metrics.

### Pre-requisite 
- Python3.9

## Options available to run script from CLI

| Options   |      short      |  full | Possible Values |
|----------|:-------------:|------:|------:|
| Ground Truth File |  -g | --ground-truth-file | any string |
| MGM output File |  -m | --mgm-output-file | any string |
| Output File Path |  -o | --output-file-path | any string |
| Help |  -h | | |

## Sample commands

```bash
$ amp_python.sif speech_to_text.py -g sample_data/sample_gt.txt -m sample_data/sample_aws_transcribe.json -o results
```