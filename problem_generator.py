# William Bradford
# wcb8ze
# generation script for k cluster problems

import random

# request: input total number of tags, total number of data items, total number of clusters,
# max tags/data item

def generate(n, K, N, alpha, beta, filename):
    output_s = f"{n} {K} {N} {alpha} {beta}\n"
    output_s_p = f"{n} {K} {N} {alpha} {beta}\n"
    perturb = random.randint(0, N)

    K_used_list = []
    for i in range(n):
        K_val = random.randint(1, K)
        while (K_val in K_used_list) and (len(K_used_list) < K):
            K_val = (K_val) % K + 1
        K_used_list.append(K_val)
        temp_s = f"{i+1} {K_val} "
        temp_s_p = f"{i+1} {K_val} "
        for j in range(N):
            x = str(random.randint(0,1))
            temp_s += x + " "
            if j != perturb:
                temp_s_p += x + " "
            else:
                temp_s_p += "0 "
        temp_s += "\n"
        temp_s_p += "\n"
        output_s += temp_s
        output_s_p += temp_s_p

    with open(filename+".txt", 'w') as f:
        f.write(output_s)

    with open(f"{filename}_{perturb+1}p.txt", 'w') as f:
        f.write(output_s_p)


def parameter_crunch(n):
    K = random.randint(2, n)
    N = random.randint(n, 10*n)
    alpha = random.randint(2, int(N/10))
    beta = 1
    filename = f"{n}n_{K}K_{N}N"
    generate(n, K, N, alpha, beta, filename)

generate(250, 7, 35, 4, 2, "250-5-35-4-2.txt")