# -*- coding: utf-8 -*-
'''
Created on 2019-01-25
@summary:  arrayfilter
@author: fiefdx
'''

from numpy cimport ndarray as ar
import numpy as np
cimport cython
from libc.float cimport float
from libc.stdint cimport uint8_t, uint32_t

cimport arrayfilterlink


@cython.boundscheck(False)
@cython.wraparound(False)
def vertices_filter(ar[float, ndim = 2, mode = "c"] data):
    cdef uint32_t h = len(data)
    cdef ar[float, ndim = 2, mode = "c"] vertices = np.empty((h, 3), dtype = np.float32)
    cdef ar[uchar, ndim = 2, mode = "c"] colors = np.empty((h, 4), dtype = np.uint8)
    length = arrayfilterlink.vertices_filter(<float*> data.data, <float*> vertices.data, <uint8_t*> colors.data, <uint32_t> h)
    return vertices[:length], colors[:length]
