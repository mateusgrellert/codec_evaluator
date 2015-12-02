from Typedef import *
from Codec import Codec
import re

class X265(Codec):
	def __init__(self):
		self.type = 'encoder'
		self.name = 'x265'
		self.license = 'GPL2'
		
		self.root_dir = HOME_PATH +'/codecs/encoders/x265/build/'
		self.build_pattern = 'make -j4'
		self.clean_pattern = 'make clean'
		self.bitstream_pattern = os.getcwd()+'/bitstreams/%s_%s_%sfr_qp%s.bin' #enc name, yuv name, nfr, qp
		self.baseargs = ' --psnr --psy-rd 0 --scenecut 0 --keyint -1'
		self.parallelargs = ''
		self.optargs = ''
		self.parallel_tools = '1001' # wpp, owf, tile, frame parallelism
		self.output_txt = self.name + '.txt'
		if not ASM:
			self.baseargs += ' --no-asm'

		#w,h, nfr, fps, qp, optargs, inp,out, output text
		self.run_pattern = self.root_dir + 'x265 --input-res %dx%d -f %d --fps %d --qp %d %s --input %s  -o %s > %s 2>&1'
		 
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
	
	def parallelize(self, wpp = 0, frame= 0, tile = 0, threads = 1, frame_threads = 1, rows = 1, cols = 1):
		self.parallelargs = ''
		if wpp:
			self.parallelargs += ' --wpp'
		else:
			self.parallelargs += ' --no-wpp'
			
		if frame:
			self.parallelargs += ' --frame-threads ' + str(frame_threads)
		else:
			self.parallelargs += ' --frame-threads 1'
			
		

	def encode(self,Yuv,qp):
		if not os.path.isdir(os.getcwd()+'/bitstreams'):
			os.system('mkdir bitstreams')
		bitstream_path = self.bitstream_pattern % (self.name, Yuv.name, Yuv.num_frames, qp)
		args = ' '.join([self.baseargs,self.optargs,self.parallelargs])

		#w,h, nfr, fps, qp, optargs, inp,out
		#self.output_txt = re.sub('_+', '_', self.name + '_'+ '_'.join(args.replace('-','').split(' ')) + '.txt')
		run_string = self.run_pattern % (Yuv.width, Yuv.height, Yuv.num_frames, Yuv.fps, qp, args,Yuv.path,bitstream_path, self.output_txt)
		#print run_string
		os.system(run_string)
		#self.parseOutput()
	
	def decode(self, bitstream):
		print >> stderr, 'Error: No decoder available for ', self.name
	
	def addParam(self, p, vals):
		if p in self.optargs:
			self.delParam(p)
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

	def parseOutput(self):
		f = open(self.output_txt, 'r')
		lines = f.read()
		f.close()
		try:
			(ni,np,nb) = [int(x) for x in re.compile('frame\s+\w:\s+(\d+)').findall(lines)]
			found = re.compile('PSNR\sMean:\sY:(\d+.\d+)\sU:(\d+.\d+)\sV:(\d+.\d+)').findall(lines)
		
			(ipsnry, ipsnru, ipsnrv) = [float(x) for x in found[0]]
			(ppsnry, ppsnru, ppsnrv) = [float(x) for x in found[1]]
			(bpsnry, bpsnru, bpsnrv) = [float(x) for x in found[2]]
		
			avg_psnry = (ipsnry*ni + ppsnry*np + bpsnry*nb) / sum([ni,np,nb])
			avg_psnru = (ipsnru*ni + ppsnru*np + bpsnru*nb) / sum([ni,np,nb])
			avg_psnrv = (ipsnrv*ni + ppsnrv*np + bpsnrv*nb) / sum([ni,np,nb])


			(ibr,pbr,bbr) = [float(x) for x in re.compile('kb/s:\s+(\d+.\d+)\s+PSNR\sMean').findall(lines)]
			avg_br = (ibr*ni + pbr*np + bbr*nb)/sum([ni,np,nb])
			fps = float(re.compile('\((\d+.\d+) fps\)').findall(lines)[0])
		except:
			return [None, None, None]

		return [avg_psnry, avg_br, fps]
