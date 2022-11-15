## Shot Detection MGM Evaluation

Python script to evaluate Shot Detection MGM output by comparing with ground truth and calculate performance metrics.

### Pre-requisite 
- Python3.9

## Options available to run script from CLI

| Options   |      short      |  full | Possible Values |
|----------|:-------------:|------:|------:|
| Ground Truth File |  -g | --ground-truth-file | any string |
| MGM output File |  -m | --mgm-output-file | any string |
| Threshold |  -t | --threshold | integer |
| Help |  -h | | |

## Sample commands

```bash
$ amp_python.sif shot_detection.py -g sample_data/sample_gt.csv -m sample_data/sample_azure.json -t 3
```