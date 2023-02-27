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

filename = "250-7-35-4-2.txt.txt"

# print("Naive approach:")
a1 = timeit.timeit(f'a.ILP(\"{filename}\")', setup="import ILP_gurobi_generalized as a", number=1)
# print("Non-naive approach:")
a2 = timeit.timeit(f'b.ILP_concise(\"{filename}\")',  setup="import ILP_gurobi_generalized_concise as b", number=1)

print(f"Generalized: {a1} seconds")
print(f"Concise: {a2} seconds")
print(f"{(((a1/a2)))} speedup factor")