def sort_sets(sets):
    overlap = [0 for i in range(len(sets))]

    for (i, s1) in enumerate(sets):
        for (j, s2) in enumerate(sets):
            if s1 == s2 and i != j:
                del sets[j]

    for (i, s1) in enumerate(sets):
        for (j, s2) in enumerate(sets):
            for e in s1:
                if e in s2 and i != j:
                    overlap[i] += 1

    return [x for _, x in sorted(zip(overlap, sets))]


S = [[1, 3], [1, 2], [3, 4], [1, 3]]

sort_sets(S)
