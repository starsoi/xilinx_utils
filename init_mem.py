import os
import sys

def main():
	if len(sys.argv) < 4:
		print 'init_mem <bmmfile> <memfile> <bitfile>'
		return
		
	bmmfile = sys.argv[1]
	memfile = sys.argv[2]
	bitfile = sys.argv[3]
	bitfile_= bitfile.split('.')[0] + '_inited.bit'

	os.system('data2mem -bm %s -bd %s -bt %s -o b %s' % (bmmfile, memfile, bitfile, bitfile_))

	print 'DONE: BIT file initialization -> ' + bitfile_
	
if __name__ == '__main__':
	main()