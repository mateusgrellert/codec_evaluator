import Codec
import X265
import KVZ
import HOMER
import Yuv

yuv = Yuv.Yuv()
yuv.initParams('/home/grellert/hm-cfgs/BQMall.cfg')

x265 = X265.X265()
kvz = KVZ.KVZ()
homer = HOMER.Homer()

encoder_list = [x265, kvz, homer]

for preset in x265.param_table['preset'][1]:
	x265.addParam('preset', preset)
	x265.encode(yuv, 40)

"""
for encoder in encoder_list:
	encoder.build()
	
for encoder in encoder_list:
	
	encoder.parallelize(wpp=1,threads=6)
	encoder.encode(yuv, 30)
"""
