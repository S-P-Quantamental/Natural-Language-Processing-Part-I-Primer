# Natural Language Processing – Part I: Primer
## Unveiling the Hidden Information in Earnings Calls
## As of Sep. 5, 2017 by Frank Zhao, Quantamental Research Group at S&P Global Market Intelligence 

---
Analyses for the primer are performed with Python and Matlab. All the NLP is done in Python, a tool that is free, ubiquitous in the field, and robust once the practitioner can navigate the learning curve. The calculations and matrix manipulations are done in Matlab (Python does have a Matlab-like library numpy, but we used Matlab due to preference).

---

Step 1: Download the Python integrated development environment (IDE). For illustrative
purposes, we used Anaconda. https://www.anaconda.com/download/

---

Step 2: Obtain sentiment word lists and save them to text files to ingest by the Python code. For illustrative purposes, we used Loughran and McDonald (2011) sentiment word lists (https://www3.nd.edu/~mcdonald/Word_Lists.html) to identify the sentiment of each
earnings call transcript.

---

Step 3: Format earnings call transcripts in the following way. There are five columns in the input files where the columns going from left to right are: stock identifier, earning call date, hour and minute, sequence identifier of every earnings call and the content of

---

Step 4: Load Python libraries that one needs (lines 22 – 35)

```python
# import libraries  
import os                 # import the os module 
import pandas as pd       # using pandas for data structure 
import nltk               # nlp library
import time               # time module can be used now e.g., time.time()

# set path
fpath = '<your_environment>/NLP/rawData/'
os.chdir(fpath) # chg working directory to fpath  
```

---

Step 5: Load in Loughran and McDonald (2011) word lists (lines 43 - 69).

```python
# initialize word lists, dict, negation list etc ...                                                                                            
fn = 'wordLists\\lmMasterList.txt' # input file
tmpWordListPandaObj = pd.read_csv(fn, sep='\t', header=None) # read in tab-delimited text file with no header
tmpWordListPandaObj.columns = ['master'] 		# rename cols 
master_list = list(tmpWordListPandaObj.master)    
master_list = [ itr for itr in master_list if not isinstance(itr,float) ]  
master_list = [itr.lower() for itr in master_list] # make all lowercase
```

---

Step 6: Define the functions that you are going to use. The one function included below
outputs the frequency count of words (lines 84 - 160).

```python
# check whether a word from list2 is in list1 then count the frequency of that word
def _out_word_freq1(list1, list2):
    wordFreqDictObj = {}
    for item in list2: 
        if item in list1: 
            wordFreqDictObj[item] = wordFreqDictObj.get(item, 0) + 1
    return wordFreqDictObj
```

---



Copyright © 2020 by S&P Global Market Intelligence, a division of S&P Global Inc. All
rights reserved. 
