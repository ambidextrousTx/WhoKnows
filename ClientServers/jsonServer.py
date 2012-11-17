#! /usr/bin/python
from multiprocessing import Process
import socket
import sys
import os
import json

import cPickle

#Server to the data that we know about people

#one big dictionary of data
infoIndex = open('professor_data.json', 'r')
#infoIndex = cPickle.load(infoIndex)
json_data = json.load(infoIndex)

#TODO: add data index that will return JSON to browser
BUFLEN = 256

#TODO: TEST 
def queryIndex (personId):
	#info = infoIndex[personId]			
	print 'Person id is {0}'.format(personId)

	#TODO
	#Add JSON parsing	
	ind = eval(personId)
	return json_data[ind]

	#return jsonInfo 

def transform(old, new):
	new['email'] = "proftest@gmail.com"
	new['profilepic'] = "default.jpg"
	new['website'] = old['profile_url']
	new['name'] = old['name']

def build_json(data):
	#print 'Data {0}'.format(data)
	results = []
	data_items = data.split(' ')
	#str_bf = ''
	for d in data_items:
		this_dict = queryIndex(d)
		new_dict = {}
		transform(this_dict, new_dict)
		results.append(new_dict)

	wrapped_dict = {}
	wrapped_dict["Results"] = results
	return json.dumps(wrapped_dict)
	

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
	#print 'Data in handleClient: {0}'.format(data)
	#this is a query string 
	#print 'The data sent to the server was: %s' % data
	personInfo = build_json(data)
	
	#output this
	output_people = personInfo    
		
	if (output_people != ''):
		sock_obj.sendall(output_people+"\n")
	else:
		empty = 'Nothing was returned...'
		sock_obj.sendall(empty+"\n")
	
	#Update: can't send a list - needs to be a single string (currently | delimited)
       	sock_obj.sendall(output_people +"\n")
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
