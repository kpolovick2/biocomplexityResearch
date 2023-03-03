# William Bradford
# wcb8ze
# ____ NOT WORKING YET ____
# comparison of output between files

import ILP_gurobi_generalized_concise as ILP

def compare(file_a, file_b, p):

    x = ILP.ILP_concise(file_a)
    y = ILP.ILP_concise(file_b)

    tag = p
    y_refactor = []
    for i in range(len(y)):
        if i == tag:
            y_refactor.append(0.0)
        y_refactor.append(y[i])

    for i in range(len(x)-1):
        # print(f"x: {x[i]}")
        # print(f"y: {y_refactor[i]}")
        if x[i] != y_refactor[i]:
            print(f"at index {i}, x = {x[i]} y = {y_refactor[i]}")

compare("50n_11K_314N.txt", "50n_11K_314N_22p.txt", 17)