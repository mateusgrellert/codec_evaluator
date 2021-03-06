from Typedef import *
from Codec import Codec

class F265(Codec):
	def __init__(self):
		self.type = 'encoder'
		self.name = 'f265'
		self.license = 'BSD'
		self.rec_yuv_pattern = 'f265_%s'
		self.root_dir = '/home/grellert/codecs/encoders/f265/'
		self.build_pattern = 'scons libav=none'
		self.clean_pattern = 'scons -c'
		self.bitstream_pattern = os.getcwd()+'/bitstreams/%s_%s_%sfr_qp%s.bin' #enc name, yuv name, nfr, qp
		self.optargs = ''
	
		if not ASM:
			self.build_pattern += ' asm=0'
	

		if TILE_PARALLELISM:
			self.run_pattern = self.root_dir + 'build/f265cli -v -w %d:%d -c %d -p "fps=%d,1 qp=%d yuv-dump=%s mt-mode=1 %s" %s %s' #w,h,nfr,fps,qp, rec yuv, optargs,inp,out
		elif SLICE_PARALLELISM:
			self.run_pattern = self.root_dir + 'build/f265cli -v -w %d:%d -c %d -p "fps=%d,1 qp=%d yuv-dump=%s mt-mode=2 %s" %s %s' #w,h,nfr,fps,qp, rec yuv, optargs,inp,out
		elif FRAME_PARALLELISM:
			self.run_pattern = self.root_dir + 'build/f265cli -v -w %d:%d -c %d -p "fps=%d,1 qp=%d yuv-dump=%s mt-mode=3 %s" %s %s' #w,h,nfr,fps,qp, rec yuv, optargs,inp,out
		else:
			self.run_pattern = self.root_dir + 'build/f265cli -v -w %d:%d -c %d -p "fps=%d,1 qp=%d yuv-dump=%s mt-mode=0 %s" %s %s' #w,h,nfr,fps,qp, rec yuv, optargs,inp,out
		 
		# key => num_args, values
		self.param_table = {'all-intra':	[1,	[0,1]], \
					   'amp':				[1, [0,1]], \
					   'bframes':			[1, range(0,17)], \
					   'cb-range':			[2, [3,4,5,6], [3,4,5,6]], \
					   'chroma-me':			[1, [0,1]], \
					   'deblock':			[1, [0,1]], \
					   'fpel':				[3, ['dia','xdia','hex'], range(0,17), ['sad', 'satd']], \
					   'hm-me':				[1, [0,1]], \
					   'nb-merge':			[1, range(1,6)], \
					   'nullify-inter-tb':	[1, [0,1]], \
					   'quality':			[1, [0,10,20,25,50,60]], \
					   'rdo':				[1, [0,1]], \
					   'rdoq':				[1, [0,1]],	\
					   'ref':				[1, range(0,17)], \
					   'sign-hiding':		[1, [0,1]],	\
					   'smooth-intra':		[1, [0,1]], \
					   'tb-depth':			[2, range(0,5), range(0,5)], \
					   'tb-range':			[2, [2,3,4,5], [2,3,4,5]], \
					   'tmv':				[1, [0,1]], \
					}
	def build(self):
		#self.clean()
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
		rec_yuv_path = self.rec_yuv_pattern % (Yuv.name) + '.yuv'	
		bitstream_path = self.bitstream_pattern % (self.name, Yuv.name, Yuv.num_frames, qp)
		run_string = self.run_pattern % (Yuv.width, Yuv.height, Yuv.num_frames, Yuv.fps, qp, rec_yuv_path, self.optargs,Yuv.path,bitstream_path)
		print run_string
		os.system(run_string)
	
	def decode(self, bitstream):
		print >> stderr, 'Error: No decoder available for ', self.name
	
	def addParam(self, p, vals):
		n_args = self.param_table[p][0]
		if n_args > 1:
			val = ','.join([str(x) for x in vals])
		else:
			val = str(vals)
		self.optargs += ' %s=%s' % (p, vals)
	
