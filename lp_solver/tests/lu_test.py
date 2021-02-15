from lp_solver.factorization import lu_factor
import numpy as np
from scipy.optimize import linprog

def is_matrice_inverable(A):
    return np.linalg.det(A) != 0

def test_lu_factor(n):
    for i in range(n):
        size = np.random.randint(3,20)
        A = np.random.randint(100, size=(size, size))
        while not is_matrice_inverable(A):
            A = np.random.randint(100, size=(size, size))
        factors = lu_factor(A)
        res = factors[0]
        for a in factors[1:]:
            res = res.dot(a)
        if not np.allclose(A,res):
            print("fail!")
            return
    print("pass")



def test_unbound_linear_problem():
    pass

def test_not_fissible_sol():
    pass

def test_feasisible_soultion():
    As = [np.array([[2,3,1],[4,1,2],[3,4,2]])]
    Cs = [np.array([5,4,3])]
    Bs = [np.array([5,11,8])]
    for A,b,c in zip(As, Bs, Cs):
        res = linprog(c=-c, A_ub=A, b_ub=b)
        if not np.allclose(-1 * res['fun'], 13):
            print("fail!")
            return
    print("pass")


test_lu_factor(100)
