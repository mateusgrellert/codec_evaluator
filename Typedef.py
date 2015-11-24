import os
from abc import ABCMeta, abstractmethod
from sys import stderr

ASM = 1
TILE_PARALLELISM = 0
TILE_ROWS = 1
TILE_COLS = 1
WPP_PARALLELISM = 0
SLICE_PARALLELISM = 0
FRAME_PARALLELISM = 0
N_THREADS = 1
N_FRAME_THREADS = 1
BASE_YUV_PATH = '/home/grellert/origCfP/'
