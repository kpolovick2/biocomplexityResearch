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

def add_tags_internal(desc, dataset, tag_added, items):
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

    new_desc = np.array([i for i in desc if i != -1])

    if len(tags_removed) > 0:
        return new_desc

    return desc


def add_tags(file, desc, new_file):
    data = parse_dataset(file)
    data = data[:-1] if len(data[-1]) == 0 else data
    data = np.array(data, dtype=np.ushort)
    new_data = parse_dataset(new_file)
    new_data = new_data[:-1] if len(new_data[-1]) == 0 else new_data
    new_data = np.array(new_data, dtype=np.ushort)
    tag_added = -1
    items = []



if __name__ == "__main__":
    add_tags_internal(random.sample(range(4), random.randint(1, 4)), np.array([[random.randint(0, 1) for j in range(4)] for i in range(4)], dtype=np.ushort), 2, [1, 2])