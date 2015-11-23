from Typedef import *

class Codec:

	
	@abstractmethod
	def __init__(self):
		raise NotImplementedError()
	@abstractmethod
	def build(self):
		raise NotImplementedError()
	@abstractmethod
	def encode(self):
		raise NotImplementedError()
	@abstractmethod
	def decode(self):
		raise NotImplementedError()
	@abstractmethod
	def addParam(self):
		raise NotImplementedError()
	

