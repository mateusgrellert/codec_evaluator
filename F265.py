from Typedef import *

class F265(Codec):
	type = 'encoder'
	license = 'BSD'
	root_dir = '/home/grellert/codecs/encoder/f265'
	build_pattern = root_dir + '/scons libav=none'
	if not ASM:
		build_pattern += ' asm=0'
	

	if TILE_PARALLELISM:
		run_pattern = root_dir + 'build/f265cli -v -w %d:%d -c %d -p "fps=%d,1 qp=%d, mt-mode=1" %s %s' #w,h,nfr,fps,qp,inp,out
	elif SLICE_PARALLELISM:
		run_pattern = root_dir + 'build/f265cli -v -w %d:%d -c %d -p "fps=%d,1 qp=%d, mt-mode=2" %s %s' #w,h,nfr,fps,qp,inp,out
	elif FRAME_PARALLELISM:
		run_pattern = root_dir + 'build/f265cli -v -w %d:%d -c %d -p "fps=%d,1 qp=%d, mt-mode=3" %s %s' #w,h,nfr,fps,qp,inp,out
	else:
		run_pattern = root_dir + 'build/f265cli -v -w %d:%d -c %d -p "fps=%d,1 qp=%d" %s %s' #w,h,nfr,fps,qp,inp,out
	 
	# key => num_args, values
	param_table = {'all-intra':	[1,	[0,1]], \
				   'amp':		[1, [0,1]], \
				   'bframes':	[1, range(0,17)], \
				   'cb-range':	[2, [3,4,5,6], [3,4,5,6]], \
				   'chroma-me':	[1, [0,1]], \
				   'deblock':	[1, [0,1]], \
				   'fpel':		[3, ['dia','xdia','hex'],range(0,17),['sad', 'satd']], \
				   'hm-me':		[1, [0,1]], \

	


