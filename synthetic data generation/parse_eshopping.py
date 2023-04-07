import csv

# create an empty list that will store an item's cluster at each index
clusters_by_item = []
# create an empty list that will store an item's session id at each index
session_ids_by_item = []
# creat an empty list that will store an item's clothing model at each index
clothing_models_by_item = []
# open the csv file
with open('../test_txt_files/e-shop clothing 2008.csv', encoding='utf8') as shopping:
    # read the csv file
    csv_data = csv.reader(shopping, delimiter=';')
    # for each row in the csv file
    for row in csv_data:
        # if the row is not the row containing column names
        if row[0] != 'year':
            # create a list of tags in the row
            clusters_by_item.append(row[4])
            session_ids_by_item.append(row[5])
            clothing_models_by_item.append(row[7])

clothing_models = {}
for model in clothing_models_by_item:
    if model not in clothing_models:
        clothing_models[model] = len(clothing_models)

session_ids = {}
for id in session_ids_by_item:
    if id not in session_ids:
        session_ids[id] = int(id)

clusters = {}
for cluster in clusters_by_item:
    if cluster not in clusters:
        clusters[cluster] = int(cluster)

body = [[0 for i in range(len(clothing_models) + 2)] for j in range(len(session_ids))]

for i in range(len(session_ids_by_item)):
    session_index = session_ids[session_ids_by_item[i]] - 1
    model_index = clothing_models[clothing_models_by_item[i]] + 2
    body[session_index][0] = session_index + 1
    body[session_index][1] = clusters[clusters_by_item[i]]

    body[session_index][model_index] = 1

n = len(session_ids)
K = len(clusters)
N = len(clothing_models)
alpha = 1000
beta = 4

output_string = f"{n} {K} {N} {alpha} {beta} \n"
for row in body:
    for number in row:
        output_string += f"{number} "
    output_string += "\n"

with open(f"../test_txt_files/eshop_example.txt", 'w') as f:
    f.write(output_string)