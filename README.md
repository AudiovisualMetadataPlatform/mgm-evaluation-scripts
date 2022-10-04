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
| Category |  -c | --category | AudioSegmentationBySegments, AudioSegmentationBySeconds, SpeechToText, ApplauseDetectionBySeconds, ApplauseDetectionBySegments, ShotDetection |
| Help |  -h | | |

## Sample commands

### Audio Segmentation By Segments
```bash
$ python3 main.py -g gloria-gibson-hudson-segments-gt.csv -m for-testing-gloria-gibson-hudson-segments.json -t 2 -c AudioSegmentationBySegments
```

### Audio Segmentation By Seconds
```bash
$ python3 main.py -g little_500_gt.csv -m little_500_segments.json -c AudioSegmentationBySeconds
```

### Speech To Text
```bash
$ python3 main.py -g sample_gt.txt -m sample_aws.txt -c SpeechToText
```

### Shot Detection
```bash
$ python3 main.py -g journey_to_center_triangle_gt.csv -m journey_to_center_triangle_azure.json -c ShotDetection -t 3
```