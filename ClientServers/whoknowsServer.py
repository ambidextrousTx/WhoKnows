#! /usr/bin/python
from multiprocessing import Process
import socket
import sys
import os

import cPickle

from cosineSim import cosineSim

#Ravi's code - TODO: method to return dictionary from string!
from nltk_get_tokens import generate
#from collections import ounter

#open the persisted indexes
#This is a server to a tfidf index
#TODO: create and shelve these indexes
#We need the inverted index to weight the query terms
idf = open('big/idfIndex.db', 'r')
tfidf = open('big/tfidfIndex.db', 'r')
idfIndex = cPickle.load(idf)
tfidfIndex = cPickle.load(tfidf)
#TODO: add data index that will return JSON to browser



BUFLEN = 256

#TODO: TEST 
def queryVector (rawQuery):
    cleanQuery = generate(rawQuery)
    tokens = cleanQuery.split(' ')
    doc = {}
    
    queryTfidf = {}
    for token in tokens:
        currentVal = doc.get(token, 0)
        newVal = currentVal + 1
        doc[token] = newVal

    for tok in doc.keys():
        #if (tok in idfIndex):
            #tokenIdf = idfIndex[token]
            #tokenTf = doc[token]
                #score = tokenIdf * tokenTf
            #queryTfidf[tok] = score
        tokenIdf = idfIndex.get(token, 0)
        tokenTf = doc.get(token, 0)
        score = tokenIdf * tokenTf
        queryTfidf[tok] = score
        
            
    return queryTfidf

#return the data for this individual
#def getPersonData:


# handle every client in a separate subprocess
# to facilitate multiple clients simultaneously
def handleClientRequest(info, sock_obj, data_root_directory):
    print 'Accepted connection from client: '
    print '%s, port: %s' % (info[0], info[1])
    print '\n'
    data = ''
#        while(True):
    tempData = sock_obj.recv(BUFLEN)
        #if not tempData:
         #   break
    data += tempData

    #this is a query string 
    #print 'The data sent to the server was: %s' % data
    #parse query and get a dictionary query[word] = tfidf value
    query = queryVector(data)#should this be salsa.querySalsa(data)?
    #print 'query vector is: %s' %str(query) 
    #result = [(56193, 'Page'), (35272, 'sheet'), (6171, 'side')]
    #now compare to all vectors and get the top one
    scores = []
    for person in tfidfIndex.keys():
        #get the query's similarity with every vector
        vector = tfidfIndex[person]
        #TODO: which cosineSim method to use
        similarity = cosineSim(query, vector)
        scores.append((person, similarity))

    #now rank the scores using lambda function
    ranked = sorted(scores, key = lambda z : z[1], reverse = True)

    #return the top five 
    output = []
    #for i in range (0, 10):
        #output += '|' + str(ranked[i])
    for i in range(0, 10):
        output.append(str(ranked[i][0]))
        
    output = ' '.join(output)
        
    if (output != ''):
        sock_obj.sendall(output+"\n")
    else:
        empty = 'Nothing was returned...'
        sock_obj.sendall(empty+"\n")
    
        print 'The top results are: %s' % output    
    #Update: can't send a list - needs to be a single string (currently | delimited)
        sock_obj.sendall(output+"\n")
        print 'Closing Connection'
        sock_obj.close()

        #fDirName = data_root_directory + '/' + str(info[0]) + '_' + str(info[1]) + '/'
        #os.mkdir(fDirName)
        #os.chdir(fDirName)
        #f = open('data.txt', 'wb')
        #f.write(data)
        #f.close()

        #os.chdir('..')
        #print 'Data transferred to %s' % fDirName

def startServer(port_number, data_root_directory):
    server_sock = socket.socket()
    server_sock.bind(('127.0.0.1', int(port_number)))
    server_sock.listen(0)
    while(True):
        # Accept a connection
        sock_obj, info = server_sock.accept()
        # Create a subprocess to deal with the client
        process = Process(target = handleClientRequest, args=(info, sock_obj, data_root_directory))
        process.start()
        process.join()

def error():
    print 'Usage: ./server.py port_number data_root_directory'
    print 'Exiting ... '
    sys.exit()

def main():
    if len(sys.argv) != 3:
        error()
    startServer(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
