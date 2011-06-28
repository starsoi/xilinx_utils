import sys
from array import *

def bitswap(byte):
	zerofill = {1:'0000000', 2:'000000', 3:'00000', 4:'0000', 5:'000', 6:'00', 7:'0', 8:''}
	bin_str = bin(byte)[2:]
	bin_str = zerofill[len(bin_str)] + bin_str
	bin_str = bin_str[::-1]
	return eval('0b' + bin_str)

def bit2ascii(bit):
	try:
		file_bit = open(bit, 'rb')
	except IOError:
		print 'FAILED: Open bit file: ' + bit
		return
	
	while ord(file_bit.read(1)) != 0xff:
		pass
	
	CONFIG_DATA_OFFSET = 27
	
	file_bit.seek(file_bit.tell() + CONFIG_DATA_OFFSET)
	bitstream = array('B')
	bitstream.fromstring(file_bit.read())
	
	#bit_ascii = '@00000000\n'
	bit_ascii = ''
	for i in range(0, len(bitstream), 4): # 32-bit word
		bit_ascii += '%02x%02x%02x%02x\n' % (bitswap(bitstream[i]), 
											 bitswap(bitstream[i+1]), 
											 bitswap(bitstream[i+2]), 
											 bitswap(bitstream[i+3]))
	return bit_ascii
											 
#	try:
#		open(bit.split('.')[0] + '.mem', 'w').write(bit_ascii)
#	except IOError:
#		print 'FAILED: Write mem file.'
#	print 'DONE: MEM file generation.'
	
def main():
	if len(sys.argv) < 2:
		print 'bit2mem.py <bitfile1.bit> <bitfile2.bit> <bitfile3.bit> ...'
		return
		
	FILENAME_OUT = 'bit2mem_out.mem'
	try:
		file_mem = open(FILENAME_OUT, 'w')
	except IOError:
		print 'FAILED: Cannot create MEM file.'
		return
		
	n_bit_file = len(sys.argv) - 1
	file_mem.write('@00000000\n')
	file_mem.write('%08x\n' % n_bit_file)

	for i in range(1, len(sys.argv)):
		bit_ascii = bit2ascii(sys.argv[i])
		file_mem.write(bit_ascii)
		
	file_mem.close()
	print 'DONE: MEM file generation: ' + FILENAME_OUT

if __name__ == '__main__':
	main()