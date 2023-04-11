"""
Хочу реализовать хеш-таблицу сам.
Да, нет особо смысла на пайтоне это делать, кроме как хорошечно понять.
Да и в целом смысла кроме как понять и что-то ещё по ходу дела поузнавать делать хеш-таблицу самому нет.
Но хочу. Просто чтобы продолжать в том же духе – прочёл -> сделал.

Что мне нужно?
1. Список (массив) фиксированной длины для хранения значений словаря
2. Хеш-функция для получения индекса – для сохранения и получения значений словаря по ключу
3. Логика для увеличения размера массива и перераспределения существующих элементов в новом массиве
4. Связанный список для добавления нескольких элементов по одному индексу, если индексы совпали
"""

from typing import Hashable, MutableMapping, Optional, Iterator, Any

from _000_linked_list import LinkedList

DEFAULT_ARRAY_SIZE = 50
ARRAY_EXTENDING_THRESHOLD_RATIO = 0.7
ARRAY_EXTENDING_FACTOR = 2
ARRAY_REDUCING_THRESHOLD_RATIO = 0.2
ARRAY_REDUCING_DENOMINATOR = 2
KEY_ERROR_MESSAGE = 'No such key:{key}'


class HashMapItem:
    def __init__(self, key: Hashable,  value: Any):
        self.key = key
        self.value = value


class HashMapLinkedList(LinkedList):
    """LinkedList to store HashMap values under the same index in case of hash collision."""
    def find_item_by_key(self, key: Hashable) -> Optional[HashMapItem]:
        for item in self:
            if item.key == key:
                return item

    def add_item(self, item):
        existing_item = self.find_item_by_key(item.key)
        if existing_item:
            existing_item.value = item.value
        else:
            self.push(item)

    def delete_item_by_key(self, key):
        for index, item in enumerate(self):
            if item.key == key:
                del self[index]
                return
        raise KeyError(KEY_ERROR_MESSAGE.format(key=key))

    def keys(self):
        return {item.key for item in self}

    def values(self):
        return [item.value for item in self]


class HashMap(MutableMapping):
    def __init__(self):
        self._init_array()

    def _set_item(self, key: Hashable, value: Any) -> None:
        item = HashMapItem(key, value)
        index, current_entry = self._get_entry_by_key(key)
        if current_entry:
            current_entry.add_item(item)
        else:
            self.array[index] = HashMapLinkedList((item,))

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self._set_item(key, value)
        self._update_array_length()

    def _del_item(self, key: Hashable) -> None:
        index, current_entry = self._get_entry_by_key(key)
        if not current_entry:
            raise KeyError(KEY_ERROR_MESSAGE.format(key=key))
        current_entry.delete_item_by_key(key)
        if not current_entry:
            self.array[index] = None

    def __delitem__(self, key: Hashable) -> None:
        self._del_item(key)
        self._update_array_length()

    def _get_item(self, key: Hashable) -> Any:
        _, current_entry = self._get_entry_by_key(key)
        item = current_entry.find_item_by_key(key) if current_entry else None
        if item is None:
            raise KeyError(KEY_ERROR_MESSAGE.format(key=key))
        return item.value

    def __getitem__(self, key: Hashable) -> Any:
        return self._get_item(key)

    def __len__(self) -> int:
        return len(self.keys())

    def __iter__(self) -> Iterator:
        yield from self.keys()

    def __repr__(self):
        key_value_pairs = ", ".join(f"{key!r}: {value!r}" for key, value in self.items())
        return f'{self.__class__.__name__} {{{key_value_pairs}}}'

    def keys(self) -> set:
        keys = set()
        for entry in self.array:
            if entry:
                keys |= entry.keys()
        return keys

    def values(self) -> list:
        values = []
        for entry in self.array:
            if entry:
                values.extend(entry.values())
        return values

    def items(self) -> Iterator:
        for entry in self.array:
            if entry:
                for item in entry:
                    yield item.key, item.value

    def _init_array(self, size=DEFAULT_ARRAY_SIZE):
        self.array: list = [None] * size

    def _get_entry_by_key(self, key: Hashable) -> tuple[int, Optional[HashMapLinkedList]]:
        index = hash(key) % len(self.array)
        return index, self.array[index]

    def _update_array_length(self):
        need_to_update = False
        current_array_len = len(self.array)
        current_ratio = len(self) / current_array_len

        if current_ratio >= ARRAY_EXTENDING_THRESHOLD_RATIO:
            need_to_update = True
            new_array_len = current_array_len * ARRAY_EXTENDING_FACTOR
        elif current_ratio <= ARRAY_REDUCING_THRESHOLD_RATIO and current_array_len > DEFAULT_ARRAY_SIZE:
            need_to_update = True
            new_array_len = current_array_len // ARRAY_REDUCING_DENOMINATOR

        if need_to_update:
            items = [item for item in self.items()]
            self._init_array(new_array_len)
            for k, v in items:
                self._set_item(k,v)


    def print_internals(self):
        print(f'{len(self.array)=}')
        # for i, entry in enumerate(self.array):
        #     if entry:
        #         print(i)
        #         for j, item in enumerate(entry):
        #             print(f'    {j}. {item.key}: {item.value}')


a = HashMap()

for i in range(400):
    print(i)
    a[i] = i
    print(f"{len(a)=}")
    a.print_internals()

for key, value in a.items():
    print(f"{key=}, {value=}")

for i in range(400):
    print(i)
    del a[i]
    print(f"{len(a)=}")
    a.print_internals()
