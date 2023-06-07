
def get_col(data, col):
    return [row[col] for row in data]


def get_key(data, col):
    key = get_col(data, col)
    key = [*set(key)]
    if "?" in key:
        key.remove("?")
    return key


def generate_ILP(name):
    with open(f"../UCI datasets/{name}.data") as f:
        input = f.read()

    data = [row.split(",") for row in input.split("\n")][:-1]

    col_key = [[] for i in range(len(data[0]))]

    for (i, row) in enumerate(col_key):
        col_key[i] = get_key(data, i)

    # set the clusters map to the
    clusters = {item: i+1 for (i, item) in enumerate(col_key[0])}
    col_key = col_key[1:]

    prev_len = 0
    for (i, c) in enumerate(col_key):
        col_key[i] = {v: j + prev_len for (j, v) in enumerate(c)}
        prev_len += len(c)

    # make the first line of the output file
    output = f"{len(data)} {len(clusters)} {prev_len} {prev_len} 1 \n"

    B = []
    for (i, row) in enumerate(data):
        temp = [0 for r in range(prev_len+2)]
        temp[0], temp[1] = i + 1, clusters[row[0]]
        for (j, item) in enumerate(row[1:]):
            if item != '?':
                temp[col_key[j][item]+2] = 1
        B.append(temp)

    for (i, row) in enumerate(B):
        temp = ""
        for item in row:
            temp += f"{item} "
        if i != len(B) - 1:
            temp += "\n"
        output += temp

    with open(f"../UCI datasets/{name}_data.txt", "w") as f:
        f.write(output)

def generate_ILP_clusters_last(name):
    with open(f"../UCI datasets/{name}.data") as f:
        input = f.read()

    data = [row.split(",") for row in input.split("\n")][:-1]

    col_key = [[] for i in range(len(data[0]))]

    for (i, row) in enumerate(col_key):
        col_key[i] = get_key(data, i)

    # set the clusters map to the
    clusters = {item: i+1 for (i, item) in enumerate(col_key[-1])}
    col_key = col_key[:-1]

    prev_len = 0
    for (i, c) in enumerate(col_key):
        col_key[i] = {v: j + prev_len for (j, v) in enumerate(c)}
        prev_len += len(c)

    # make the first line of the output file
    output = f"{len(data)} {len(clusters)} {prev_len} {prev_len} 1 \n"

    B = []
    for (i, row) in enumerate(data):
        temp = [0 for r in range(prev_len+2)]
        temp[0], temp[1] = i + 1, clusters[row[0]]
        for (j, item) in enumerate(row[1:]):
            if item != '?':
                temp[col_key[j][item]+2] = 1
        B.append(temp)

    for (i, row) in enumerate(B):
        temp = ""
        for item in row:
            temp += f"{item} "
        if i != len(B) - 1:
            temp += "\n"
        output += temp

    with open(f"../UCI datasets/{name}_data.txt", "w") as f:
        f.write(output)


generate_ILP_clusters_last("iris")