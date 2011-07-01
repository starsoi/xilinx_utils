import sys
import array
from packets import *
from bitstream_parser import *
from frame import *

def main():
	if len(sys.argv) < 2:
		print 'bit_parse.py <bitfile.bit>'
		sys.exit()
	
	parser = bitstream_parser(sys.argv[1])
	print 'Parsing...'
	#print_packets(parser)
	print_frames(parser)
	
def print_packets(parser):
	for i in range(len(parser.pktlist)):
		p = parser.pktlist[i]
		if p.get_op() == 'NOP' and i > 0 and parser.pktlist[i-1].get_op() == 'NOP':
			continue

		if p.word_cnt == 1:
			print '%08x: %s: %08x' % (p.hdr_raw, str(p), p.data[0])
			if p.get_reg() == 'FAR':
				frame_addr = frame_address(p.data)
				print frame_addr

		else:
			print '%08x: %s' % (p.hdr_raw, str(p))
		
		if p.is_frame_data:
			print '(...%d frames...)' % len(parser.frames)
						
def print_frames(parser):
	for i in range(len(parser.frames)):
		f = parser.frames[i]
		print '----------- Frame %d -----------' % (i+1)
		if sum(f.raw) == 0:
			print '|            Empty             |'
			print '-------------------------------'
			continue
			
		
		print '640 configuration bits for 10 CLBs ABOVE the HCLK row:'
		for j in range(len(f.f_top)-1, -1, -1):
			print '%08x' % f.f_top[j]
		
		print '640 config. bits for 10 CLBs BELOW the HCLK row:'
		for j in range(len(f.f_bottom)-1, -1, -1):
			print '%08x' % f.f_bottom[j]
			
		print '4 Miscellaneous HCLK configuration bits: %x' % f.hclk_conf
		print '12 ECC bits: %03x' % f.ecc
		print '-------------------------------'
		
if __name__ == '__main__':
	main()
