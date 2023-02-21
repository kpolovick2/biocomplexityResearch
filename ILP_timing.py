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

# print("Naive approach:")
a1 = timeit.timeit('a.ILP()', setup="import ILP_gurobi_generalized as a", number=25)
# print("Non-naive approach:")
a2 = timeit.timeit('b.ILP_concise()',  setup="import ILP_gurobi_generalized_concise as b", number=25)

print(f"Naive: {a1}")
print(f"Concise: {a2}")
print(f"{((1/(a2/a1)) - 1)*100}% speedup")