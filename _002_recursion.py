def countdown(number):
    print(number)
    if number <= 1:
        return
    countdown(number - 1)


# countdown(5):
#     print(5)
#     countdown(4):
#         print(4)
#         countdown(3):
#             print(3)
#             countdown(2):
#                 print(2)
#                 countdown(1):
#                     print(1)
#                     return
#                 return
#             return
#         return
#     return
#

def countdown_(number):
    if number <= 1:
        print(number)
        return
    countdown_(number - 1)
    print(number)

#
# countdown_(5):
#     countdown_(4):
#         countdown_(3):
#             countdown_(2):
#                 countdown_(1):
#                     print(1)
#                     return
#                 print(2)
#                 return
#             print(3)
#             return
#         print(4)
#         return
#     print(5)
#     return


# базовый случай – объект не является словарём
# возвращаем его ключ с parent_key и значение

# рекурсивный случай – объект является словарём
# вызываем рекурсивно функцию, parent_key = parent_key + key

# нужно все значения собирать


def flatten_dict_keys(dikt: dict, parent_key='', flattened_dict=None):
    if flattened_dict is None:
        flattened_dict = dict()

    for k, v in dikt.items():
        flattened_key = f'{parent_key}_{k}' if parent_key else str(k)
        if not isinstance(v, dict):
            flattened_dict[flattened_key] = v
        else:
            flatten_dict_keys(v, flattened_key, flattened_dict)

    return flattened_dict






dikt = {
    'lol': 'kek',
    'user': {
        'name': {
            'first': 'Данила',
            'second': 'Камаев',
        },
        'login': 'kamaeff'
    },
    'role': {
        'id': 123,
        'slug': 'qa-engineer'
    }
}

flatten_dict_keys(dikt)





"""
Внезапно, это имеет смысл. В функциональщине типа нет изменяемых переменных, но есть функции.
В примере в книге стр 84 приводится haskell:
```haskell
sum [] = 0
sum (x:xs) = x + sum(xs)

В случае итеративного варианта у нас появляется больше мутабельности – в переменной–накопителе суммы result:
def sum(arr):
    result = 0
    for i in arr:
        result += i
    return result

Или типа того.
http://learnyouahaskell.com/recursion
https://www.reddit.com/r/haskell/comments/1nb80j/proper_use_of_recursion_in_haskell/
https://en.wikibooks.org/wiki/Haskell/Recursion

"""




def sum(arr):
    if not arr:
        return 0
    return arr[0] + sum(arr[1:])


print(sum([1,2,3,4]))



def count(arr):
    if not arr:
       return 0
    return 1 + count(arr[1:])

print(count([1,2,3,4]))


def max_(arr):
    if len(arr) == 1:
        return arr[0]
    if len(arr) == 2:
        if arr[0] > arr[1]:
            return arr[0]
        else:
            return arr[1]
    return max_([arr[0], max(arr[1:])])

print(max_([1,2,3,4,5,0,9,6,7,-12321,909090, 512, -0.9, -17]))