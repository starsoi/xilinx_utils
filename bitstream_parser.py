import array
from packets import *
from frame import *

FRAME_LENGTH_WORD = 41
CONFIG_DATA_OFFSET = 27 + 6*4 # from dummy ffffffff to SYNC

class bitstream_parser(object):
	def __init__(self, bit):
		try:
			file_bit = open(bit, 'rb')
		except IOError:
			raise 'FAILED: Open bit file: ' + bit
	
		while ord(file_bit.read(1)) != 0xff:
			pass	
			
		self.pktlist = []
		self.frames = []
		
		file_bit.seek(file_bit.tell() + CONFIG_DATA_OFFSET)
		
		
		bitstring = file_bit.read(4)
		
		while bitstring:
			p = packet(array.array('L', bitstring))
			if p.word_cnt > 0:
				p.data.fromstring(file_bit.read(p.word_cnt*4))
				p.data.byteswap()
				
			if p.hdr_type == 0x2:
				p.reg_addr = self.pktlist[-1].reg_addr
			
			if (p.hdr_type == 0x1 and p.get_reg() == 'FAR'):
				frame_addr = frame_address(p.data)
			if (p.hdr_type == 0x1 and p.get_reg() == 'FDRI' and p.word_cnt > 0) or (p.hdr_type == 0x2 and self.pktlist[-1].get_reg() == 'FDRI'):
				# frame data
				p.is_frame_data = True
				for i in range(0, p.word_cnt, FRAME_LENGTH_WORD):
					self.frames.append(frame(p.data[i:i+FRAME_LENGTH_WORD], frame_addr, len(self.frames)))
					
			self.pktlist.append(p)			
			bitstring = file_bit.read(4)
			
		
