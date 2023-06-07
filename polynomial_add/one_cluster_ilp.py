import gurobipy as gp
from gurobipy import LinExpr


# takes a file as an argument and finds the minimum descriptor of the file using linear method
def ILP_one_cluster(filename):
    # the beginning code simply disables gurobi's console output
    with gp.Env(empty=True) as env:
        env.setParam('OutputFlag', 0)
        env.start()
        with gp.Model(env=env) as m:
            # open the data set file
            with open(filename) as f:
                input = f.read()

            # remove new lines from the data set
            input.replace("\n", "")
            # split input file on spaces
            input_array = input.split()
            n = int(input_array[0])  # number of data items
            K = int(input_array[1])  # number of clusters
            N = int(input_array[2])  # number of tags
            alpha = int(input_array[3])  # maximum size of descriptor for each item

            # create an empty array to store B values
            B = []
            # create an empty array to store cluster values corresponding to data items
            clusters = []
            for i in range(n):
                # create a new line in the B matrix
                B.append([])
                # add the cluster value corresponding to the data item to the array
                clusters.append(int(input_array[i * (N + 2) + 6]))
                # append tags to the new line in the B array
                for j in range(N):
                    B[i].append(int(input_array[i * (N + 2) + 7 + j]))

            # create y[j,k] variables
            y = {}
            for j in range(1, N + 1):
                for k in range(1, K + 1):
                    y[j, k] = m.addVar(vtype=gp.GRB.BINARY, name="k=%s y[%s,%s]" % (k, j, k))

            # Objective function is to minimize the sum of the variables in A
            coef = [1 for j in range(1, N + 1) for k in range(1, K + 1)]
            var = [y[j, k] for j in range(1, N + 1) for k in range(1, K + 1)]
            objective = m.setObjective(LinExpr(coef, var), gp.GRB.MINIMIZE)

            # CONSTRAINTSs
            # (a) must contain at least one tag from each of the data items in that cluster
            A = [0 for c in range(n + 1)]
            constraint1 = []
            for i in range(1, n + 1):
                for j in range(1, N + 1):
                    # find the k value
                    k = clusters[i - 1]
                    if B[i - 1][j - 1] == 1:
                        # add the constraint that a descriptor must describe each data item within the cluster
                        A[i] += y[j, k]
                constraint1.append(m.addConstr(A[i], ">=", 1))

            m.update()

            m.optimize()

            # get the values of variables
            x_values = m.getAttr("X")
            y_values = m.getVars()

            # make an array of the names of used variables
            vars_used = []
            for i in range(len(x_values)):
                # if the value of the variable is 1.0, include it in the array if the variable is a z variable, exclude it
                if x_values[i] == 1.0 and y_values[i].getAttr("VarName")[0] != 'z':
                    vars_used.append(y_values[i].getAttr("VarName"))

            # sort the array alphabetically
            vars_used.sort()

            # create an array of descriptors
            D = [[] for i in range(K + 1)]

            for var in vars_used:
                # split the string on the space between the k value at the beginning and the y
                k = var.split()
                # assign j to be the tag value
                j = int(k[1].split("[")[1].split(",")[0])
                # assign i to be the k value of the string
                i = int(k[0].split("=")[1])
                # add the tag number to the corresponding descriptor
                D[i].append(j)

            # create an empty output string
            output_string = ""
            # print the values of the solution that equal one
            # print("Solution:\n---------------------------")
            for var in vars_used:
                # use a temp variable to only output the variable's name rather than the k value
                temp = var.split()
                # append the variable to the output string
                output_string += f"{temp[1]} = 1\n"

            # print(output_string)

            # output the descriptors and descriptor format
            # print("Descriptors:\n---------------------------")
            # print(f"Descriptor format:"
            #       f"\nD_k : [tags in a comma separated list]")
            for k in range(1, K + 1):
                # sort the descriptor in order of increasing tag number
                D[k].sort()
                # print the descriptor in the format specified in the print statement above
                descriptor = f"D_{k} : size {len(D[k])} : {D[k]}"
                output_string += f"{descriptor} \n"
                # print(descriptor)

            return output_string
