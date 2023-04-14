

from answer_to_data import *
from ILP_linear import *

n, K, N, alpha, beta = 300, 6, 40, 4, 1

generate(n=n, K=K, N=N, alpha=alpha, beta=beta, min_alpha=2, min_tags=4, max_tags=9, min_items=35,
         max_items=70, percent_overlap=0)

filename = f"../test_txt_files/{n}n_{K}K_{N}N_{alpha}a_{beta}b.txt"

ILP_linear(filename)