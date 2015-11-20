from Typedef import *
import re

class Yuv:
	def __init__(self):
		self.width = 832
		self.height = 480
		self.num_frames = 64
		self.fps = 60
		self.name = 'BQMall'
		self.path = '/home/grellert/origCfP/BQMall_832x480_60.yuv'
		
	def initParams(self, cfg_path):
		f = open(cfg_path,'r').read()
		self.path = BASE_YUV_PATH + re.compile('(\w+\.yuv)').findall(f)[0]
		self.fps = int(re.compile('FrameRate\s+\:\s+(\d+)').findall(f)[0])
		self.width = int(re.compile('SourceWidth\s+\:\s+(\d+)').findall(f)[0])
		self.height = int(re.compile('SourceHeight\s+\:\s+(\d+)').findall(f)[0])