from utils import print_results

@print_results
def euclidean(a, b):
    """Euclidean algorithm to find Greatest Common Divisor for two integers."""
    if a < b:
        a, b = b, a
    modulo = a % b
    if not modulo:
        return b
    return euclidean(b, modulo)


@print_results
def euclidean_iterative(a, b):
    if a < b:
        a, b = b, a
    while modulo := a % b:
        a, b = b, modulo
    return b


assert euclidean(6, 21) == euclidean_iterative(6, 21)
assert euclidean(7, 21) == euclidean_iterative(7, 21)
assert euclidean(75, 21232) == euclidean_iterative(75, 21232)
assert euclidean(75, 21235) == euclidean_iterative(75, 21235)
assert euclidean(75, 21235123312) == euclidean_iterative(75, 21235123312)
assert euclidean(12, 21235123312) == euclidean_iterative(12, 21235123312)