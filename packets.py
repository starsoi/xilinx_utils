'''
for Virtex-5 bitstream
'''
import array

class packet(object):
	Header_Type = {0x1:'Type 1', 0x2:'Type 2'}
	Opcode = {0x0:'NOP', 0x1:'Read', 0x2:'Write', 0x3:'Reserved'}
	Register_Type1 =   {0x00:'CRC', 
						0x01:'FAR',
						0x02:'FDRI',
						0x03:'CFDRO',
						0x04:'CMD',
						0x05:'CTL0',
						0x06:'MASK',
						0x07:'STAT',
						0x08:'LOUT',
						0x09:'COR0',
						0x0A:'MFWR',
						0x0B:'CBC',
						0x0C:'IDCODE',
						0x0D:'AXSS',
						0x0E:'COR1',
						0x0F:'CSOB',
						0x10:'WBSTAR',
						0x11:'TIMER',
						0x13:'UNKOWN_REG',
						0x16:'BOOTSTS',
						0x18:'CTL1',
						0xFF:'FF'}

	def __init__(self, hdr):
		if type(hdr) is not array.array: # expected that p is of type array('I')
			raise 'Array expected'
		
		self.data = array.array('I')
		
		hdr.byteswap()
		hdr = hdr[0]

		self.hdr_type = (hdr >> 29) & 0x7
		if self.hdr_type == 0x1:
			self.op = (hdr >> 27) & 0x3
			self.reg_addr = (hdr >> 13) & 0x1F
			self.word_cnt = hdr & 0x3ff
		elif self.hdr_type == 0x2:
			self.op = (hdr >> 27) & 0x3
			self.word_cnt = hdr & 0x7ffffff
			
		self.hdr_raw = hdr
		self.is_frame_data = False

	def get_reg(self):
		return packet.Register_Type1[self.reg_addr]
		
	def get_op(self):
		return packet.Opcode[self.op]
			
	def __str__(self):
		return self.__repr__()
			
	def __repr__(self):
		if self.hdr_type == 0x1: #type 1
			if self.op == 0x0: #nop
				return 'Type 1 NO OP'
			elif self.op == 0x1: #read
				return 'Type 1 Read %d word(s) from %s' % (self.word_cnt, packet.Register_Type1[self.reg_addr])
			elif self.op == 0x2: #write
				return 'Type 1 Write %d word(s) to %s' % (self.word_cnt, packet.Register_Type1[self.reg_addr])
		elif self.hdr_type == 0x2: #type 2
			return 'Type 2 Data %d words' % (self.word_cnt)
