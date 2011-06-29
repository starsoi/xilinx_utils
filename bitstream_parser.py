import array
from packets import *

class bitstream_parser(object):
	def __init__(self, bit):
		try:
			file_bit = open(bit, 'rb')
		except IOError:
			raise 'FAILED: Open bit file: ' + bit
	
		while ord(file_bit.read(1)) != 0xff:
			pass	
			
		self.pktlist = []
		
		CONFIG_DATA_OFFSET = 27 + 6*4 # from dummy ffffffff to SYNC
		file_bit.seek(file_bit.tell() + CONFIG_DATA_OFFSET)
		
		bitstring = file_bit.read(4)
		
		while bitstring:
			p = packet(array.array('B', bitstring))
			if p.word_cnt > 0:
				p.data.fromstring(file_bit.read(p.word_cnt*4))
			self.pktlist.append(p)
			bitstring = file_bit.read(4)
			
		
