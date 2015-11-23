from Typedef import *
from Codec import Codec

class X265(Codec):
	def __init__(self):
		self.type = 'encoder'
		self.name = 'x265'
		self.license = 'BSD'
		self.root_dir = '/home/grellert/codecs/encoders/f265/'
		self.build_pattern = 'scons libav=none'
		self.clean_pattern = 'scons -c'
		self.bitstream_pattern = os.getcwd()+'/bitstreams/%s_%s_%s_%s.bin' #enc name, yuv name, nfr, qp
		self.optargs = ''
	
