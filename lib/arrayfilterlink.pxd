from libc.stdint cimport uint8_t, uint32_t
from libc.float cimport float

cdef extern from "arrayfilter.h":
    uint32_t vertices_filter(float* data, float* vertices, uint8_t* colors, uint32_t length)
