# William Bradford
# wcb8ze
# generation script for k cluster problems

import random


def generate(n, K, N, alpha, beta, filename):
    output_s = f"{n} {K} {N} {alpha} {beta}\n"

    K_used_list = []
    for i in range(n):
        K_val = random.randint(1, K)
        while (K_val in K_used_list) and (len(K_used_list) < K):
            K_val = (K_val) % K + 1
        K_used_list.append(K_val)
        temp_s = f"{i+1} {K_val} "
        for j in range(N):
            temp_s += str(random.randint(0,1)) + " "
        temp_s += "\n"
        output_s += temp_s

    with open(filename+".txt", 'w') as f:
        f.write(output_s)

    tag_removed = output_s.split("\n")
    tag_removed_array = []
    tag = random.randint(2, N+1)
    for i in range(1, len(tag_removed)-1):
        row = tag_removed[i].split()
        del row[tag]
        tag_removed_array.append(row)

    tag_removed_s = ""
    first_row = tag_removed[0]
    new_first_row = ""
    for item in first_row.split():
        if item == f"{N}":
            item = f"{N-1}"
        new_first_row += f"{item} "

    tag_removed_s += new_first_row + "\n"

    for row in tag_removed_array:
        for element in row:
            tag_removed_s += f"{element} "
        tag_removed_s += "\n"

    with open(filename + f"_{tag-2}p.txt", 'w') as f:
        f.write(tag_removed_s)



def parameter_crunch(n):
    K = random.randint(2, n)
    N = random.randint(n, 10*n)
    alpha = random.randint(2, int(N/10))
    beta = 1
    filename = f"{n}n_{K}K_{N}N"
    generate(n, K, N, alpha, beta, filename)

parameter_crunch(20)