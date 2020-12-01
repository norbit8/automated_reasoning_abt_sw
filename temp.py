from Formula import Formula, is_base_formula, is_unary, is_variable
from tempo import *
from semantics import *

def createDic(f,d,counter):
    phi_G = Formula("x" + str(counter))
    counter+=1
    d[f.id] = phi_G
    if (is_base_formula(f)) or is_variable(f.root):
        return counter
    elif (is_unary(f.root)):
       return createDic(f.first, d, counter)
    else:
        counter = createDic(f.first, d, counter)
        counter = createDic(f.second, d, counter)
        return counter

def createLis(f,d, lis):
    if (is_base_formula(f) or is_variable(f.root)):
        f_temp = Formula("<->", d[f.id], f)
        lis.append(f_temp)
        return
    if (is_unary(f.root)):
        temp = Formula(f.root, d[f.first.id])
        f_temp = Formula("<->", d[f.id] ,temp)
        lis.append(f_temp)
        createLis(f.first,d, lis)
    else:
        temp = Formula(f.root, d[f.first.id], d[f.second.id])
        f_temp = Formula("<->", d[f.id] ,temp)
        lis.append(f_temp)
        createLis(f.first, d, lis)
        createLis(f.second, d, lis)


def get_Tseitinis_list(phi):
    d = dict()
    lis = []
    counter = 0
    createDic(phi, d, counter)
    lis.append(d[phi.id])
    createLis(phi, d, lis)
    return lis,d

def get_literal_from_cnf(f):
    literals = []

    while (f.root == '|'):

        if (f.first.root == "~"):
            literals.append(f.first.root + f.first.first.root)
        else:
            literals.append(f.first.root)
        f = f.second

    if f.root == "~":
        literals.append(f.root + f.first.root)
    else:
        literals.append(f.root)

    return literals

def create_cnf_from_literals(l):
    if len(l)==1:
        return Formula.parse(l[0])
    else:
        second = create_cnf_from_literals(l[1:])
        first = Formula.parse(l[0])
        return Formula("|",first,second)



def remove_literal_occurs_twice(f):
    literals = list(set(get_literal_from_cnf(f)))
    return create_cnf_from_literals(literals)

def is_clause_tautlogy(f):
    literals = list(set(get_literal_from_cnf(f)))
    for literal in literals:
        if literal[0] == "~":
            if literal[1:] in literals:
                return True
        else:
            if "~" + literal in literals:
                return True
    return False


def is_clause_BCP(clause,d):
    """
    checks whether only one var isnt assign
    :param clause:
    :param d:
    :return:
    """
    counter = 0
    for literal in clause:
        if literal[0] == "~":
            var = literal[1:]
            assign = False
        else:
            var = literal
            assign = True
        if var in d.keys():
            if not (d[var] ^ assign):
                return
        else:
            potenital_last_variable = var
            potenital_assign = assign
            counter+=1
        if counter > 1:
            return
    return (potenital_last_variable, potenital_assign)

def BCP(cnf,d):
    bcp_flag = True
    while bcp_flag:
        clause_flag = False
        for clause in cnf:
            t = is_clause_BCP(clause,d)
            if (t != None):
                clause_flag = True
                if t[0] in d.keys() and d[t[0]] != t[1]:
                    return False
                d[t[0]]= t[1]
        if not clause_flag:
            bcp_flag = False

    return True

def list_to_true_cnf(l):
    if len(l)==1:
        return l[0]
    else:
        second = list_to_true_cnf(l[1:])
        first = l[0]
        return Formula("&",first,second)

def tseitinis_model(f,model, special_dic):
    if (is_base_formula(f)) or is_variable(f.root):
        model[special_dic[f.id].root] = evaluate(f, model)
    elif (is_unary(f.root)):
        tseitinis_model(f.first, model, special_dic)
        model[special_dic[f.id].root] = evaluate(f, model)
    else:
        tseitinis_model(f.first, model, special_dic)
        tseitinis_model(f.second, model, special_dic)
        model[special_dic[f.id].root] = evaluate(f, model)
    return model

def compare_formulas(input_formula, ts_formula, special_dict):
    """
    This method gets two formulas, one in regular form and the other one is the first one ts form
    and return True if the second formula is really the ts form of the first one.
    :param input_formula: Formula
    :param ts_formula: Formula that should be the ts form of the first input formula
    :return: True if ts_formula is the ts form of the input_formula
    """
    f_input_vars = Formula.variables(input_formula)
    models_original_formula = all_models(list(f_input_vars))
    for model in models_original_formula:
        result_original_formula = evaluate(input_formula, model)
        ts_model = tseitinis_model(input_formula, model, special_dict)
        result_ts_formula = evaluate(ts_formula, ts_model)
        if result_original_formula != result_ts_formula:
            return False
    return True

##Tseitini
phi = Formula.parse("((~((p|q)|~(q->r))&~q)<->~r13)")
Tseitinis_list, special_dict = get_Tseitinis_list(phi)
print(Tseitinis_list)
f1 = convert_to_cnf(Tseitinis_list)
print(f1)
f1 = list_to_true_cnf(f1)

# model = {"p":True, "q":True, "r":True}
# Tseitinis_list, special_dict = get_Tseitinis_list(phi)
# tseitinis_model(phi,model, special_dict)
# print(model)


# true_cnf = list_to_true_cnf(convert_to_cnf(Tseitinis_list))
# print(true_cnf)
print(compare_formulas(phi, f1, special_dict))

#removal
# f = Formula.parse("(w1|(r|(q|(r|(w1|~w2)))))")
# print(f)
# f_clean = remove_literal_occurs_twice(f)
# print(is_clause_tautlogy(f))
# print(f)

# cnf = [["~r","~w","q11"],["r","p","~w"],["p","q","w"],["w23","w34"]]
# d = dict()
# d["p"]= False
# d["q"] = False
#
# print(BCP(cnf,d))
# print(d)
