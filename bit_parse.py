import sys
import array
from packets import *
from bitstream_parser import *

def main():
	if len(sys.argv) < 2:
		print 'bit_parse.py <bitfile.bit>'
		sys.exit()
	
	print 'Parsing...'
	parser = bitstream_parser(sys.argv[1])

	for i in range(len(parser.pktlist)):
		p = parser.pktlist[i]
		if p.word_cnt == 1:
			print '%08x: %s: %02x%02x%02x%02x' % (p.hdr_raw, str(p), p.data[0], p.data[1], p.data[2], p.data[3])
		else:
			print '%08x: %s' % (p.hdr_raw, str(p))

	
		
if __name__ == '__main__':
	main()
