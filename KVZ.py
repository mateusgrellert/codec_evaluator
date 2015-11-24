from Typedef import *
from Codec import Codec
import math

class KVZ(Codec):
	def __init__(self):
		self.type = 'encoder'
		self.name = 'kvazaar'
		self.license = 'GPL2'
		self.root_dir = '/home/grellert/codecs/encoders/kvazaar/src/'
		self.build_pattern = 'make -j4'
		self.clean_pattern = 'make clean'
		self.bitstream_pattern = os.getcwd()+'/bitstreams/%s_%s_%sfr_qp%s.bin' #enc name, yuv name, nfr, qp
		self.optargs = ' --gop 8'
	
		if not ASM:
			self.optargs += ' --cpuid 0'

		#w,h, nfr, fps, qp, optargs, inp,out
		self.run_pattern = self.root_dir + 'kvazaar --input-res %dx%d -n %d --input-fps %d --qp %d %s -i %s -o %s'
		 
		# key => num_args, values
		self.param_table = {'ref':					[1,	 [1,4,8,15], \
					   'no-deblock':				[0, ['no-deblock']], \
					   'no-sao':					[0, ['no-sao']], \
					   'no-rdoq':					[0, ['no-rdoq']], \
					   'no-signhide':				[0, ['no-signhide']], \
					   'rd':						[1, [0,1,2]], \
					   'full-intra-search':			[0, ['full-intra-search']], \
					   'me':						[1, ['hexbs', 'tz']], \
					   'no-transform-skip':			[0, ['no-transform-skip']], \
					   'subme':						[1, [0,1]], \
					   'pu-depth-inter':			[2, [0,1,2,3],[0,1,2,3]], \
					   'pu-depth-intra':			[2, [0,1,2,3,4],[0,1,2,3,4]], \
					   'bipred':					[0, ['bipred']], \
					}
				
				

	def build(self):
		self.clean()
		cwd = os.getcwd()
		os.chdir(self.root_dir)
		print self.build_pattern
		os.system(self.build_pattern)
		os.chdir(cwd)
	
	def clean(self):
		cwd = os.getcwd()
		os.chdir(self.root_dir)
		os.system(self.clean_pattern)
		os.chdir(cwd)
		
	def encode(self,Yuv,qp):
		if not os.path.isdir(os.getcwd()+'/bitstreams'):
			os.system('mkdir bitstreams')
		bitstream_path = self.bitstream_pattern % (self.name, Yuv.name, Yuv.num_frames, qp)
		
		if WPP_PARALLELISM:
			self.optargs += ' --wpp'
			if FRAME_PARALLELISM:
				self.optargs += ' --owf ' + str(N_FRAME_THREADS)
		if TILE_PARALLELISM:
			nrows = int(math.ceil(Yuv.height/TILE_ROWS/64))*64 # must be multiple of CTU size / using ceil seems to yield better fps (MUST CHECK)
			ncols = int(math.ceil(Yuv.width/TILE_COLS/64))*64
			self.optargs += ' --tiles-width-split ' + ncols
			self.optargs += ' --tiles-height-split ' + nrows

		if WPP_PARALLELISM or FRAME_PARALLELISM or TILE_PARALLELISM:
			self.optargs += ' --threads ' + str(N_THREADS)
		
		#w,h, nfr, fps, qp, optargs, inp,out
		run_string = self.run_pattern % (Yuv.width, Yuv.height, Yuv.num_frames, Yuv.fps, qp, self.optargs,Yuv.path,bitstream_path)
		print run_string
		os.system(run_string)
	
	def decode(self, bitstream):
		print >> stderr, 'Error: No decoder available for ', self.name
	
	def addParam(self, p, vals):
		if p in self.optargs:
			self.delParam(p)
		
		n_args = self.param_table[p][0]
		if n_args == 0:
			self.optargs += ' --%s' % (vals)
		elif n_args == 2:
			self.optargs += ' --%s %s-%s' % (p, vals[0], vals[1])
		else:
			self.optargs += ' --%s %s' % (p, vals)
	
	def delParam(self,p):
		toks = self.optargs.split('--')
		for tok in toks:
			if p in tok:
				del toks[toks.index(tok)]
			
		self.optargs = '--'.join(toks)
			
