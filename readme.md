# Natural Language Processing – Part I: Primer
## Unveiling the Hidden Information in Earnings Calls
## As of Sep. 5, 2017 by Frank Zhao, Quantamental Research Group at S&P Global Market Intelligence 

---
Analyses for the primer are performed with Python and Matlab. All the NLP is done in Python, a tool that is free, ubiquitous in the field, and robust once the practitioner can navigate the learning curve. The calculations and matrix manipulations are done in Matlab (Python does have a Matlab-like library numpy, but we used Matlab due to preference).

---

**Step 1:** Download the Python integrated development environment (IDE). For illustrative
purposes, we used Anaconda. https://www.anaconda.com/download/

---

**Step 2:** Obtain sentiment word lists and save them to text files to ingest by the Python code. For illustrative purposes, we used Loughran and McDonald (2011) sentiment word lists (https://www3.nd.edu/~mcdonald/Word_Lists.html) to identify the sentiment of each
earnings call transcript.

---

**Step 3:** Format earnings call transcripts in the following way. There are five columns in the input files where the columns going from left to right are: stock identifier, earning call date, hour and minute, sequence identifier of every earnings call and the content of

---

**Step 4:** Load Python libraries that one needs (lines 22 – 35)

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

**Step 5:** Load in Loughran and McDonald (2011) word lists (lines 43 - 69).

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

**Step 6:** Define the functions that you are going to use. The one function included below
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

**Step 7:** Have a control structure to traverse through time periods and firms. We decided to traverse one quarter at a time across all firms for that quarter. We used the while loop control structure whereas one could also use the for loop control structure. Relative to other languages like Matlab, C++, etc., the for loop in Python is very robust and powerful, which also makes some for loop syntaxes unintuitive. If you decide to use the for loop instead, perhaps consider using the key word enumerate where you can
actually observe and utilize the iterator in the for loop (lines 173 - 213).

```python
start_time = time.time(); # record time when a piece of code is executed 
yrItr = 0
while yrItr < len(yrVec):
    qtrItr = 0
    while qtrItr < len(qtrVec): 
        #creating filename to read in
        fn = str('C:\\Users\\fzhao\\Desktop\\NLP\\rawData\\transcriptsAll\\sp9_q' + str(qtrVec[qtrItr]) + '_' + str(yrVec[yrItr])  + '.txt') # input file
       
        #check file exists                                                                          
        if os.path.isfile(fn) and os.stat(fn).st_size != 0:
            tmpPandaObj = pd.read_csv(fn, sep='\t', header=None) # read in tab-delimited text file with no header
            tmpPandaObj.columns  = ['stockId','dt','hhmm','seq','ecalls'] # rename cols 
```

---

**Step 8:** This step is about tokenizing and preprocessing of an earnings call. In the screenshot below, we use the non-native, but well-known, nltk NLP library and specifically the method word_tokenize to parse an earnings call into tokens where the function parses whenever it encounters a (user-defined) punctuation or white space. We also show other text preprocessing that we did: i) removal of punctuation ii) removal of empty spaces between words and iii) standardizing all text to lower case and so forth
(lines 234 - 240).

```python
# nltk library methods + text preprocessing
dsRawSeriesObj = dsRawSeriesObj.replace("n't"," not")   
tokensListObj = nltk.word_tokenize(dsRawSeriesObj) # tokenize all words 
tokensListObj = [itr.lower() for itr in tokensListObj] # make all lowercase
            
punct = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'; # string.punctuation less '-'                   
tokensListObj = ["".join([j for j in i if j not in punct]) for i in tokensListObj]
tokensListObj = [itr for itr in tokensListObj if itr] # keep on concat if item in list isnt empty 
```
---

**Step 9:** Count the frequency of total words and negative words as defined by the Loughran and McDonald (2011) dictionary, utilizing our user-defined functions. First, find the intersection of the vector of words that belong to both an earnings call and the master word list. The function only outputs a unique vector of words. So we feed the vector of overlapping words and the earnings call into our user-defined function earlier to output a hash table where the words are the keys and their frequencies of usage as another column. Lastly, traverse through all firms in a calendar quarter and output each computation to the data structure panda. Then you can just divide the number of negative words in each transcript by the total number of word in that transcript to calculate a negative sentiment level and from there calculate the change in the sentiment level between quarters once you output the rest of the data set (lines 246 -
255).

```python
tmpWordsList = list(set(tokensListObj) & set(master_list)) 
tokensNmasterList = tmpWordsList

if not tmpWordsList:
    tmpInt = 0
else:
    tmpDfObj = _out_word_freq1(tmpWordsList, tokensListObj)
    masterWordsDsDictObj = tmpDfObj
    tmpInt = sum(tmpDfObj.values())
masterCnt = tmpInt                   
```

---

Copyright © 2020 by S&P Global Market Intelligence, a division of S&P Global Inc. All
rights reserved. 
