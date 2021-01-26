




#todo change impl
def model_over_skeleton_to_model_over_formula(partial_assignment, sub_map):
    assignment = {sub_map[skeleton_var]: skeleton_var_assignment for skeleton_var, skeleton_var_assignment in partial_assignment.items()}
    return assignment
