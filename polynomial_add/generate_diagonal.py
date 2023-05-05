
def output_file(data, dataset_name, dir="perturb_data"):
    """
    uses a dataset in list format to generate an output file
    :param data: a dataset in list format
    :param dataset_name: the name of the dataset
    :param iteration_number: the number that should be appended to the end of the filename
    :return: void
    """
    output_string = ""
    for row in data:
        for column in row:
            output_string += f"{column} "
        output_string += "\n"

    # create a new text file to store the perturbed tag set
    with open(f"{dir}/{dataset_name}.txt", "w") as f:
        # write the output file
        f.write(output_string)

def n_dimensional_diaognal(n):
    data = [[n, 1, n+1, n*2, 0]]

    for i in range(n):
        temp = [0 for i in range(n + 3)]
        temp[0] = i+1
        temp[1] = 1
        temp[i+2] = 1
        data.append(temp)

    output_file(data, f"{n}diagonal", "../test_txt_files")

    for i in range(1, len(data)):
        data[i][-1] = 1

    output_file(data, f"{n}diagonal_1", "../test_txt_files")

def n_dimensional_diaognal_split(n, f):
    data = [[n, 1, 3, 3, 0]]

    for i in range(n):
        temp = [0 for i in range(5)]

        temp[0] = i + 1
        temp[1] = 1
        if i < f:
            temp[2] = 1
        else:
            temp[3] = 1
        data.append(temp)


    output_file(data, f"{n}diagonal", "../test_txt_files")

    for i in range(1, len(data)):
        data[i][-1] = 1

    output_file(data, f"{n}diagonal_1", "../test_txt_files")

n_dimensional_diaognal_split(1000, 500)