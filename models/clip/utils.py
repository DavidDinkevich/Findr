def merge_contiguous_tuples(arr):
    merged_arr = []
    for tup in arr:
        if not merged_arr or tup[0] > merged_arr[-1][1] + 1:
            merged_arr.append(tup)
        else:
            merged_arr[-1] = (merged_arr[-1][0], max(merged_arr[-1][1], tup[1]))
    return merged_arr
