from Typedef import *
from Codec import Codec

class Homer(Codec):
	def __init__(self):
		self.type = 'encoder'
		self.name = 'homerHEVC'
		self.license = 'LGPL2.1'
		self.root_dir = HOME_PATH + '/codecs/encoders/HomerHEVC/build/Linux/'
		self.build_pattern = 'make -j4'
		self.clean_pattern = 'make clean'
		self.bitstream_pattern = os.getcwd()+'/bitstreams/%s_%s_%sfr_qp%s.bin' #enc name, yuv name, nfr, qp
		self.baseargs = ' -intra_period 0 -bitrate_mode 0 -scene_change 0'
		self.optargs = ''
		self.parallelargs = ''
		self.yuv_fps = 60
		self.parallel_tools = 0x9 # '1001'  wpp, owf, tile, frame parallelism
		self.output_txt = self.name + '.txt'
		self.runid = 0
		if ASM:
			self.baseargs += ' -sse 1'
		else:
			self.baseargs += ' -sse 0'

		#w,h, nfr, fps, qp, optargs, inp,out, text output
		self.run_pattern = self.root_dir + 'homer_app/Release/homer_app -widthxheight %dx%d -n_frames %d -frame_rate %d -qp %d %s -i %s -o %s > %s 2>&1'
		 
		# key => num_args, values
		self.param_table = {'cu_size':					[1,	[16,32,64]], \
					   'motion_estimation_precision':	[1, [0,1,2]], \
					   'max_pred_depth':				[1, [1,2,3,4]], \
					   'max_intra_tr_depth':			[1, [0,1,2,3,4]], \
					   'max_inter_tr_depth':			[1, [0,1,2,3,4]], \
					   'sign_hiding':					[1, [0,1]], \
					   'sao':							[1, [0,1]], \
					   'performance_mode':				[1, [0,1,2]], \
					   'rd_mode':						[1, [0,1]], \
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
		
	def parallelize(self, wpp = 0, frame= 0, tile = 0, threads = 1, frame_threads = 1, rows = 1, cols = 1):
		self.parallelargs = ''
		if wpp:
			self.parallelargs += ' -n_wpp_threads ' + str(threads - frame_threads) 
		else:
			self.parallelargs += ' -n_wpp_threads 0'
			
		if frame:
			self.parallelargs += ' -n_enc_engines ' + str(frame_threads)
		else:
			self.parallelargs += ' -n_enc_engines 1'


			

	def encode(self,Yuv,qp):
		if not os.path.isdir(os.getcwd()+'/bitstreams'):
			os.system('mkdir bitstreams')
		bitstream_path = self.bitstream_pattern % (self.name, Yuv.name, Yuv.num_frames, qp)

		self.output_txt = self.name + '_run'+str(self.runid)+'_QP'+str(qp)+'.txt'
		if qp == 37:
			self.runid += 1
		args = ' '.join([self.baseargs,self.optargs,self.parallelargs]).strip('  ')
		self.yuv_fps = Yuv.fps
		#w,h, nfr, fps, qp, optargs, inp,out
		#self.output_txt = re.sub('_+', '_', self.name + '_'+ '_'.join(args.replace('-','').split(' ')) + '.txt')
		run_string = self.run_pattern % (Yuv.width, Yuv.height, Yuv.num_frames, Yuv.fps, qp, args,Yuv.path,bitstream_path, self.output_txt)
		print run_string
		os.system(run_string)
		f = open(self.output_txt,'a')
		f.write('\n'+run_string)
		f.close()
	
	def decode(self, bitstream):
		print >> stderr, 'Error: No decoder available for ', self.name
	
	def addParam(self, p, vals):
		if p in self.optargs:
			self.delParam(p)

		self.optargs += ' -%s %s' % (p, vals)
	
	def delParam(self,p):
		toks = self.optargs.split('-')
		for tok in toks:
			if p in tok:
				del toks[toks.index(tok)]
			
		self.optargs = '-'.join(toks)
		
	def generateRandomCfg(self):	
		cfg = []
		for p in self.param_table:
			cfg.append([p,str(random.choice(self.param_table[p][1]))])
		return cfg

	
	def parseOutput(self):
		f = open(self.output_txt, 'r')
		lines = f.read()
		f.close()
# engine:1, frame:31, P, bits:171040,PSNRY: 38.89, PSNRU: 41.83,PSNRV: 42.82, Average PSNRY: 13.39, PSNRU: 14.48,PSNRV: 14.89, vbv: 0.35, qp: 22, pts: 31, 
		try:
			bits = sum([int(x) for x in re.compile('bits:(\d+),').findall(lines)])
			psnry = [float(x) for x in re.compile('PSNRY:\s+(\d+.\d+),').findall(lines)]
			avg_psnry = sum(psnry)/len(psnry)
	#		64 frames in 3046 milliseconds: 21.011162 fps
			nfr = int(re.compile('\s+(\d+)\s+frames\s+in').findall(lines)[0])
			avg_br = float(bits)/(nfr/self.yuv_fps)/1000.0
			fps = float(re.compile('(\d+.\d+)\s+fps').findall(lines)[0])
		except:
			return [None, None, None]

		return [avg_psnry, avg_br, fps]
	
