import timeit

# ------------- Timing with constraint C optimization --------------
# the concise implementation (which I will now refer to as optimized)
# 92.455% of the time of the naive implementation
# (8.16% speedup)
# over 100000 executions with 10 data items, 4 clusters, and 14 tags (4x14.txt)
#           94.825% in the second test
#           (5.46% speedup)
# 49.802% of the time over 5000 executions with 20 data items, 9 clusters, and 28 tags (9x28.txt)
#           (100.8% speedup)
# 10.795% of the time over 1000 executions with 38 data items, 16 clusters, and 56 tags (16x56.txt)
#           (826.3% speedup)
# negligible speedup for large values of n or N with small values of K
# 17735.92% speedup for 39_clusters.txt on a singular execution

# ------------- Timing on 1000n_20K_20N_250a_200b.txt --------------
# Testing done on Intel i9-9880H CPU @ 2.30 GHz
# Generalized: 24.8271618 seconds per execution
# -------------------------
# Concise: 25.1950017 seconds per execution
# 0.9854002827870418 speedup factor
# -------------------------
# Gurobi Linearized: 25.7550016 seconds per execution
# 0.9639743839115117 speedup factor
# -------------------------
# Linearized: 3.6334454999999934 seconds per execution
# 6.83295285425364 speedup factor

# ------------- Timing on 1000n_20K_20N_250a_200b.txt --------------
# Testing done on Intel i9-9880H CPU @ 2.30 GHz
# Generalized did not terminate after multiple hours of execution
# Linearized: 1.2935439 seconds per execution

# TODO: document running time of generation and solving separately
#               run on n=1000, n=10000, n=100000

filename = "test_txt_files/eshop_example.txt"
test_count = 1

# generalized_time = timeit.timeit(f'a.ILP(\"{filename}\")', setup="import ILP_gurobi_generalized as a", number=test_count)
concise_time = timeit.timeit(f'b.ILP_concise(\"{filename}\")',  setup="import ILP_gurobi_generalized_concise as b", number=test_count)
g_linearized_time = timeit.timeit(f'c.ILP_linear_g(\"{filename}\")', setup="import ILP_linear_g_optimized as c", number=test_count)
linearized_time = timeit.timeit(f'd.ILP_linear(\"{filename}\")', setup="import ILP_linear as d", number=test_count)

# print(f"Generalized: {generalized_time/test_count} seconds per execution")
print("-------------------------")
print(f"Concise: {concise_time/test_count} seconds per execution")
# print(f"{generalized_time/concise_time} speedup factor")
print("-------------------------")
print(f"Gurobi Linearized: {g_linearized_time/test_count} seconds per execution")
# print(f"{generalized_time/g_linearized_time} speedup factor")
print("-------------------------")
print(f"Linearized: {linearized_time/test_count} seconds per execution")
# print(f"{generalized_time/linearized_time} speedup factor")