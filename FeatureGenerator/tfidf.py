#!/usr/bin/python

#tfidf module which takes two vectors and returns cosine similarity
#TODO: change this into a module that builds and persists an idfIndex, and a tfidfIndex

from math import log, sqrt
import cPickle
import shelve


#TODO: not implemented!!
#This code uses Ravi's parsing module
#TODO: move to server module
#def buildQueryVector(query): 

#TODO: move to ___main___?
def persistIndexes(dictMatrix):
    idfIndex, tfIndex = buildIndexes(dictMatrix)
    tfidfInd = tfidfIndex(idfIndex, tfIndex)    
    
    # now persist using cPickle - note: this can also be done in the interpreter
    invIndexFile = open('idfIndex.db', 'w')
    tfidfIndexFile = open('tfidfIndex.db', 'w')
    cPickle.dump(idfIndex, invIndexFile)
    cPickle.dump(tfidfInd, tfidfIndexFile)  
 
    # Ambidextrous: changing to shelve because
    # that is what I know :P
    # pers_obj_1 = shelve.open('tfidfIndex.db')
    # pers_obj_2 = shelve.open('idfIndex.db')
    # pers_obj_1['1'] = tfidfInd
    # pers_obj_2['1'] = idfIndex
    # pers_obj_1.close()
    # pers_obj_2.close()

#build the tf and the idf dictionaries
def buildIndexes(dictMatrix):

    #this returns a dictionary of 
    #remember that we'll need the global doc count  
    globalDocCount = len(dictMatrix.keys())
    idfIndex = {} 
    tfIndex = {}    

    for person in dictMatrix.keys():
        singleDocHash = {}
        # Ambidextrous: changed; added key 'tokens'
        for word in dictMatrix[person]['tokens']:
            currentVal = singleDocHash.get(word, 0)
            singleDocHash[word] = currentVal + 1        
        #add the doc vector to the tf matrix
        tfIndex[person] = singleDocHash         

        #+1 for each key in the doc
        for key in singleDocHash.keys():
            print 'key: ' + str(key)
            currentVal = idfIndex.get(key, 0)
            print 'currentVal is: ' + str(currentVal)
            currentVal += 1
            print 'currentVal is: ' + str(currentVal)
            idfIndex[key] = currentVal 

    #calulate the final idf values  
    for word in idfIndex.keys():
        rawVal = idfIndex[word]
        print 'word: ' +str(word) + ' rawVal: ' + str(rawVal)   
        print 'globalDoc: ' + str(globalDocCount)
        finalVal = log(globalDocCount/rawVal) + 1       
        idfIndex[word] = finalVal

    return (idfIndex, tfIndex)


def tfidfIndex(idfIndex, tfIndex):

    tfidfIndex = {} 
    for person in tfIndex.keys():
        personHash = {}
        for word in tfIndex[person].keys():
            if (word in idfIndex):
                idfVal = idfIndex[word]
                #TODO: fix errors here
                tfVal = tfIndex[person][word]
                tfidfVal = idfVal * tfVal                       
                personHash[word] = tfidfVal
        tfidfIndex[person] = personHash

    return tfidfIndex   
        
