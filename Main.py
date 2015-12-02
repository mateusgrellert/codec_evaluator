import Codec
import X265
import KVZ
import HOMER
import Yuv
from Bjontegaard import bdrate
from Typedef import *

import itertools


yuv = Yuv.Yuv()
yuv.initParams(HOME_PATH+'/hm-cfgs/cropped/BQMall.cfg')

x265 = X265.X265()
kvz = KVZ.KVZ()
homer = HOMER.Homer()


encoder_list = [homer]
#encoder_list = [kvz,homer]
#encoder_list = [homer,kvz,x265]


ref_bitrate_vet = [5397.4200, 2462.7825, 1200.5250, 612.2025]
ref_psnr_vet = [39.6266, 36.5677, 33.4729, 30.4879]

for encoder in encoder_list:
	print 'ENCODER: ', encoder.name
	results_dict = {}
	fps_vet = []
	psnr_vet = []
	bitrate_vet = []
	invalid_cfgs = {}

	for i in range(0,10):
		curr_cfg = encoder.generateRandomCfg()
		#print cfg
		for pv in curr_cfg:
			[p,v] = pv
			encoder.addParam(p,v)
		fps_vet = []
		psnr_vet = []
		bitrate_vet = []
		for qp in [22,27,32,37]:
			encoder.parallelize()
			encoder.encode(yuv,qp)
			[avg_psnry, avg_br, fps] = encoder.parseOutput()
			if avg_psnry != None:
				psnr_vet.append(avg_psnry)
				bitrate_vet.append(avg_br)
				fps_vet.append(fps)
			else:
				break
			
		if psnr_vet:
			curr_cfg_str = '_'.join([str(item) for sublist in curr_cfg for item in sublist])
			print curr_cfg_str
			print encoder.optargs
			for b,p,f in zip(bitrate_vet, psnr_vet,fps_vet):
				print '%.2f\t%.3f\t\t\t\t\t%.3f' % (b,p,f)
			results_dict[curr_cfg_str] = [bdrate(ref_bitrate_vet, bitrate_vet, ref_psnr_vet, psnr_vet)/100.0,sum(fps_vet)/len(fps_vet)]
		else:
			invalid_cfgs.append(curr_cfg_str)


"""
	for qp in [22,27,32,37]:
		encoder.addParam(param, val)
		encoder.parallelize()
		encoder.encode(yuv,qp)
		[avg_psnry, avg_br, fps] = encoder.parseOutput()
		if avg_psnry != None:
			psnr_vet.append(avg_psnry)
			bitrate_vet.append(avg_br)
			fps_vet.append(fps)
		else:
			break
		
	if psnr_vet:
		print 'ARGS\t',re.sub(';[\s|;]*', ';', ';'.join(encoder.optargs.replace('-','').split(' ')))
		for b,p,f in zip(bitrate_vet, psnr_vet,fps_vet):
			print '%.2f\t%.3f\t\t\t\t\t%.3f' % (b,p,f)
			results_dict[curr_cfg] = bdrate(ref_bitrate_vet, bitrate_vet, ref_psnr_vet, psnr_vet)/100.0
	else:
		invalida_cfgs.append(curr_cfg)
"""







"""
for encoder in encoder_list:
	print 'ENCODER: ', encoder.name
	results_dict = {}
	nvals = []
	for arg_vals in encoder.param_table.values():
		[arg, vals] = [arg_vals[0], arg_vals[1:]]
		if arg < 2:
			vals = vals[0]
		else:
			vals = list(itertools.product(*vals))
		nvals.append(vals)
	nvals = list(itertools.product(*nvals))
	print len(nvals)
	#for vals in nvals[300:400]:
	#	for p, v in zip(encoder.param_table, vals):
	#		encoder.addParam(p,v)
	#	print re.sub(';[\s|;]*', ';', ';'.join(encoder.optargs.replace('-','').split(' '))).lstrip(';')
"""
"""
	
		for val in nvals:
			fps_vet = []
			psnr_vet = []
			bitrate_vet = []
			for qp in [22,27,32,37]:
				encoder.addParam(param, val)
				encoder.parallelize()
				encoder.encode(yuv,qp)
				[avg_psnry, avg_br, fps] = encoder.parseOutput()
				if avg_psnry != None:
					psnr_vet.append(avg_psnry)
					bitrate_vet.append(avg_br)
					fps_vet.append(fps)
				else:
					break
			
			if psnr_vet:
				print 'ARGS\t',re.sub(';[\s|;]*', ';', ';'.join(encoder.optargs.replace('-','').split(' ')))
				for b,p,f in zip(bitrate_vet, psnr_vet,fps_vet):
					print '%.2f\t%.3f\t\t\t\t\t%.3f' % (b,p,f)
					results_dict[curr_cfg] = bdrate(ref_bitrate_vet, bitrate_vet, ref_psnr_vet, psnr_vet)/100.0

"""

"""
for encoder in encoder_list:
	print 'ENCODER: ', encoder.name
	results_dict = {}
	for param, args_vals in encoder.param_table.items():
		vals = args_vals[1:]
		if len(vals) == 1:
			nvals = vals[0]
		else:
			for x in vals[0]:
				for y in vals[1]:
					nvals.append([x,y])
		for val in nvals:
			fps_vet = []
			psnr_vet = []
			bitrate_vet = []
			for qp in [22,27,32,37]:
				encoder.addParam(param, val)
				encoder.parallelize()
				encoder.encode(yuv,qp)
				[avg_psnry, avg_br, fps] = encoder.parseOutput()
				if avg_psnry != None:
					psnr_vet.append(avg_psnry)
					bitrate_vet.append(avg_br)
					fps_vet.append(fps)
				else:
					break
			
			if psnr_vet:
				print 'ARGS\t',re.sub(';[\s|;]*', ';', ';'.join(encoder.optargs.replace('-','').split(' ')))
				for b,p,f in zip(bitrate_vet, psnr_vet,fps_vet):
					print '%.2f\t%.3f\t\t\t\t\t%.3f' % (b,p,f)
					results_dict[curr_cfg] = bdrate(ref_bitrate_vet, bitrate_vet, ref_psnr_vet, psnr_vet)/100.0
"""					
					
					
					
"""
n_threads = 10
for encoder in encoder_list:
	print 'ENCODER: ', encoder.name
	for wpp_en in [0,1]:
		if wpp_en and (encoder.parallel_tools & 0x8 == 0): continue

		for tile_en in [0,1]:
			if  tile_en and (encoder.parallel_tools & 0x2 == 0): continue
			
			for frame_par_en in [0,1]:
				if frame_par_en and ((encoder.parallel_tools & 0x1 == 0) and (encoder.parallel_tools & 0x4 == 0)): continue
				
				fps_vet = []
				psnr_vet = []
				bitrate_vet = []
				for qp in [22,27,32,37]:
					break_flag = 0
					if encoder.name == 'kvazaar':
						encoder.setYuvDimAndFPS(yuv.width, yuv.height, yuv.fps)
		
					frame_par =  (encoder.parallel_tools & 0x1) and frame_par_en
					tile = (encoder.parallel_tools & 0x2) and tile_en
					owf = (encoder.parallel_tools & 0x4) and frame_par_en
					wpp = (encoder.parallel_tools & 0x8) and wpp_en
								
					frame_threads = 1
					tile_rows = 2
					tile_cols = 2
					
					if wpp and (frame_par or owf):
						frame_threads = int(n_threads/4) + 1
					elif owf and wpp == 0:
						continue
					elif frame_par:
						ctuRows = int(yuv.height / 64)
						frame_threads = min(n_threads, ctuRows / 2)

					encoder.parallelize(wpp, (frame_par or owf), tile, n_threads, frame_threads, tile_rows, tile_cols)
					encoder.encode(yuv,qp)			

					[avg_psnry, avg_br, fps] = encoder.parseOutput()
					if avg_psnry != None:
						psnr_vet.append(avg_psnry)
						bitrate_vet.append(avg_br)
						fps_vet.append(fps)
					else:
						break
				
				if psnr_vet:
					print 'ASM/WPP/TILE/FRAME PARALLELISM\t%d\t%d\t%d\t%d' % (ASM, int(wpp), int(tile), int(owf or frame_par))
					for b,p,f in zip(bitrate_vet, psnr_vet,fps_vet):
						print '%.2f\t%.3f\t\t\t\t\t%.3f' % (b,p,f)

					#print '%.4f\t' % (bdrate(ref_bitrate_vet, bitrate_vet, ref_psnr_vet, psnr_vet)/100.0),
					
					
"""
"""
print '\t'.join(x265.param_table['preset'][1][1:3])
for preset in x265.param_table['preset'][1][1:3]:
	fps_vet = []
	psnr_vet = []
	bitrate_vet = []
	for qp in [22,27,32,37]:
		x265.addParam('preset', preset)
		x265.parallelize(wpp=1, frame=1, threads = 10, frame_threads = 0)
		x265.encode(yuv, qp)
		[avg_psnry, avg_br, fps] = x265.parseOutput()
		psnr_vet.append(avg_psnry)
		bitrate_vet.append(avg_br)
		fps_vet.append(fps)

	for b,p,f in zip(bitrate_vet, psnr_vet,fps_vet):
		print b,'\t',p,'\t\t\t\t\t',f

	print '%.4f\t' % (bdrate(ref_bitrate_vet, bitrate_vet, ref_psnr_vet, psnr_vet)/100.0),

print '\n',
"""

"""
for encoder in encoder_list:
	encoder.build()
	
for encoder in encoder_list:
	
	encoder.parallelize(wpp=1,threads=6)
	encoder.encode(yuv, 30)
"""
