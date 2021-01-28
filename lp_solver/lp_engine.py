# ------- IMPORTS -------
import numpy as np

# ------- CONSTANTS -------
NO_SOLUTION = 0
SUCCESS = 1
UNBOUNDED = 2
BLAND_RULE = 0
DANTZIG_RULE = 1
EPSILON = 0.0001


def parse_result(c_B, c_N, x_B, x_N):
    """
    Given the arguments below, returns the maximized target function result, and the variables values
    which maximizes it.
    :param c_B: Basis vector values.
    :param c_N: Non basic variables values.
    :param x_B: Mapping vector from basis vector B to the variable index.
    :param x_N: Mapping vector from the non-basic vector to the variable index.
    :return: Target function value, the vars value which maximizes it.
    """
    # vars_indices = np.arange(x_N.shape)
    # for index in vars_indices:
    #
    #
    #
    # return result,
    pass


def get_entering_column():
    pass

def step_3():
    pass

def step_4():
    pass

def step_5():
    pass

def lp_solver(A_N: np.array, b: np.array, c_N: np.array, strategy=DANTZIG_RULE):
    # Init mats
    number_of_normal_vars = A_N.shape[1]
    number_of_slack_vars = A_N.shape[0]
    x_N = np.arange(1, number_of_normal_vars + 1)
    x_B = np.arange(number_of_normal_vars + 1, number_of_normal_vars + 1 + number_of_slack_vars)
    B = np.eye(number_of_slack_vars, number_of_slack_vars)
    c_B = np.zeros(x_B.shape)
    # print("x_n: ", x_N, "\n x_B: ", x_B, "\nB: ", B, c_N, c_B)
    # TODO: LU-factorization on B
    # B = lu_factorization(B)
    # >> Step 0: checking feasibility <<
    if np.count_nonzero(c > EPSILON) == 0:
        print("NO SOLUTION")
        return NO_SOLUTION
    while True:  # START REVISED-SIMPLEX ALGORITHM
        # >> Step 1: BTRAN <<
        # TODO: use eta matrices
        y = c_B @ np.linalg.inv(B)  # get y
        entering_var_vector = c_N - (y @ A_N)
        # >> Step 2: getting the entering variable <<
        entering_var = 0
        if np.count_nonzero(entering_var_vector > EPSILON) == 0:  # FOUND OPTIMAL
            return SUCCESS, parse_result(c_B, c_N, x_B, x_N)
        if strategy == BLAND_RULE:
            arg_sorted = np.argsort(x_N)
            sorted_entering = np.take_along_axis(entering_var_vector, arg_sorted, axis=0)
            val = sorted_entering[sorted_entering > EPSILON][0]
            for index, number in enumerate(entering_var_vector):
                if val == number:
                    entering_var = index
                    break
        elif strategy == DANTZIG_RULE:
            entering_var = np.argmax(entering_var_vector)
        entering_var = 2  # TODO: delete me, it's a debug because Dr.Guy chose this entering var in his example
        # >> Step 3: FTRAN <<
        # TODO: use eta matrices
        d = np.linalg.inv(B) @ A_N[:, entering_var]
        # >> Step 4: Find the largest t s.t. b - td >= 0 thus getting the leaving variable <<
        leaving_var, t = np.argmin(b / d), np.min(b / d)
        if t < 0:
            return UNBOUNDED
        # >> Step 5: Swap the entering/leaving columns in B and A_N and in x_B and x_N <<
        c_N[entering_var], c_B[leaving_var] = c_B[leaving_var], c_N[entering_var]
        print(B[:, leaving_var])
        print("---------")
        B[:, leaving_var], A_N[:, entering_var] = A_N[:, entering_var], B[:, leaving_var]
        print(B, "\n", A_N)
        exit(1)
    return SUCCESS


if __name__ == "__main__":
    A = np.array([[3, 2, 1, 2], [1, 1, 1, 1], [4, 3, 3, 4]])
    b = np.array([225, 117, 420])
    c = np.array([19, 13, 12, 17])
    # bla = np.zeros(4,)
    # print(np.count_nonzero(bla > 0) == 0)

    print("result: ", lp_solver(A, b, c, BLAND_RULE))
