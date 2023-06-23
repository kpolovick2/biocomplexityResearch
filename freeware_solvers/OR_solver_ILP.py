from ortools.linear_solver import pywraplp


def parse_input_file(filepath):
    # open the data set file
    with open(filepath) as f:
        input = f.read()

    # remove new lines from the data set
    input.replace("\n", "")
    # split input file on spaces
    input_array = input.split()
    n = int(input_array[0])  # number of data items
    K = int(input_array[1])  # number of clusters
    N = int(input_array[2])  # number of tags
    alpha = int(input_array[3])  # maximum size of descriptor for each item
    beta = int(input_array[4])  # maximum overlap

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

    return n, K, N, alpha, beta, B, clusters


def or_solver(filepath):
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return
    n, K, N, alpha, beta, B, clusters = parse_input_file(filepath)
    y = {}
    for j in range(1, N + 1):
        for k in range(1, K + 1):
            y[j, k] = solver.NumVar(0, 1, f'k={k} {j}')

    var = [y[j, k] for j in range(1, N+1) for k in range(1,K+1)]

    # CONSTRAINTSs
    # (a) must contain at least one tag from each of the data items in that cluster
    A = [0 for c in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, N + 1):
            # find the k value
            k = clusters[i - 1]
            if B[i - 1][j - 1] == 1:
                # add the constraint that a descriptor must describe each data item within the cluster
                A[i] += y[j, k]
        solver.Add(A[i] >= 1)

    for k in range(1, K + 1):
        var1 = [y[j, k] for j in range(1, N + 1)]
        solver.Add(sum(var1) <= alpha)

    z = {}
    z_sum = 0
    for k in range(1, K):
        for l in range(k + 1, K + 1):
            for j in range(1, N + 1):
                if B[k - 1][j - 1] * B[l - 1][j - 1] == 1:
                    z[j, k, l] = solver.NumVar(0, 1, f"z[%s,%s,%s]" % (j, k, l))
                    solver.Add(z[j, k, l] <= y[j, k])
                    solver.Add(z[j, k, l] <= y[j, l])
                    solver.Add(z[j, k, l] >= y[j, k] + y[j, l] - 1)
                    z_sum += z[j, k, l]
    solver.Add(z_sum <= beta)

    # minimize the sum of the variables
    solver.Minimize(sum(var))

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print(f"Objective value: {solver.Objective().Value()}")
        vars_used = []
        for v in var:
            if v.solution_value() == 1:
                vars_used.append(str(v))
        vars_used.sort()
        print(vars_used)
        return vars_used
    else:
        print("No solution exists")


or_solver("../test_txt_files/4x14.txt")
# solution count: 1
# optimal solution: [[], [1, 14], [2, 6], [7, 10], [9, 13]]