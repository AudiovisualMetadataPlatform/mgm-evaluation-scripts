import re, os
import string
from num2words import num2words
import json
from .helper import *

config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
with open(config_file, "r") as f:
  data = json.load(f)
abbrs = data["abbrs"]
contractions = data["contractions"]
numwords = data["numwords"]

#functions to normalize transcripts
# Lowercasing all words
# Expanding written abbreviations to their full forms (such Dr. as to doctor)
# Contracting words that can be contracted
# Spelling all compound words with spaces (such as blackboard to black board or part-time to part time)
# Converting numerals to words (or vice-versa)
# Removing punctuation (except apostrophes)
def expandAbbr(transcript):
  """Expand abbreviations in abbrs list"""
  words = transcript.split(' ')
  newwordlist = []
  for w in words:
    if w.replace('.', '') in abbrs:
      newwordlist.append(abbrs[w.replace('.', '')])
    else:
      newwordlist.append(w)
  newtranscript = ' '.join(newwordlist)
  return newtranscript

def expandContractions(transcript):
  """Expand contractions in contractions list"""
  for k,v in contractions.items():
    transcript = transcript.replace(k, v)
  return transcript

def numsToWords(transcript):
  """Convert numbers to words"""
  words = transcript.split(' ')
  newwordlist = []
  for w in words:
    if re.search('\d+', w):
      w = w.replace(',', '')
      if w[0] == '$':
        x = w.replace('$', '').split('.')
        if x[0] != '0':
          numword = num2words(x[0])
          newwordlist.append(numword)
          if x[0] == '1':
            newwordlist.append('dollar')
          else:
            newwordlist.append('dollars')
        if len(x) == 2:
          if x[1] != '00':
            numword = num2words(x[1])
            newwordlist.append(numword)
            newwordlist.append('cents')
      else:
        try:
          numword = num2words(w)
          newwordlist.append(numword)
        except:
          newwordlist.append(w)
    else:
      newwordlist.append(w)
  newtranscript = ' '.join(newwordlist)
  return newtranscript

def umuh(transcript):
  """Remove 'um's and 'uh's from transcript """
  transcript = transcript.replace('um', '')
  transcript = transcript.replace('uh', '')
  return transcript

def normalize(transcript):
    transcript = readFile(transcript)
    """Normalize a GT transcript or MGM output for WER comparison."""
    #lowercase
    transcript = transcript.lower().replace ('%', ' percent')
    #expand abbreviations
    transcript = expandAbbr(transcript)
    #contract to contractions
    transcript = expandContractions(transcript)
    #convert numbers to words
    transcript = numsToWords(transcript)
    #remove ums and uhs
    transcript = umuh(transcript)
    #replace hyphen with spaces
    transcript = transcript.replace('-', ' ')
    #strip punctuation
    transcript = transcript.translate(str.maketrans('', '', string.punctuation))
    #strip extra spaces
    transcript = ' '.join(transcript.split())
    return transcript