import numpy as np

def lu_lfactor(A,start):
    l = []
    if A.shape[1] <= start:
        l.append(A)
        return l
    else:
        L_i = np.eye(A.shape[0],A.shape[1])
        for i in range(start, A.shape[0]):
            L_i[i, start-1] = -(A[i, start-1] / A[start-1,start-1])
        l.append(L_i)
        return l + lu_lfactor(L_i.dot(A), start+1)


def lu_ufactor(A):
    u = []
    for i in range(A.shape[1]):
        U_i  = np.eye(A.shape[0],A.shape[1])
        U_i[:,i] = A[:,i]
        u.append(U_i)
    return u

def lu_factor(A):
    low = lu_lfactor(A, 1)
    up = lu_ufactor(low[-1])
    # try:
    low = [np.linalg.inv(i) for i in low[:-1]]
    return low + up[::-1]


