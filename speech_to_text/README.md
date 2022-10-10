## Speech-To-Text MGM Evaluation

Python script to evaluate Speech-To-Text MGM output by comparing with ground truth and calculate performance metrics.

### Pre-requisite 
- Python3.9

## Options available to run script from CLI

| Options   |      short      |  full | Possible Values |
|----------|:-------------:|------:|------:|
| Ground Truth File |  -g | --ground-truth-file | any string |
| MGM output File |  -m | --mgm-output-file | any string |
| Help |  -h | | |

## Sample commands

```bash
$ python3 speech_to_text.py -g sample_gt.txt -m sample_aws.json -c SpeechToText
```