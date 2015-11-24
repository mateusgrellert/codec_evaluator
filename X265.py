from Typedef import *
from Codec import Codec

class X265(Codec):
	def __init__(self):
		self.type = 'encoder'
		self.name = 'x265'
		self.license = 'GPL2'
		self.root_dir = '/home/grellert/codecs/encoders/x265/build/'
		self.build_pattern = 'make -j4'
		self.clean_pattern = 'make clean'
		self.bitstream_pattern = os.getcwd()+'/bitstreams/%s_%s_%sfr_qp%s.bin' #enc name, yuv name, nfr, qp
		self.optargs = ' -psnr --scenecut 0'
	
		if not ASM:
			self.optargs += ' --no-asm'

		#w,h, nfr, fps, qp, optargs, inp,out
		self.run_pattern = self.root_dir + 'x265 --input-res %dx%d -f %d --fps %d --qp %d %s --input %s  -o %s'
		 
		# key => num_args, values
		self.param_table = {'preset':				[1,	 ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow', 'placebo']], \
					   'tune':						[1, ['psnr', 'ssim', 'zerolatency', 'fastdecode']], \
					   'ctu':						[1, [64,32,16]], \
					   'tu-intra-depth':			[1, [1,2,3,4]], \
					   'tu-inter-depth':			[1, [1,2,3,4]], \
					   'rect':						[0, ['rect', 'no-rect']], \
					   'amp':						[0, ['amp', 'no-amp']], \
					   'rd':						[1, range(0,7)], \
					   'psy-rd ':					[1, [0, 0.5, 1.0, 1.5, 2.0]], \
					   'nr ':						[1, [0, 100, 250, 500, 750, 1000]], \
					   'tskip-fast':				[0, ['tskip-fast', 'no-tskip-fast']], \
					   'early-skip':				[0, ['early-skip','no-early-skip']], \
					   'fast-cbf':					[0, ['fast-cbf','no-fast-cbf']],	\
					   'weightp':					[0, ['weightp','no-weightp']], \
					   'weightb':					[0, ['weightb','no-weightb']],	\
					   'signhide':					[0, ['signhide','no-signhide']], \
					   'tskip':						[0, ['tskip','no-tskip']], \
					   'me':						[1, [0,1,2,3,4]], \
					   'subme':						[1, range(0,8)], \
					   'merange':					[1, [0,16,32,64]], \
					   'max-merge':					[1, [1,2,3,4,5]], \
					   'strong-intra-smoothing':	[0, ['strong-intra-smoothing','no-strong-intra-smoothing']], \
					   'constrained-intra':			[0, ['constrained-intra','no-constrained-intra']], \
					   'b-intra':					[0, ['b-intra','no-b-intra']], \
					   'fast-intra':				[0, ['fast-intra','no-fast-intra']], \
					   'b-pyramid':					[0, ['b-pyramid','no-b-pyramid']], \
					   'cutree':					[0, ['cutree','no-cutree']], \
					   'lft':						[0, ['lft','no-lft']], \
					   'sao':						[0, ['sao','no-sao']], \
					   'rdpenalty':					[1, [0,1,2]], \
					   'bframes':					[1, [1,2,4,8]], \
					   'bframe-bias':				[1, [0,25,50,100]], \
					   'b-adapt':					[1, [0,1,2]], \
					   'ref':						[1, [1,2,4,8,16]], \
					   'aq-mode':					[1, [0,1,2]], \
					   'sao-lcu-bounds':			[1, [0,1]], \
					   'sao-lcu-opt':				[1, [0,1]], \
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
		bitstream_path = self.bitstream_pattern % (self.name, Yuv.name, Yuv.num_frames, qp)
		
		if WPP_PARALLELISM:
			self.optargs += ' --wpp'
		if FRAME_PARALLELISM:
			self.optargs += ' --frame-threads ' + str(N_FRAME_THREADS)
			
		if WPP_PARALLELISM or FRAME_PARALLELISM:
			self.optargs += ' --threads ' + str(N_THREADS)
		
		#w,h, nfr, fps, qp, optargs, inp,out
		run_string = self.run_pattern % (Yuv.width, Yuv.height, Yuv.num_frames, Yuv.fps, qp, self.optargs,Yuv.path,bitstream_path)
		print run_string
		os.system(run_string)
	
	def decode(self, bitstream):
		print >> stderr, 'Error: No decoder available for ', self.name
	
	def addParam(self, p, vals):
		n_args = self.param_table[p][0]
		if n_args == 0:
			self.optargs += ' --%s' % (vals)
		else:
			self.optargs += ' --%s %s' % (p, vals)
	
	def delParam(self,p):
		toks = self.optargs.split('--')
		for tok in toks:
			if p in tok:
				del toks[toks.index(tok)]
			
		self.optargs = '--'.join(toks)
	
