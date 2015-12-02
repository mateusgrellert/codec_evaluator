import os
from abc import ABCMeta, abstractmethod
from sys import stderr
import platform
import re
import sys
import random

BASE_YUV_PATH = os.environ['HOME'] + '/origCfP/cropped/'
HOME_PATH = os.environ['HOME']
PARALLEL = 1
if len(sys.argv) > 1:
	ASM = int(sys.argv[1])
else:
	ASM = 0
