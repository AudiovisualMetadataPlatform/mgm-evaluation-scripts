## Audio Segmentation

Python script to evaluate Audio Segmentation MGM output by comparing with ground truth and calculate performance metrics. We can evaluate based on segments or seconds.

### Pre-requisite 
- Python3.9

## Options available to run script from CLI

| Options   |      short      |  full | Possible Values |
|----------|:-------------:|------:|------:|
| Ground Truth File |  -g | --ground-truth-file | any string |
| MGM output File |  -m | --mgm-output-file | any string |
| Threshold |  -t | --threshold | integer |
| Use Case |  -u | --use-case | by_segments, by_seconds |
| Help |  -h | | |

## Sample commands

### Audio Segmentation By Segments
```bash
$ amp_python.sif audio_segmentation.py -g sample_data/sample_gt.csv -m sample_data/sample_segments.json -t 2 -u "by_segments" -o outputs
```

### Audio Segmentation By Seconds
```bash
$ amp_python.sif audio_segmentation.py -g sample_data/sample_gt.csv -m sample_data/sample_segments.json -u "by_seconds" -o outputs
```