''' 
Author: Hoa Quach
Due Date: 2/13/2018

Python 2.7.6
'''

from decimal import getcontext, Decimal
getcontext().prec = 3

from file_parser import *

def cumulative(lists):
	'''Function to calculate cumulative values in a given list'''
	cu_list = []
	length = len(lists)
	cu_list = [sum(lists[0:x + 1]) for x in range(0, length)]
	
	return cu_list

def filter_by_2017(filename):
	_filter_2017 = [s for s in parse_log(filename) 
	if s['trans_dt'] == 2017 and s['other_id'] == '' and s['cmte'] != '' and s['zip_code'] != '' and s['name'] != '' and s['trans_amt'] != '' and len(s['zip_code']) < 6 and len(s['cmte']) == 9 and s['zip_code'].isdigit() and s['trans_dt'] != '']
	
	return _filter_2017

def filter_by_2018(filename):
	'''Function to filter columns in 2018 data set'''
	_filter_2018 = [s for s in parse_log(filename) 
	if s['trans_dt'] == 2018 and s['other_id'] == '' and s['cmte'] != '' and s['zip_code'] != '' and s['name'] != '' and s['trans_amt'] != '' and len(s['zip_code']) < 6 and len(s['cmte']) == 9 and s['zip_code'].isdigit() and s['trans_dt'] != '']
	
	return _filter_2018

def calc_nearest_rank(list2, p, percentile_filename):
	'''Function to calculate the nearest-rank from given list and percentile value'''
	p = len(list2) # N-size
	percentile_value = round((Decimal(parse_percentile( percentile_filename ))/ Decimal(100)) * Decimal(p)) + 0.5
	percentile_value = int(percentile_value - 1)

	return percentile_value

def hashTable(list1, list2, list3):
	'''Function to create hash table to search for repeat donors; created 'id' as unique identifier during file parser'''
	for donor in list1:
		list2[donor['id']] = donor

	for donor in list3: 
	    if donor['id'] in list2.items(): 
	        donor['zip_code'] = list2[donor['id']].get('zip_code')


def constraints(percentile_filename):
	'''[OPTIONAL] function to add constraint conditionals to percentile text file'''
	percentile = parse_percentile(percentile_filename)
	if percentile > 100:
		print ""
		print "Error: Your percentile value is %s. Highest percentile value is 100." % percentile
		print ""
		sys.exit()
	elif percentile == 0:
		print ""
		print "Error: The percentile file is %s. Lowest percentile value is 1." % percentile
		print ""
		sys.exit()
	elif percentile < 0:
		print ""
		print "Warning: The percentile file is %s. Setting percentile to lowest acceptable value of 1." % percentile
		print " "
		sys.exit()	        
