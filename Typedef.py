import os
from abc import ABCMeta, abstractmethod
from sys import stderr
import platform
import re
import sys
import random
import collections
import zlib, base64

BASE_YUV_PATH = os.environ['HOME'] + '/origCfP/cropped/'
HOME_PATH = os.environ['HOME']
PARALLEL = 1
if len(sys.argv) > 1:
	ASM = int(sys.argv[1])
else:
	ASM = 0
	

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield str(sub)
        else:
            yield str(el)


def zlibCompress(text):
	coded = base64.b64encode(zlib.compress(text,9))
	coded = coded.replace('/','SLASH')
	return coded

def zlibDecompress(coded):
	text = text.replace('SLASH','/')
	return zlib.decompress(base64.b64decode(coded))

