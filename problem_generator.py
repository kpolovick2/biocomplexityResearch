# William Bradford
# wcb8ze
# generation script for k cluster problems

import random

def generate(n,K,N,alpha, beta):

    output_s = f"{n} {K} {N} {alpha} {beta}\n"

    for i in range(n):
        temp_s = f"{i+1} {random.randint(1, K)} "
        for j in range(N):
            temp_s += str(random.randint(0,1)) + " "
        temp_s += "\n"
        output_s += temp_s

    print(output_s)

generate(100,39,250,7,1)