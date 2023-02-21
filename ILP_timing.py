import timeit

# 7.545% speedup over 100000 executions with 10 data items, 4 clusters, and 14 tags (4x14.txt)
#           5.157% speedup in the second test

# print("Naive approach:")
a1 = timeit.timeit('a.ILP()', setup="import ILP_gurobi_generalized as a", number=5000)
# print("Non-naive approach:")
a2 = timeit.timeit('b.ILP_concise()',  setup="import ILP_gurobi_generalized_concise as b", number=5000)

print(f"Naive: {a1}")
print(f"Concise: {a2}")
print(f"{(1-(a2/a1))*100}% speedup")