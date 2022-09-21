## MGM Evaluation

Python scripts to evaluate MGM output by comparing with ground truth and calculate performance metrics.

### Pre-requisite 
- Python3.9

## Options available to run script from CLI

| Options   |      short      |  full | Possible Values |
|----------|:-------------:|------:|------:|
| Ground Truth File |  -g | --ground-truth-file | any string |
| MGM output File |  -m | --mgm-output-file | any string |
| Threshold |  -t | --threshold | integer |
| Category |  -c | --category | AudioSegmentationBySegments, AudioSegmentationBySeconds |
| Help |  -h | | |

## Sample commands

```bash
$ python3 main.py -g gloria-gibson-hudson-segments-gt.csv -m for-testing-gloria-gibson-hudson-segments.json -t 2 -c AudioSegmentationBySegments
```

```bash
$ python3 main.py -g little_500_gt.csv -m little_500_segments.json -c AudioSegmentationBySeconds
```