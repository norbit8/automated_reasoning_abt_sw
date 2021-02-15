# ------- IMPORTS -------
from functools import reduce
import numpy as np
from lp_solver.factorization import lu_factor as lu_factorization

# ------- CONSTANTS -------
ETA_THRESHOLD = 30
NO_SOLUTION = 0
SUCCESS = 1
UNBOUNDED = 2
BLAND_RULE = 0
DANTZIG_RULE = 1
EPSILON = 0.0001


def ftran(eta_list, a):
    """
    Implementation of the ftran method.
    :param eta_list: Eta matrices list.
    :param a: Vector.
    :return: The resulting vector.
    """
    if len(eta_list) == 1:
        return np.linalg.inv(eta_list[0]).dot(a)
    z = ftran(eta_list[:-1], a)
    return np.linalg.inv(eta_list[-1]).dot(z)


def btran_helper(eta_list, a):
    """
    Helper function for the Btran method.
    :param eta_list: Eta vectors list.
    :param a: Vector a.
    :return: The resulting vector.
    """
    if len(eta_list) == 1:
        return a.dot(np.linalg.inv(eta_list[0]))
    z = btran_helper(eta_list[1:], a)
    return z.dot(np.linalg.inv(eta_list[0]))


def btran(c_N, c_B, B, A_N, B_temp):
    """
    Btran implementation
    :param c_N: Vector.
    :param c_B: Vector.
    :param B: Matrix.
    :param A_N: Matrix.
    :param B_temp: Vector.
    :return: BTran implementation.
    """
    # y = c_B @ np.linalg.inv(B)  # get y
    y = btran_helper(B_temp, c_B)
    entering_var_vector = c_N - (y @ A_N)
    return entering_var_vector


def blands_rule(entering_var_vector, x_N):
    """
    Bland's rule implementation.
    :param entering_var_vector: The entering vector.
    :param x_N: Vector.
    :return: The resulted index.
    """
    mask = (entering_var_vector > 0).astype(np.int64)
    mask *= x_N
    for index, item in enumerate(mask):
        if item > 0:
            return index


def lp_solver(A_N: np.array, b: np.array, c_N: np.array, strategy=DANTZIG_RULE):
    """
    The main lp solver function, returns the result
    :param A_N: Matrix
    :param b: Vector
    :param c_N: Vector
    :param strategy: Bland rule or Dantzig rule
    :return: The result of the lp solver
    """
    # Init mats
    b_star = b.copy()
    number_of_normal_vars = A_N.shape[1]
    number_of_slack_vars = A_N.shape[0]
    x_N = np.arange(1, number_of_normal_vars + 1)
    x_B = np.arange(number_of_normal_vars + 1, number_of_normal_vars + 1 + number_of_slack_vars)
    B = np.eye(number_of_slack_vars, number_of_slack_vars)
    c_B = np.zeros(x_B.shape)
    B_eta_mats = [B.copy()]
    # >> Step 0: checking feasibility <<
    if np.count_nonzero(c > EPSILON) == 0:
        return NO_SOLUTION, None
    while True:  # START REVISED-SIMPLEX ALGORITHM
        if not np.allclose(B.dot(b_star), b):  # Numerical safeguard
            print(B.dot(b_star), b.astype(np.float64))
            print("NUMERICAL STABILIZATION PROCESS...")
            B_eta_mats = lu_factorization(reduce(np.dot, B_eta_mats))
        # >> Step 1: BTRAN <<
        entering_var_vector = btran(c_N, c_B, B, A_N, B_eta_mats)
        # >> Step 2: getting the entering variable <<
        entering_var = 0
        if np.count_nonzero(entering_var_vector > EPSILON) == 0:  # FOUND OPTIMAL
            return SUCCESS, c_B @ b_star
        if strategy == BLAND_RULE:
            entering_var = blands_rule(entering_var_vector, x_N)
        elif strategy == DANTZIG_RULE:
            entering_var = np.argmax(entering_var_vector)
        # >> Step 3: FTRAN <<
        d1 = ftran(B_eta_mats, A_N[:, entering_var].copy())
        # >> Step 4: Find the largest t s.t. b - td >= 0 thus getting the leaving variable <<
        choose_t = b_star / d1
        choose_t = np.where(choose_t > 0, choose_t, np.inf)  # choose_t[choose_t < 0] = np.inf
        leaving_var, t = np.argmin(choose_t), np.min(choose_t)
        b_i_1 = np.eye(B.shape[0])
        b_i_1[:, leaving_var] = d1
        B_eta_mats.append(b_i_1)
        if np.count_nonzero(d1 <= 0) == d1.shape[0]:  # d cant be negative
            return UNBOUNDED, None
        # >> Step 5: Swap the entering/leaving columns in B and A_N and in x_B and x_N <<
        c_N[entering_var], c_B[leaving_var] = c_B[leaving_var], c_N[entering_var]
        B[:, leaving_var], A_N[:, entering_var] = np.copy(A_N[:, entering_var]), np.copy(B[:, leaving_var])
        x_B[leaving_var], x_N[entering_var] = x_N[entering_var], x_B[leaving_var]
        # >> Step 6: Set the value of the entering variable to t and update b <<
        b_star = b_star - d1 * t
        b_star[leaving_var] = t


if __name__ == "__main__":
    """
    TESTING CLASS EXAMPLE
    """
    # CLASS EXAMPLE
    A = np.array([[3, 2, 1, 2], [1, 1, 1, 1], [4, 3, 3, 4]])
    b = np.array([225, 117, 420])
    c = np.array([19, 13, 12, 17])
    # -------------
    res, val = lp_solver(A, b, c, BLAND_RULE)
    if res == UNBOUNDED:
        print("UNBOUNDED")
    elif res == SUCCESS:
        print(f"SUCCESS\nMaximal value is: {val}")
    else:
        print("NO SOLUTION")
