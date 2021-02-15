# ------- IMPORTS -------
from functools import reduce

import numpy as np
from lp_solver.factorization import lu_factor as lu_factorization
# ------- CONSTANTS -------
NO_SOLUTION = 0
SUCCESS = 1
UNBOUNDED = 2
BLAND_RULE = 0
DANTZIG_RULE = 1
EPSILON = 0.0001

def ftran(eta_list, a):
    if len(eta_list) == 1:
        return np.linalg.inv(eta_list[0]).dot(a)
    z = ftran(eta_list[1:], a)
    return np.linalg.inv(eta_list[0]).dot(z)

def btran1(eta_list, a):
    if len(eta_list) == 1:
        return a.dot(np.linalg.inv(eta_list[0]))
    z = ftran(eta_list[1:], a)
    return z.dot(np.linalg.inv(eta_list[0]))


def btran(c_N, c_B, B, A_N, B_temp):
    y = c_B @ np.linalg.inv(B)  # get y
    # y1 = btran1(B_temp, c_B)
    # print("check: ", y ,y1)
    entering_var_vector = c_N - (y @ A_N)
    print(f"entering_var_vector: {entering_var_vector}")
    return entering_var_vector


def step_3():
    pass


def step_4():
    pass


def step_5():
    pass


def blands_rule(entering_var_vector, x_N):
    # mask = (entering_var_vector > 0).astype(np.int64)
    # mask *= x_N
    # min_value, min_index = np.max(mask), np.argmax(mask)
    # for index, item in enumerate(mask):
    #     if item != 0:
    #         if item < min_value:
    #             min_index = index
    #             min_value = item
    mask = (entering_var_vector > 0).astype(np.int64)
    mask *= x_N
    for index, item in enumerate(mask):
        if item > 0:
            return index
    # return min_index


def lp_solver(A_N: np.array, b: np.array, c_N: np.array, strategy=DANTZIG_RULE):
    # Init mats
    number_of_normal_vars = A_N.shape[1]
    number_of_slack_vars = A_N.shape[0]
    x_N = np.arange(1, number_of_normal_vars + 1)
    x_B = np.arange(number_of_normal_vars + 1, number_of_normal_vars + 1 + number_of_slack_vars)
    B = np.eye(number_of_slack_vars, number_of_slack_vars)
    c_B = np.zeros(x_B.shape)
    # print("x_n: ", x_N, "\n x_B: ", x_B, "\nB: ", B, c_N, c_B)
    B_temp = [B.copy(),]

    # >> Step 0: checking feasibility <<
    if np.count_nonzero(c > EPSILON) == 0:
        return NO_SOLUTION, None
    iter = 1

    while True:  # START REVISED-SIMPLEX ALGORITHM
        # print(f"----------Iteration number: {iter}--------------")
        # print("x_n: ", x_N,
        #       "\nx_B: ", x_B,
        #       "\nB: ", B,
        #       "\nc_N: ", c_N,
        #       "\nc_B: ", c_B,
        #       "\nA_N:", A_N)
        # B_temp = lu_factorization(reduce(np.dot, B_temp))
        print("B_Temp" , B_temp)
        # print ("let see " , reduce(np.dot, B_temp), B)
        # >> Step 1: BTRAN <<
        # TODO: use eta matrices
        entering_var_vector = btran(c_N, c_B, B, A_N, B_temp)
        # >> Step 2: getting the entering variable <<
        entering_var = 0
        if np.count_nonzero(entering_var_vector > EPSILON) == 0:  # FOUND OPTIMAL
            return SUCCESS, c_B @ b
        if strategy == BLAND_RULE:
            entering_var = blands_rule(entering_var_vector, x_N)
        elif strategy == DANTZIG_RULE:
            entering_var = np.argmax(entering_var_vector)

        # >> Step 3: FTRAN <<
        # TODO: use eta matrices
        d1 = ftran(B_temp, A_N[:, entering_var].copy())
        print("an" , A_N[:, entering_var].copy())
        d = np.linalg.inv(B) @ A_N[:, entering_var]
        print("check: d and d1", d, d1 )

        # >> Step 4: Find the largest t s.t. b - td >= 0 thus getting the leaving variable <<
        choose_t = b / d
        # choose_t[choose_t < 0] = np.inf
        choose_t = np.where(choose_t > 0, choose_t, np.inf)
        leaving_var, t = np.argmin(choose_t), np.min(choose_t)
        b_i_1 = np.eye(B.shape[0])
        b_i_1[:, leaving_var] = d.copy()
        B_temp.append(b_i_1)
        print("leaving_var: ", leaving_var)
        print("entering_var:", entering_var)
        print("d:", d)
        print("b:", b)
        print("division b/d=", b / d)
        if np.count_nonzero(d <= 0) == d.shape[0]:  # d cant be negative
            return UNBOUNDED, None
        # >> Step 5: Swap the entering/leaving columns in B and A_N and in x_B and x_N <<
        c_N[entering_var], c_B[leaving_var] = c_B[leaving_var], c_N[entering_var]
        B[:, leaving_var], A_N[:, entering_var] = np.copy(A_N[:, entering_var]), np.copy(B[:, leaving_var])
        x_B[leaving_var], x_N[entering_var] = x_N[entering_var], x_B[leaving_var]
        # >> Step 6: Set the value of the entering variable to t and update b <<
        b = b - d * t
        b[leaving_var] = t
        iter += 1

        print("SO FAR:", c_B @ b)
        print("-------------------------------------------------")

#
# if __name__ == "__main__":
#     # CLASS EXAMPLE
#     A = np.array([[3, 2, 1, 2], [1, 1, 1, 1], [4, 3, 3, 4]])
#     b = np.array([225, 117, 420])
#     c = np.array([19, 13, 12, 17])
#     # -------------
#     res, val = lp_solver(A, b, c, BLAND_RULE)
#     if res == UNBOUNDED:
#         print("UNBOUNDED")
#     elif res == SUCCESS:
#         print(f"SUCCESS\nMaximal value is: {val}")
#     else:
#         print("NO SOLUTION")





B = [np.eye(3), np.array([[3., 0., 0.],[1., 1., 0.],[4., 0., 1.]])]
a = np.array([2,1,3])
d = np.linalg.inv(reduce(np.dot, B)) @ a
print(d)
d1 = ftran(B, a)
print(d1)
