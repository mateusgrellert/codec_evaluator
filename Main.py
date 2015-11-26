import Codec
import X265
import KVZ
import HOMER
import Yuv
from Bjontegaard import bdrate

yuv = Yuv.Yuv()
yuv.initParams('/Users/grellert/hm-cfgs/cropped/BQMall.cfg')

x265 = X265.X265()
kvz = KVZ.KVZ()
homer = HOMER.Homer()

encoder_list = [x265, kvz, homer]
ref_bitrate_vet = [5397.4200, 2462.7825, 1200.5250, 612.2025]
ref_psnr_vet = [39.6266, 36.5677, 33.4729, 30.4879]

print '\t'.join(x265.param_table['preset'][1])
for preset in x265.param_table['preset'][1]:
	fps_vet = []
	psnr_vet = []
	bitrate_vet = []
	for qp in [22,27,32,37]:
		x265.addParam('preset', preset)
		x265.parallelize()
		x265.encode(yuv, qp)
		[avg_psnry, avg_br, fps] = x265.parseOutput()
		psnr_vet.append(avg_psnry)
		bitrate_vet.append(avg_br)
		fps_vet.append(fps)

	for b,p,f in zip(bitrate_vet, psnr_vet,fps_vet):
		print b,'\t',p,'\t\t\t\t\t',f

	#print '%.4f\t' % (bdrate(ref_bitrate_vet, bitrate_vet, ref_psnr_vet, psnr_vet)/100.0),

print '\n',


"""
for encoder in encoder_list:
	encoder.build()
	
for encoder in encoder_list:
	
	encoder.parallelize(wpp=1,threads=6)
	encoder.encode(yuv, 30)
"""
