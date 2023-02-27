from collections import deque
from numbers import Number
from random import randint
from statistics import median_low
from typing import NamedTuple

__all__ = [
    'quick_sort',
    'quick_sort_iterative',
    'quick_sort_inplace',
]


# сортируем по убыванию
def quick_sort(collection):
    lst = list(collection)
    if len(lst) <= 1:
        return lst
    if len(lst) == 2:
        if lst[0] < lst[1]:
            lst[0], lst[1] = lst[1], lst[0]
        return lst

    pivot = median_low(lst)

    return [
        *quick_sort([value for value in lst if value > pivot]),
        *[value for value in lst if value == pivot],
        *quick_sort([value for value in lst if value < pivot]),
    ]


# по возрастанию
def quick_sort_iterative(collection):
    #     нужен стек для проходов по подкускам или даже пара/тройка стеков
    result = []
    collection = list(collection)
    stack = deque()
    stack.append(collection)
    del collection
    while stack:
        to_sort = stack.pop()

        if len(to_sort) <= 1:
            result.extend(to_sort)
            continue
        if len(to_sort) == 2:
            if to_sort[0] > to_sort[1]:
                to_sort[0], to_sort[1] = to_sort[1], to_sort[0]
            result.extend(to_sort)
            continue

        pivot = median_low(to_sort)
        lt = [value for value in to_sort if value < pivot]
        eq = [value for value in to_sort if value == pivot]
        gt = [value for value in to_sort if value > pivot]

        if not lt and not gt:
            result.extend(eq)
            continue

        stack.extend((gt, eq, lt))

    return result


class SublistBounds(NamedTuple):
    """
    Represents left and right indices of sublist after partition.
    """
    left: int
    right: int

    @property
    def middle(self):
        """Get index of the middle element of sublist"""
        return (self.left + self.right + 1) // 2

    @property
    def size(self):
        """Get length of sublist"""
        return self.right - self.left + 1


def swap_items(lst, idx1, idx2):
    """
    Swaps two list values
    """
    lst[idx1], lst[idx2] = lst[idx2], lst[idx1]


def median_of_three(lst: list[Number], bounds: SublistBounds) -> Number:
    """Swaps first, middle and last elements of list inplace to make them sorted.
    Returns index of median (middle) element.
    """
    left = lst[bounds.left]
    mid = lst[bounds.middle]
    right = lst[bounds.right]
    if (left > mid) ^ (left > right):
        if mid > right:
            swap_items(lst, bounds.middle, bounds.right)
        swap_items(lst, bounds.left, bounds.middle)
    elif (mid < left) ^ (mid < right):
        if left > right:
            swap_items(lst, bounds.left, bounds.right)
    else:
        if left > mid:
            swap_items(lst, bounds.left, bounds.middle)
        swap_items(lst, bounds.middle, bounds.right)
    return lst[bounds.middle]


def dutch_partition(lst: list[Number], bounds: SublistBounds) -> tuple[SublistBounds, SublistBounds]:
    """
    There are several approaches to do partition:
    - https://opendsa-server.cs.vt.edu/embed/quicksortAV
    - original qsort.c https://codebrowser.dev/glibc/glibc/stdlib/qsort.c.html#151
    - dutch flag https://en.wikipedia.org/wiki/Dutch_national_flag_problem

    I'm going to implement a dutch flag approach for partition.
    Explanation could be found on youtube e.g. https://www.youtube.com/watch?v=sEQk8xgjx64

    This function returns a tuple of indices of:
    - the rightmost element in left group
    - the leftmost element in right group
    :param lst: list for partition
    :param bounds: tuple of right and left indexes of sublist
    """
    pivot = median_of_three(lst, bounds)
    mid = left = bounds.left
    right = bounds.right
    while mid <= right:
        if lst[mid] < pivot:
            swap_items(lst, mid, left)
            mid += 1
            left += 1
        elif lst[mid] == pivot:
            mid += 1
        else:  # lst[mid] > pivot
            swap_items(lst, mid, right)
            right -= 1

    # к концу цикла left будет указывать на начало средней группы (следующий элемент после конца левой)
    # mid будет указывать на начало правой группы (следующий элемент после конца средней)
    # right будет указывать на конец средней группы (предыдущий элемент перед началом последней)
    return SublistBounds(bounds.left, left - 1), SublistBounds(mid, bounds.right)


def append_bounds_to_stack_if_needed(lst: list, bounds: SublistBounds, stack: deque) -> None:
    """
    Processes bounds of new sublist after partition:
    - does nothing for list of 0..1 elements
    - swaps elements of list of 2 elements if necessary
    - appends list of 3 or more elements to stack

    :param lst: original list
    :param bounds: sublist bounds
    :param stack: stack to append sublist indices
    :return: None
    """
    if bounds.size > 2:
        stack.append(bounds)
    elif bounds.size == 2:
        if lst[bounds.left] > lst[bounds.right]:
            swap_items(lst, *bounds)


# сортируем по возрастанию
def quick_sort_inplace(lst: list[Number]) -> None:
    stack: deque[SublistBounds] = deque()
    append_bounds_to_stack_if_needed(lst, SublistBounds(0, len(lst) - 1), stack)
    while stack:
        current_bounds = stack.pop()
        left_sublist_bounds, right_sublist_bounds = dutch_partition(lst, current_bounds)
        if left_sublist_bounds.size > right_sublist_bounds.size:
            append_bounds_to_stack_if_needed(lst, left_sublist_bounds, stack)
            append_bounds_to_stack_if_needed(lst, right_sublist_bounds, stack)
        else:
            append_bounds_to_stack_if_needed(lst, right_sublist_bounds, stack)
            append_bounds_to_stack_if_needed(lst, left_sublist_bounds, stack)


if __name__ == '__main__':
    lists = [
        [randint(-100, 100) for _ in range(1000)],
        [],
        [0],
        [0, 0],
        [0, 0, 0],
        [1, 2, 3, 4],
        [4, 3, 2, 1],
    ]
    for lst in lists:
        res1 = quick_sort(lst)
        print(f'recursive: {res1 == sorted(lst, reverse=True)}')
        res2 = quick_sort_iterative(lst)
        print(f'iterative: {res2 == sorted(lst)}')
        quick_sort_inplace(lst)
        print(f'inplace: {lst == sorted(lst)}')