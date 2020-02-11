##########################################################################################################################################################
#
# README - As of Sep. 5, 2017 by Frank Zhao, Quantamental Research Group at S&P Global Market Intelligence 
# 1. Fully working code to generate the following for each stock's earnings call transcript 
#       1.1 year, calendar quarter, earnings call date, CIQ stock id 
#       1.2 total tokens count, total word tokens count, positive word token count, negative word token count, litigious word token count, fog index 
# 2. Change pathways to your own - there are six places to change
# 		2.1 lines 34, 43, 51, 58, 65, 191
# 3. For the first run, a list of polysyllabic words (3+ syllables) is generated which takes 120s from CMU open source dictionary using phonemes
#       3.1 for subsequent runs, just save this list if you don't change the syllable count cutoff 
# 4. To make it easy initially: 
#       4.1 code is set to traverse through 3 firms' transcripts each calendar qtr
#       4.2 to run all firms just change 3 to length of all unique stocks (line 205)
#
##########################################################################################################################################################





##########################################################################################################################################################  
# import libraries  
import os                 # import the os module 
import pandas as pd       # using pandas for data structure 
import nltk               # nlp library
import time               # time module can be used now e.g., time.time()





##########################################################################################################################################################   
# set path
fpath                                                                                   = 'C:/Users/fzhao/Desktop/NLP/rawData/'
os.chdir(fpath) # chg working directory to fpath                                         



                                                                                                                                                                     

##########################################################################################################################################################                                                                  
# initialize word lists, dict, negation list etc ...                                                                                            
fn                                                                                      = 'wordLists\\lmMasterList.txt' # input file
tmpWordListPandaObj                                                                     = pd.read_csv(fn, sep='\t', header=None) # read in tab-delimited text file with no header
tmpWordListPandaObj.columns                                                             = ['master'] 		# rename cols 
master_list                                                                             = list(tmpWordListPandaObj.master)    
master_list                                                                             = [ itr for itr in master_list if not isinstance(itr,float) ]                                                                                                                                                                                                                                           
master_list                                                                             = [itr.lower() for itr in master_list] # make all lowercase

                                                                                           
fn                                                                                      = 'wordLists\\litList2009.txt' # input file
tmpWordListPandaObj                                                                     = pd.read_csv(fn, sep='\t', header=None) # read in tab-delimited text file with no header
tmpWordListPandaObj.columns                                                             = ['litigious'] 		# rename cols 
litigious_list                                                                          = list(tmpWordListPandaObj.litigious)                                                         
litigious_list                                                                          = [itr.lower() for itr in litigious_list] # make all lowercase


fn                                                                                      = 'wordLists\\negList2009.txt' # input file
tmpWordListPandaObj                                                                     = pd.read_csv(fn, sep='\t', header=None) # read in tab-delimited text file with no header
tmpWordListPandaObj.columns                                                             = ['negative'] 		# rename cols 
negative_list                                                                           = list(tmpWordListPandaObj.negative)  
negative_list                                                                           = [itr.lower() for itr in negative_list] # make all lowercase


fn                                                                                      = 'wordLists\\posList2009.txt' # input file
tmpWordListPandaObj                                                                     = pd.read_csv(fn, sep='\t', header=None) # read in tab-delimited text file with no header
tmpWordListPandaObj.columns                                                             = ['positive'] 		# rename cols 
positive_list                                                                           = list(tmpWordListPandaObj.positive)  
positive_list                                                                           = [itr.lower() for itr in positive_list] # make all lowercase
     
                                                                                           
negation_list                                                                           = ['no', 'not', 'none', 'neither', 'never', 'nobody'];                                                                                             
      
myDict                                                                                  = nltk.corpus.cmudict.dict()  




                                                   
##########################################################################################################################################################  
## user defined funcs 

# check whether a word from list2 is in list1 then count the frequency of that word
def _out_word_freq1(list1, list2):
    wordFreqDictObj                                                                     = {}
    for item in list2: 
        if item in list1: 
            wordFreqDictObj[item]                                                       = wordFreqDictObj.get(item, 0) + 1
    return wordFreqDictObj



# for pos words only - dont cnt words that have a negation in one of three places preceding it           
def _out_word_freq2(list1, list2, negation_list): # _out_word_freq2(tmpWordsList, tokensListObj, negation_list) 
    wordFreqDictObj                                                                     = {}
    for index, item in enumerate(list2):
        if item in list1:
            if index == 0:
                wordFreqDictObj[item]                                                   = wordFreqDictObj.get(item, 0) + 1
            elif index == 1:
                if list2[index-1] not in negation_list:
                    wordFreqDictObj[item]                                               = wordFreqDictObj.get(item, 0) + 1               
            elif index == 2:
                if list2[index-1] not in negation_list and list2[index-2] not in negation_list:
                    wordFreqDictObj[item]                                               = wordFreqDictObj.get(item, 0) + 1
            elif index >= 3:
                if list2[index-1] not in negation_list and list2[index-2] not in negation_list and list2[index-3] not in negation_list: 
                    wordFreqDictObj[item]                                               = wordFreqDictObj.get(item, 0) + 1
            else:
                print('error')
    return wordFreqDictObj



# calc avg words per sentence
def _avgWordsPerSent(dsRawSeriesObj):
    outDfObj                                                                            = pd.DataFrame( columns=('cnt','totalSent') )
    
    sent_tokenize_list                                                                  = nltk.sent_tokenize(dsRawSeriesObj)
    tot_num_sent                                                                        = len(sent_tokenize_list)
    
    itr                                                                                 = 0
    while itr < len(sent_tokenize_list):
        tmp1                                                                            = sent_tokenize_list[itr].split()
        tmp2                                                                            = ["".join([j for j in i if j not in punct]) for i in tmp1]
        outDfObj.loc[len(outDfObj)]                                                     = [ len(tmp2), len(sent_tokenize_list) ]
     
        itr                                                                             = itr + 1
    
    avgWordsPerSent                                                                     = outDfObj['cnt'].sum() / tot_num_sent
    
    return avgWordsPerSent



# identify a list of words with certain # of syllables or greater from CMU open source dict using phonemes 
def _createListOfPollySyllabicWords(myDict, syllableCutoff):
    outDfObj                                                                            = pd.DataFrame( columns=('w','cnt') )
    
    for my_var in myDict:
        
        tmpCnt                                                                          = [len(list(y for y in l if y[-1].isdigit())) for l in myDict[my_var]]
        tmpCnt                                                                              = tmpCnt[0]
        
        if tmpCnt >= syllableCutoff:
            outDfObj.loc[len(outDfObj)]                                                 = [my_var, tmpCnt]
            print(my_var)


    polysyllabic_list                                                                   = list(outDfObj['w'])  
    polysyllabic_list                                                                   = [itr.lower() for itr in polysyllabic_list] # make all lowercase
    
    
    ## save list after the first run if the syllable count cutoff isn't revised
    # fpath                                                                             = 'C:/Users/fzhao/Desktop/NLP/rawData/wordLists'                                                                                                                                 
    # fn                                                                                = 'polysyllabicList.txt' # input file
    # outDfObj['w'].to_csv(fn, sep='\t', index=False)    
    

    return polysyllabic_list








##########################################################################################################################################################  
## main  

# initialize diff params
yrVec                                                                                   = [i for i in range(2008, 2018)]
qtrVec                                                                                  = [1,2,3,4]

#declare column names for the dataframe  
outDfObj                                                                                = pd.DataFrame( columns=('yr', 'qtr', 'ecDt', 'stockId', 'totWords', 'totWordsMasterList', 'posWordsCnt', 'negWordsCnt', 'litWordsCnt', 'fogIdx' ) )

polysyllabic_list                                                                       = _createListOfPollySyllabicWords(myDict, 3) # 3 syllables+



start_time                                                                              = time.time(); # record time when a piece of code is executed 
yrItr                                                                                   = 0
while yrItr < len(yrVec):
    
    qtrItr                                                                              = 0
    while qtrItr < len(qtrVec): 
        
        #creating filename to read in
        fn                                                                              = str('C:\\Users\\fzhao\\Desktop\\NLP\\rawData\\transcriptsAll\\sp9_q' + str(qtrVec[qtrItr]) + '_' + str(yrVec[yrItr])  + '.txt') # input file
       
        #check file exists                                                                          
        if os.path.isfile(fn) and os.stat(fn).st_size != 0:
            tmpPandaObj                                                                 = pd.read_csv(fn, sep='\t', header=None)        # read in tab-delimited text file with no header
            tmpPandaObj.columns                                                         = ['stockId','dt','hhmm','seq','ecalls']        # rename cols 

                      
            # unique stock vec where stockId is one of the columns and apply the mthd unique to it 
            uniqueStockIdVec                                                            = tmpPandaObj.stockId.unique() # pandaObj with columnName with method to panda obj                                                  

                                                                                                                                                      
            ## traverse through all the unique ids                                                                                                 
            sItr                                                                        = 0 # stock itr vec 
            while sItr < 3: #len(uniqueStockIdVec):
                
                # assign stock i data to tmpDs
                thisStockDsPandaObj                                                     = tmpPandaObj.loc[tmpPandaObj['stockId'] == uniqueStockIdVec[sItr]]
                
                # loop through dt(t) for stock(i) 
                uniqueDtVec                                                             = thisStockDsPandaObj.dt.unique() # pandaObj with columnName with method to panda obj           
                dItr                                                                    = 0
                while dItr < len(uniqueDtVec):
          

                    # identify date for stock i 
                    thisStockThisDtDsPandaObj                                           = thisStockDsPandaObj.loc[tmpPandaObj['dt'] == uniqueDtVec[dItr]] 
            
                    # sort by sequence of the calls 
                    thisStockThisDtDsPandaObj                                           = thisStockThisDtDsPandaObj.sort_values(['seq'], ascending=[True])    
            
            
            
                    #########################################################################################################################
                    # three values to keep track of 
                    thisStockId                                                         = uniqueStockIdVec[sItr]
                    ecDt                                                                = uniqueDtVec[dItr]
                    dsRawSeriesObj                                                      = "".join(thisStockThisDtDsPandaObj['ecalls']);
                                             

                   
                    #########################################################################################################################
                    # nltk library methods + text preprocessing
                    dsRawSeriesObj                                                      = dsRawSeriesObj.replace("n't"," not")   
                    tokensListObj                                                       = nltk.word_tokenize(dsRawSeriesObj) # tokenize all words 
                    tokensListObj                                                       = [itr.lower() for itr in tokensListObj] # make all lowercase
            
                    punct                                                               = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'; # string.punctuation less '-'                   
                    tokensListObj                                                       = ["".join([j for j in i if j not in punct]) for i in tokensListObj]
                    tokensListObj                                                       = [itr for itr in tokensListObj if itr] # keep on concat if item in list isnt empty 



                    #########################################################################################################################
                    # master word list 
                    tmpWordsList                                                        = list(set(tokensListObj) & set(master_list)) 
                    tokensNmasterList                                                   = tmpWordsList

                    if not tmpWordsList:
                        tmpInt                                                          = 0
                    else:
                        tmpDfObj                                                        = _out_word_freq1(tmpWordsList, tokensListObj)
                        masterWordsDsDictObj                                            = tmpDfObj
                        tmpInt                                                          = sum(tmpDfObj.values())
                    masterCnt                                                           = tmpInt                   


                    
                    # positive word list
                    tmpWordsList                                                        = list(set(tokensListObj) & set(positive_list))                                                                       
                    tokensNposList                                                      = tmpWordsList
                    
                    if not tmpWordsList:
                        tmpInt                                                          = 0
                    else:
                        tmpDfObj                                                        = _out_word_freq2(tmpWordsList, tokensListObj, negation_list) 
                        posWordsDsDictObj                                               = tmpDfObj
                        tmpInt                                                          = sum(tmpDfObj.values())
                    posCnt                                                              = tmpInt           



                    # negative word list
                    tmpWordsList                                                        = list(set(tokensListObj) & set(negative_list))                                                                      
                    tokensNnegList                                                      = tmpWordsList
                    if not tmpWordsList:
                        tmpInt                                                          = 0
                    else:
                        tmpDfObj                                                        = _out_word_freq1(tmpWordsList, tokensListObj)            
                        negWordsDsDictObj                                               = tmpDfObj
                        tmpInt                                                          = sum(tmpDfObj.values())
                    negCnt                                                              = tmpInt               



                    # litigious word list
                    tmpWordsList                                                        = list(set(tokensListObj) & set(litigious_list))                                                                        
                    tokensNlitList                                                      = tmpWordsList
                    if not tmpWordsList:
                        tmpInt                                                          = 0
                    else:
                        tmpDfObj                                                        = _out_word_freq1(tmpWordsList, tokensListObj)  
                        litWordsDsDictObj                                               = tmpDfObj
                        tmpInt                                                          = sum(tmpDfObj.values())
                    litCnt                                                              = tmpInt            
            





                                        


                    #########################################################################################################################
                    ## calc avgWordsPerSent, the proportion of words with 3+ syllables in a text and finally fog idx
                    avgWordsPerSent                                                     = _avgWordsPerSent(dsRawSeriesObj)

                    # polysyllabic word list
                    tmpWordsList                                                        = list(set(tokensListObj) & set(polysyllabic_list))                                                                        
                    tokensNpolyList                                                     = tmpWordsList
                    if not tmpWordsList:
                        tmpInt                                                          = 0
                    else:
                        tmpDfObj                                                        = _out_word_freq1(tmpWordsList, tokensListObj)  
                        polyWordsDsDictObj                                              = tmpDfObj
                        tmpInt                                                          = sum(tmpDfObj.values()) 
                    polyCnt                                                              = tmpInt            
                    pctWordsWith3PlusSyllables                                          = polyCnt / len(tokensListObj)
                   
                    fogIdx                                                              = 0.4 * ((avgWordsPerSent) + 100 * (pctWordsWith3PlusSyllables))                                                                                                                                                                                                                                                               
                    
                        
                    
                    

                    #########################################################################################################################
                    outDfObj.loc[len(outDfObj)]                                         = [ yrVec[yrItr], qtrVec[qtrItr], ecDt, thisStockId, len(tokensListObj), masterCnt, posCnt, negCnt, litCnt, fogIdx]
                                       
                    # keeping track of multiple transcripts for stock i 
                    dItr                                                                = dItr + 1 # lined up with dItr while  
                ############### while through each unique date for stock i         

                    

                # keeping track of each stock
                sItr                                                                    = sItr + 1 # lined up with sItr while
                print(yrVec[yrItr], qtrVec[qtrItr], sItr, thisStockId) 
            ############### while through each stock       
                
                
 
        ############### end of if os.path.isfile(fn):
        # while through qtrs
        qtrItr                                                                          = qtrItr + 1
        
        
        
    ############### end of while qtrItr < 4:     
    # while through yrs   
    yrItr                                                                               = yrItr + 1    





# for testing purposes 
print("--- %s seconds ---" % (time.time() - start_time))





# convert sci notation to int  
outDfObj['yr']                                                                          = outDfObj['yr'].astype(int)
outDfObj['ecDt']                                                                        = outDfObj['ecDt'].astype(int)
outDfObj['stockId']                                                                     = outDfObj['stockId'].astype(int)
outDfObj['totWords']                                                                    = outDfObj['totWords'].astype(int)
outDfObj['totWordsMasterList']                                                          = outDfObj['totWordsMasterList'].astype(int)





################## end #############################################################################################################################################





