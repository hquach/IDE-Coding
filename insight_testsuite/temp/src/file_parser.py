''' 
Author: Hoa Quach
Due Date: 2/13/2018

Python 2.7.6
'''

import sys, os

def parse_log(filename):
	'''Function to read text file and store selected columns in list'''
	try:
		fields = (line.split('|') for line in open(filename, 'r').readlines())
		
		df = [{ 'id'	:	str(f[7]) + str(f[10][:5]),
				'cmte'	:	str(f[0]),
				'name'	:	str(f[7]),
				'zip_code'	:	f[10][:5],
				'trans_dt'	:	int(f[13][4:]),
				'trans_amt'	:	float(f[14]),
				'other_id'	:	str(f[15]) }
				for f in fields]
		
		return df
	except IOError:
		print("\n Error: Wrong itcont.txt file naming convention or file path\n")
		sys.exit()

def parse_percentile(percentile_filename):
	'''Function to read percentile.txt file and convert to integer'''
	try:
		with open( percentile_filename ) as f_in:
			
			if os.stat( percentile_filename ).st_size == 0:
				print ""
				print 'Error: percentile file is empty.'
				print ""
				sys.exit()
			else:
			    lines = filter(None, (line.rstrip() for line in f_in))
			    percentile = [int(m) for m in lines]
			    
			    return percentile[0]
		    	
		    	try:
		    		first_char = f_in.read(1)
		    	except IOError:
		    		sys.exit()
	except IOError:
		print("\n Error: Wrong percentile.txt file naming convention or file path\n")
		sys.exit()
	except ValueError:
		print "\n Error: percentile.txt file contains an invalid numeric.\n"
		sys.exit()
