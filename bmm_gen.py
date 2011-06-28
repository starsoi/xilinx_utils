import sys
import os
from xdl2bmm import *

def bmm_gen(ncd):
	os.system('xdl -ncd2xdl ' + ncd)
	xdl2bmm(os.path.split(ncd)[-1].split('.')[0] + '.xdl')

def main():
	bmm_gen(sys.argv[1])
	
if __name__ == '__main__':
	main()