import numpy as np
import numpy.linalg as la
cimport numpy as np

DTYPE = np.double
ctypedef np.double_t DTYPE_t

ITYPE = np.int
ctypedef np.int_t ITYPE_t

cdef double min3(double a, double b, double c):
    cdef double m = a
    if b < m:
        m = b
    if c < m:
        m = c
    return m

# Compute DTW from a precomputed pointwise distance matrix
def dtw_fast_precomputed(np.ndarray[DTYPE_t,ndim=2] d):
    cdef int nrows = d.shape[0]
    cdef int ncols = d.shape[1]

    cdef np.ndarray[DTYPE_t,ndim=2] dtw = np.zeros((nrows+1,ncols+1), dtype = DTYPE)

    dtw[:,0] = 1e6
    dtw[0,:] = 1e6
    dtw[0,0] = 0.0

    cdef unsigned int i,j
    cdef DTYPE_t cost

    for i in range(nrows):
        for j in range(ncols):
            cost = d[i][j]
            dtw[i+1,j+1] = cost + min3(dtw[i,j+1],dtw[i+1,j],dtw[i,j])

    return dtw, dtw[nrows,ncols]

# Cython version of the trackeback function
def _trackeback_fast(D):
    cdef int i
    cdef int j
    i, j = np.array(D.shape) - 1
    cdef int tb
    p, q = [i], [j]
    while (i > 0 and j > 0):
        tb = np.argmin((D[i-1, j-1], D[i-1, j], D[i, j-1]))

        if (tb == 0):
            i = i - 1
            j = j - 1
        elif (tb == 1):
            i = i - 1
        elif (tb == 2):
            j = j - 1

        p.append(i)
        q.append(j)

    return (np.array(list(reversed(p))), np.array(list(reversed(q))))
