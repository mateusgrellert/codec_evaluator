import Codec
import F265
import Yuv

yuv = Yuv.Yuv()
f265 = F265.F265()
yuv.initParams('/home/grellert/hm-cfgs/BQSquare.cfg')

f265.build()
f265.run(yuv,30)

