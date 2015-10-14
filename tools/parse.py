#!/usr/bin/env python
''' Parse sis3316 raw (binary) data stream, get events ordered by timestamp. '''

import sys,os
import argparse
from struct import unpack
import io # BufferedReader


__fields__ = ('npeak','peak','info',
	'acc1','acc2','acc3','acc4','acc5','acc6','acc7','acc8',
	'maw_max','maw_after_trig','maw_before_trig',
	'raw', 'maw_raw',
	'e_start', 'e_max', #Start Energy value, Max Energy value
	'avg_cnt', 'avg_raw', #Averaging mode
	#----
	'baseline', 'charge', #Peak/Charge mode
	)
	
	
#chid_initial
#from operator import itemgetter
#newlist = sorted(list_to_be_sorted, key=itemgetter('name')) 
#io.BufferedReader
#peek([n]), read, read
#reader = io.open(sys.stdin.fileno())

# parse

	
class Parse:
	MAX_EVENT_LENGTH = (18 + 1022) * 4 + (65536+65534) * 2 # (hdr+maw_data) * word_sz + (raw+avg) * halfword_sz
	
	""" Parse an events file, return a single event at once """
	def __init__(self, filename, fields):
		self._reader = io.open(filename, 'rb') #not iterable if stdin!, 'seek' and it's friends won't work
		if self._reader.isatty():
			raise ValueError('You are trying to read data from a terminal.')
		
		self._fields = fields
			#TODO: check fields are valid
	
	def __iter__(self):
		return self
		
	def _guess_event_sz(self):
		""" Try to calculate size of the next event. Return a size or raise ValueError/StopIteration. """
		# Since Raw data format is a bit "overoptimized"... 
		# We don't know event size for channels in each group, and there is no MAW length field,
		# so it's not easy at all to calculate actual event length looking on data...
		#
		# Reasonable workaround is to try to find next higher timestamp value, since it changes
		# only once in 17 seconds (on 250 MHz).
		
		
		return 140
		
	def _peek_event(self, sz, fields):
		sz = self._guess_event_sz()
		
	def _cache_lookup(self, word):
		return None
		
		
	def next(self):
		""" Return events from a continuous redout (in general, from single memory bank), ordered by timestamp.
		When events are rare, consecutive readouts could be merged. """
		reader = self._reader
		fields = self._fields
		
		data = []
		
		while True:
			
			return 42
			
			header = reader.peek(4)
			if len(header) < 4:
				raise StopIteration #no data
			
			chan_fmt = header[0:2]
			
			sz = self._cache_lookup(chan_fmt)
			if not sz:
				sz = self._guess_event_sz()
			
			try: 
				evt = self._peek_event(sz, fields)
				
			except ValueError: #wrong event data
				#shift a byte
				continue
				
			
			
		return data
			
			
	
	__next__ = next
	

def main():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('infile', nargs='?', type=str, default='-', help="raw data file (stdin by default)")
	parser.add_argument('-o','--outfile', type=argparse.FileType('w'), default=sys.stdout, help="redirect output to a file")
	parser.add_argument('-F','--fields', nargs='+', type=str, default=('ts','raw'), help="default is \"--fields ts raw\". Valid field names are: %s." % str(__fields__) )
	args = parser.parse_args()
	
	fields = ('ts','raw')
	
	if args.infile is '-':
		args.infile = sys.stdin.fileno()
	
	try:
		p = Parse(args.infile, fields)
		
	except ValueError as e:
		sys.stderr.write("Err: %s \n" % e)
		exit(1)
	
	for events in p:
		print(events)
	
	
if __name__ == "__main__":
    main()
