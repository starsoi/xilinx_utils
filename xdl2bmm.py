'''
example:
in coregen:
	without optimization (all memory block use the same primitive)
	word width: 32 bits
	depth: 65536
	--> memory capacity: 256 KB
generated core:
	read/write port width of each block ram is 2-bit
	arrangement of the block rams:
		   Bit 31 - Bit 24          Bit 7 - Bit 0  
		| 60 | 56 | 52 | 48 | ... | 12 | 8  |  4 |  0 |
		| 61 | 57 | 53 | 49 | ... | 13 | 9  |  5 |  1 |
		| 62 | 58 | 54 | 50 | ... | 14 | 10 |  6 |  2 |
		| 63 | 59 | 55 | 51 | ... | 15 | 11 |  7 |  3 | 
'''
import sys
import re

def parse(xdl):
	try:
		file_xdl = open(xdl, 'r')
	except IOError:
		print 'FAILED: Open xdl file: ' + xdl
		sys.exit()
		
	re_ram = re.compile('^inst\s"[\w/\.]+ramloop\[\d+\][\w/\.]+"')
	re_ram_i = re.compile('\[\d+\]')
	re_ram_pl = re.compile('placed\s[\w]+\s[\w]+')
	re_ram_w = re.compile('READ_WIDTH_A::\d+')
	
	ram_name = {}
	ram_w = 0
	
	s = file_xdl.readline()
	while s != '':
		res_re = re_ram.search(s)
		if res_re:
			inst_name = res_re.group()
			idx = int(re_ram_i.search(inst_name).group()[1:-1])
			placed = re_ram_pl.search(s).group().split()[2].split('_')[1]
			ram_name[idx] = (inst_name.split()[1][1:-1], placed) #{idx:(inst_name, placed string)}
			#print idx, ':', ram_name[idx], 
			ss = file_xdl.readline()
			while ram_w == 0:
				res_re = re_ram_w.search(ss)
				if res_re:
					ram_w = int(res_re.group().split('::')[1])
					print 'READ_WIDTH_A:', ram_w
					break
				ss = file_xdl.readline()
		s = file_xdl.readline()
		
	if file_xdl:
		file_xdl.close()
	
	return ram_name, ram_w
	
		
def xdl2bmm(xdl):
	DATA_WIDTH = 32
	RAM_SIZE = 32*1024 #(RAMB32)
	ram_name, ram_w = parse(xdl)
	n_x = DATA_WIDTH / ram_w
	n_y = len(ram_name) / n_x
	block_size = RAM_SIZE * n_x / 8

	ram_k = ram_name.keys()
	ram_k.sort()

	bmm = 'ADDRESS_SPACE pr_mem RAMB32' + \
		  ' [0x%08x:0x%08x]\n' % (0, block_size * n_y - 1)
	for i in range(n_y):
		bmm += '\tBUS_BLOCK\n'
		for j in range(n_x):
			idx = ram_k[(n_x-j-1)*n_y+i]
			bmm += '\t\t' + ram_name[idx][0] + \
				   ' [%d:%d]' % (DATA_WIDTH-j*ram_w-1, DATA_WIDTH-j*ram_w-1 -ram_w+1) + \
				   ' PLACED = %s;\n' % ram_name[idx][1]
				   #' OUTPUT = ram%d.mem;\n' % idx 
				   #' PLACED = %s;\n' % ram_name[idx][1]
				   
				   
		bmm += '\tEND_BUS_BLOCK;\n'
	bmm += 'END_ADDRESS_SPACE;'
	
	try:
		open(xdl.split('.')[0] + '.bmm', 'w').write(bmm)
	except IOError:
		print 'FAILED: Write bmm file.'
		sys.exit()
	print 'DONE: BMM file generation.'
	
def main():
	xdl2bmm(sys.argv[1])
	
if __name__ == '__main__':
	main()