import numpy as np
import random
from dataset_perturbing.perturb_utilities import *
# import one_cluster_ilp as ILP


def mut_vec_diff(v1, v2):
    """
    returns the difference between two vectors stored in the first vector
    :param v1: the first vector
    :param v2: the second vector
    :return: void
    """
    min = math.inf
    for (i, v) in enumerate(v2):
        v1[i] -= v
        min = v1[i] if v1[i] < min else min
    return min


# def thread_vec_diff(v1, v2):
#     thread.start_new_thread(mut_vec_diff(v1[len(v1) // 2:], v2[len(v2) // 2:]))
#     thread.start_new_thread(mut_vec_diff(v1[:len(v1) // 2], v2[:len(v2) // 2]))
#     return

def add_tags_internal(dataset, desc, tag_added, items):
    vec_desc = np.zeros(shape=(len(desc) + 1, len(dataset)), dtype=np.ushort)
    for (i, t) in enumerate(desc):
        for (j, item) in enumerate(dataset[:, t]):
            vec_desc[i, j] = item

    desc_sum = np.sum(vec_desc, axis=0, dtype=np.ushort)

    added_vec = dataset[:, tag_added]
    for item in items:
        added_vec[item] += 1

    desc_sum += added_vec

    tags_removed = []

    for (i, t) in enumerate(desc):
        desc_sum -= dataset[:, t]
        if np.min(desc_sum) < 1:
            desc_sum += dataset[:, t]
        else:
            tags_removed.append(i)

    for idx in tags_removed:
        desc[idx] = -1

    new_desc = [i for i in desc if i != 4294967295]
    new_desc.append(t)
    new_desc = np.array(new_desc)

    if len(tags_removed) > 0:
        return new_desc
    return desc


def add_tags(file, desc, new_file):
    data = parse_dataset(file)
    # while len(data[0]) < len(data[1]):
    #     data[0].append(0)
    data = data[:-1] if len(data[-1]) == 0 else data
    data = np.array(data, dtype=np.ushort)
    new_data = parse_dataset(new_file)
    # while len(new_data[0]) < len(new_data[1]):
    #     new_data[0].append(0)
    new_data = new_data[:-1] if len(new_data[-1]) == 0 else new_data
    new_data = np.array(new_data, dtype=np.ushort)
    tag_added = -1
    items = []
    for (i, item) in enumerate(data):
        # for each tag value in the item
        for (j, t) in enumerate(item):
            # if the two datasets do not match
            if t != new_data[i][j]:
                # set tag_added to the tag
                tag_added = j - 1
                # add i to the list of items
                items.append(i)

    if tag_added == -1:
        return desc
    return add_tags_internal(data, np.array(desc, dtype=np.uint), tag_added, np.array(items, dtype=np.uint))



if __name__ == "__main__":
    print(add_tags("../test_txt_files/1000diagonal.txt", list(range(1,3)), "../test_txt_files/1000diagonal_1.txt"))
    # add_tags_internal(random.sample(range(4), random.randint(1, 4)), np.array([[random.randint(0, 1) for j in range(4)] for i in range(4)], dtype=np.ushort), 2, [1, 2])