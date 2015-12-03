from Typedef import *
from Codec import Codec
import math

class KVZ(Codec):
	def __init__(self):
		self.type = 'encoder'
		self.name = 'kvazaar'
		self.license = 'GPL2'
		self.root_dir = HOME_PATH + '/codecs/encoders/kvazaar/src/'
		self.build_pattern = 'make -j4'
		self.clean_pattern = 'make clean'
		self.bitstream_pattern = os.getcwd()+'/bitstreams/%s_%s_%sfr_qp%s.bin' #enc name, yuv name, nfr, qp
		self.baseargs = ' --gop 8'
		self.optargs = ''
		self.parallelargs = ''
		self.parallel_tools = 0xE # '1110' # wpp, owf, tile, frame parallelism
		self.output_txt = self.name + '.txt'
		self.runid = 0

		if ASM:
			self.baseargs += ' --cpuid 1'
		else:
			self.baseargs += ' --cpuid 0'

		#w,h, nfr, fps, qp, optargs, inp,out, output text
		self.run_pattern = self.root_dir + 'kvazaar --input-res %dx%d -n %d --input-fps %d --qp %d %s -i %s -o %s > %s 2>&1'
		 
		# key => num_args, values
		self.param_table = {'ref':					[1,	 [1,4,8,15]], \
					   'no-deblock':				[0, ['no-deblock','']], \
					   'no-sao':					[0, ['no-sao','']], \
					   'no-rdoq':					[0, ['no-rdoq','']], \
					   'no-signhide':				[0, ['no-signhide','']], \
					   'rd':						[1, [0,1,2]], \
					   'full-intra-search':			[0, ['full-intra-search','']], \
					   'me':						[1, ['hexbs', 'tz']], \
					   'no-transform-skip':			[0, ['no-transform-skip','']], \
					   'subme':						[1, [0,1]], \
					   'pu-depth-inter':			[2, [0,1,2,3],[0,1,2,3]], \
					   'pu-depth-intra':			[2, [0,1,2,3,4],[0,1,2,3,4]], \
					   'bipred':					[0, ['bipred','']], \
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
		
	def setYuvDimAndFPS(self, w,h,fps):
		self.yuv_height = h
		self.yuv_width = w
		self.yuv_fps = fps
		
	def parallelize(self, wpp = 0, frame= 0, tile = 0, threads = 1, frame_threads = 1, rows = 1, cols = 1):
		
		self.parallelargs = ''
		
		if wpp:
			self.parallelargs += ' --wpp'
			if frame:
				self.parallelargs += ' --owf ' + str(frame_threads)
			else:
				self.parallelargs += ' --owf 0'
		else:
			self.parallelargs += ' --owf 0'

		if tile:
			nrows = int(math.ceil(self.yuv_height/rows/64))*64 # must be multiple of CTU size / using ceil seems to yield better fps (MUST CHECK)
			ncols = int(math.ceil(self.yuv_height/cols/64))*64
			self.parallelargs += ' --tiles-width-split ' + str(ncols)
			self.parallelargs += ' --tiles-height-split ' + str(nrows)

		if wpp or frame or tile:
			self.parallelargs += ' --threads ' + str(threads)
		else:
			self.parallelargs += ' --threads 0'
			

	def encode(self,Yuv,qp, cfg_string):
		if not os.path.isdir(os.getcwd()+'/bitstreams'):
			os.system('mkdir bitstreams')
		if not os.path.isdir(os.getcwd()+'/outputs'):
			os.system('mkdir outputs')
			if not os.path.isdir(os.getcwd()+'/outputs/'+Yuv.name):
				os.system('mkdir /outputs/'+Yuv.name)
		bitstream_path = self.bitstream_pattern % (self.name, Yuv.name, Yuv.num_frames, qp)
		args = (' '.join([self.baseargs,self.optargs,self.parallelargs])).strip('  ')
		code = zlibCompress(cfg_string)
		self.output_txt = '%s_%s_QP%d.txt'% (self.name, cfg_string, qp)
		
		if qp == 37:
			self.runid += 1
			
		#self.output_txt = re.sub('_+', '_', self.name + '_'+ '_'.join(args.replace('-','').split(' ')) + '.txt')
		#w,h, nfr, fps, qp, optargs, inp,out
		self.run_string = self.run_pattern % (Yuv.width, Yuv.height, Yuv.num_frames, Yuv.fps, qp, args,Yuv.path,bitstream_path,self.output_txt)
		#print run_string
		os.system(self.run_string)	
		f = open(self.output_txt,'a')
		f.write('\n'+self.run_string)
		f.close()
		
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
			
	def generateRandomCfg(self):
		cfg = []
		for p in self.param_table:
			n_args = self.param_table[p][0]
			if n_args < 2:
				val = str(random.choice(self.param_table[p][1]))
				if val != '':
					cfg.append([p])
			elif n_args == 2:
				val1 = str(random.choice(self.param_table[p][1]))
				val1_idx = self.param_table[p][1].index(int(val1))
				val2 = str(random.choice(self.param_table[p][2][val1_idx:]))
				cfg.append([p,[val1,val2]])
				
		return cfg

	def parseOutput(self):
		f = open(self.output_txt, 'r')
		lines = f.read()
		f.close()
#		 Processed 64 frames,    6963776 bits AVG PSNR: 38.7552 42.4212 43.3029
		try:
			(nfr, bits) = [int(x) for x in re.compile('Processed\s+(\d+)\s+frames,\s+(\d+)\s+bits').findall(lines)[0]]	
			(avg_psnry, avg_psnru,avg_psnrv) = [float(x) for x in re.compile('AVG\s+PSNR:\s+(\d+.\d+)\s+(\d+.\d+)\s+(\d+.\d+)').findall(lines)[0]]
			avg_br = float(bits)/(nfr/self.yuv_fps)/1000.0
			fps = float(re.compile('FPS:\s+(\d+.\d+)').findall(lines)[0])
		except:
			return [None, None, None]

		return [avg_psnry, avg_br, fps]
