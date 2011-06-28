test_mem = open('test.mem', 'wb')
test_mem.write('@00000000\n')

for i in range(0xffff):
	test_mem.write('%08x\n' % i)
