
def get_col(data, col):
    return [row[col] for row in data]


def get_key(data, col):
    c = get_col(data, col)
    return [*set(c)]


with open("../UCI datasets/agaricus-lepiota.data") as f:
    input = f.read()

data = [row.split(",") for row in input.split("\n")][:-1]

for row in data:
    print(row)

print(get_key(data, 0))