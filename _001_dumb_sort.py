from random import randint


def dumb_sort(iterable):
    original = list(iterable)
    if not original:
        return original

    sorted_ = list()
    while original:
        max_value = original[0]
        max_idx = 0
        for idx, value in enumerate(original):
            if value >= max_value:
                max_value = value
                max_idx = idx
        sorted_.append(original.pop(max_idx))

    return sorted_


lst = [randint(0,100) for _ in range(100)]
sorted_lst = dumb_sort(lst)

print(lst)
print(sorted_lst)