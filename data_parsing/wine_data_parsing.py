import math


with open("../UCI datasets/wine/wine.data") as f:
    input = f.read()

data = input.split("\n")
data = [row.split(",") for row in data][:-1]

for (j, row) in enumerate(data):
    for (i, item) in enumerate(row):
        if item == "":
            data[j][i] = -1

# extract the desired categories
data = [[float(i) for i in row] for row in data]
clusters = [row[0] for row in data]
ash = [row[2] for row in data]
phenol = [row[5] for row in data]
proline = [row[12] for row in data]

# use extracted categories to create a list of tags corresponding to the values of each category
cluster_dict = {i: int(i) for i in [*set(clusters)]}
ash_dict = {val: i for (i, val) in enumerate([*set(ash)])}
phenol_dict = {val: i + len(ash_dict) for (i, val) in enumerate([*set(phenol)])}
proline_dict = {val: i + len(ash_dict) + len(phenol_dict) for (i, val) in enumerate([*set(proline)])}

print(f"{len(ash)} : {len(ash_dict)}")
print(f"{len(phenol)} : {len(phenol_dict)}")
print(f"{len(proline)} : {len(proline_dict)}")

n = len(ash)
K = len(cluster_dict)
N = len(ash_dict) + len(phenol_dict) + len(proline_dict)
alpha = 133
beta = 1

output = f"{n} {K} {N} {alpha} {beta} \n"

dataset = [[0 for i in range(N + 2)] for j in range(len(clusters))]

for (i, row) in enumerate(dataset):
    dataset[i][0] = i + 1
    dataset[i][1] = cluster_dict[clusters[i]]
    dataset[i][ash_dict[ash[i]]+2] = 1
    dataset[i][phenol_dict[phenol[i]]+2] = 1
    dataset[i][proline_dict[proline[i]]+2] = 1

for (i, row) in enumerate(dataset):
    for item in row:
        output += f"{item} "
    if i != len(dataset) - 1:
        output += "\n"

with open("../UCI datasets/wine/wine_data.txt", "w") as f:
    f.write(output)
