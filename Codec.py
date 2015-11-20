from Typedef import *

class Codec:

	
	@abstractmethod
	def __init__(self):
		raise NotImplementedError()
	@abstractmethod
	def build(self):
		raise NotImplementedError()
	@abstractmethod
	def run(self):
		raise NotImplementedError()
	@abstractmethod
	def addParam(self):
		raise NotImplementedError()
	

