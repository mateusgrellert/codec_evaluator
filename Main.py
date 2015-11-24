import Codec
import X265
import KVZ
import Yuv

yuv = Yuv.Yuv()
kvz = KVZ.KVZ()
yuv.initParams('/home/grellert/hm-cfgs/BQSquare.cfg')

kvz.build()
kvz.decode('str.bin')
kvz.encode(yuv,30)

