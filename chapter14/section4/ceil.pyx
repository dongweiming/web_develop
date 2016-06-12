cdef extern from "math.h":
    double ceil(double x)


cdef double f(double x):
    return ceil(x)


cpdef double f2(double x):
    return f(x)
