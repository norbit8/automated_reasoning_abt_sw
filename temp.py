from Formula import Formula, is_base_formula, is_unary, is_variable

def createDic(f,d,counter):
    phi_G = Formula("x" + str(counter))
    counter+=1
    d[f.id] = phi_G
    if (is_base_formula(f)):
        return counter
    if (is_unary(f.root)):
       return createDic(f.first, d, counter)
    else:
        counter = createDic(f.first, d, counter)
        counter = createDic(f.second, d, counter)
        return counter

def createLis(f,d, lis):
    if (is_base_formula(f)):
        f_temp = Formula("<->", d[f.id], f)
        lis.append(f_temp)
        return
    if (is_unary(f.root)):
        temp = Formula(f.root, d[f.first.id])
        f_temp = Formula("<->", d[f.id] ,temp)
        lis.append(f_temp)
        createLis(f.first,d, lis)
    else:
        print(f)
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
    return lis

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
# #Tseitini
# phi = Formula.parse("((p&q)|~(q|r))")
# Tseitinis_list = get_Tseitinis_list(phi)

#removal
# f = Formula.parse("(w1|(r|(q|(r|(w1|~w2)))))")
# print(f)
# f_clean = remove_literal_occurs_twice(f)
# print(is_clause_tautlogy(f))
# print(f)

cnf = [["~r","~w","q11"],["r","p","~w"],["p","q","w"],["w23","w34"]]
d = dict()
d["p"]= False
d["q"] = False

print(BCP(cnf,d))
print(d)
