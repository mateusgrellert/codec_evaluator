from Typedef import *

class Codec:

	
	@abstractmethod
	def __init__(self):
		raise NotImplementedError()
	@abstractmethod
	def build(self):
		raise NotImplementedError()
	@abstractmethod
	def encode(self, Yuv, qp):
		raise NotImplementedError()
	@abstractmethod
	def decode(self, bitstream):
		raise NotImplementedError()
	@abstractmethod
	def addParam(self, p, vals):
		raise NotImplementedError()
	@abstractmethod
	def delParam(self, p):
		raise NotImplementedError()
	

