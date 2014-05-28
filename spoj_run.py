#!/usr/bin/python
# 
# Syntax:
#       spoj_run.py <problem> <lang> <source>
#
# Submit file <source> to SPOJ judge as solution of problem with code 
# <problem> using language with code <lang>.


import sys
import time
import SpojApi
import os

#netrc_file="/var/www/html/tgh.nti.tul.cz/py/.netrc"
netrc_file="/home/jb/.netrc"


try:
	log_file=open("log","a")
	log_file.close()
except:
	print ('cannot open to log file: ' + os.getcwd() + '/log')

def log (s):
        # set to True for logging  
	if (False):
		print (s)
		print ('\n')
		try:
			log_file=open("log","a")
			log_file.write(s)
			log_file.write("\n")
			log_file.close()
		except:
			print ('cannot write to log file: ' + os.getcwd() + '/log')


# read params
problem = sys.argv[1]
language = sys.argv[2]
sourcePath = sys.argv[3]


# get source
log ("reading file")
handle = open(sourcePath, 'r')
source = handle.read();



log ("creating api object")
spoj = SpojApi.SpojApi()

log ("logging to spoj")
#success = spoj.login ("tgh_2014", "frnak")
success = spoj.login_with_netrc(netrc_file)
if success == 0:
    exit (101)

log ("submitting solution")
id = spoj.submit (problem, source, language)
if id == -1:
    exit (102)

print 'id=%s' % id
log ("getting result")
data = spoj.get_sub_results(id)

result = spoj.result_strings['compiling']
while (spoj.active_status(result)) :
	time.sleep(0.5)
	data = spoj.get_sub_results(id)
	result = data['result']


print 'date=%s' % data['date']
print 'status=%s' % data['result']
print 'result_full=%s' % data['result_full']
print 'runtime=%s' % data['time']
print 'runmem=%s' % data['mem']
print 'stdio=%s' % data['stdio']
print 'info=%s' % data['test_info']



exit (0);
