from numpy import array, zeros, argmin, inf
from numpy.linalg import norm

from .fast import dtw_fast_precomputed, _trackeback_fast

def dtw(x, y, dist=lambda x, y: norm(x - y, ord=1)):
    """ Computes the DTW of two sequences.

    :param array x: N1*M array
    :param array y: N2*M array
    :param func dist: distance used as cost measure (default L1 norm)

    Returns the minimum distance, the accumulated cost matrix and the wrap path.

    """
    x = array(x)
    if len(x.shape) == 1:
        x = x.reshape(-1, 1)
    y = array(y)
    if len(y.shape) == 1:
        y = y.reshape(-1, 1)

    r, c = len(x), len(y)

    D = zeros((r + 1, c + 1))
    D[0, 1:] = inf
    D[1:, 0] = inf

    for i in range(r):
        for j in range(c):
            D[i+1, j+1] = dist(x[i], y[j])

    dtw_dist, dtw_matrix = dtw_precomputed(D)

    return dist, dtw_distmat, _trackeback(dtw_matrix)


def dtw_py_precomputed(d):
    r, c = d.shape

    dtw_dist = zeros((r + 1, c + 1))
    dtw_dist[0, 1:] = inf
    dtw_dist[1:, 0] = inf

    for i in range(r):
        for j in range(c):
            cost = d[i][j]
            dtw_dist[i+1, j+1] = cost + min(dtw_dist[i, j],
                    dtw_dist[i, j+1], dtw_dist[i+1, j])

    return dtw_dist[r, c], dtw_dist


def _trackeback(D):
    i, j = array(D.shape) - 1
    p, q = [i], [j]
    while (i > 0 and j > 0):
        tb = argmin((D[i-1, j-1], D[i-1, j], D[i, j-1]))

        if (tb == 0):
            i = i - 1
            j = j - 1
        elif (tb == 1):
            i = i - 1
        elif (tb == 2):
            j = j - 1

        p.insert(0, i)
        q.insert(0, j)

    p.insert(0, 0)
    q.insert(0, 0)
    return (array(p), array(q))

try:
    _trackeback = _trackeback_fast
    dtw_precomputed = dtw_fast_precomputed
except:
    dtw_precomputed = dtw_py_precomputed
