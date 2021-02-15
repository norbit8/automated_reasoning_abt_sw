import numpy as np
from scipy.optimize import linprog
from lp_solver.lp_engine import lp_solver

def get_test_one():
    A = np.array([[3, 2, 1, 2], [1, 1, 1, 1], [4, 3, 3, 4]])
    b = np.array([225, 117, 420])
    c = np.array([19, 13, 12, 17])
    return A,b,c

def get_test_two():
    A = np.array([[2,3,1],[4,1,2],[3,4,2]])
    b = np.array([5,11,8])
    c = np.array([5,4,3])
    return A,b,c

def get_test_three():
    A = np.array([[5,7],[4,2],[2,1]])
    b = np.array([8,15,3])
    c = np.array([0.6, 0.35])
    return A,b,c



def test_feasisible_soultion():
    A1,b1,c1 = get_test_two()
    A2, b2, c2 = get_test_one()
    A3, b3, c3 = get_test_three()
    As = [A1, A2, A3]
    Bs = [b1, b2, b3]
    Cs = [c1, c2, c3]
    for A,b,c in zip(As, Bs, Cs):
        res = linprog(c=-c, A_ub=A, b_ub=b)
        res = -1 * res['fun']
        res1 = lp_solver(A, b ,c)[1]
        if not np.allclose(res, res1):
            print("fail!")
            return
    print("pass")


test_feasisible_soultion()