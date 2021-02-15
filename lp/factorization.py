import numpy as np
import scipy.linalg

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
    # except:
    #     for i in low:
    #         print(i)

    return low + up[::-1]


# A = np.array([ [7, 3, -1, 2], [3, 8, 1, -4], [-1, 1, 4, -1], [2, -4, -1, 6] ])
# lis = lu_factor(A)
# for a in lis:
#     print(a)
#
# res = lis[0]
#
# for a in lis[1:]:
#     res = res.dot(a)
# print(np.round(res))

