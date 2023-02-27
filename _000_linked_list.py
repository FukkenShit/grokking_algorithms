from typing import Optional


class ListNode:
    def __init__(self, value, next_=None):
        self.value = value
        self.next: Optional[ListNode] = next_


class LinkedList:
    def __init__(self, iterable=None):
        self.size = 0
        self.first: Optional[ListNode] = None
        if iterable is not None:
            self.extend(iterable)

    def extend(self, iterable):
        previous_node: Optional[ListNode] = self._get_last_node() if self else None
        for i in iterable:
            node: ListNode = ListNode(i)
            if previous_node is None:
                self.first = node
            else:
                previous_node.next = node
            previous_node = node
        self.size += len(iterable)

    def push(self, value):
        node = ListNode(value)
        node.next = self.first
        self.first = node
        self.size += 1

    def __reversed__(self):
        new_list: LinkedList = self.__class__()
        for i in self:
            new_list.push(i)
        return new_list

    def _get_last_node(self):
        if not self:
            raise IndexError
        last_node = self.first
        while last_node.next is not None:
            last_node = last_node.next
        return last_node

    def append(self, value):
        node = ListNode(value)
        if self.first is None:
            self.first = node
        else:
            self._get_last_node().next = node
        self.size += 1

    def _prepare_index(self, index):
        if index >= self.size or index < -self.size:
            raise IndexError
        if index < 0:
            index = self.size + index
        return index

    def _get_node_by_index(self, index):
        node = self.first
        for _ in range(index):
            node = node.next
        return node

    def popleft(self):
        if not self:
            raise IndexError("Attempting to pop from empty LinkedList")
        value = self.first.value
        self.first = self.first.next
        self.size -= 1
        return value

    def pop(self, index=None):
        if not self:
            raise IndexError("Attempting to pop from empty LinkedList")
        if index is None:
            index = self.size - 1
        index = self._prepare_index(index)

        previous_node: Optional[ListNode] = None
        node: ListNode = self.first
        for _ in range(index):
            previous_node, node = node, node.next

        if previous_node is not None:
            previous_node.next = node.next
        else:
            self.first = node.next
        self.size -= 1
        return node.value

    def __getitem__(self, index):
        index = self._prepare_index(index)
        node = self._get_node_by_index(index)
        return node.value

    def __setitem__(self, index, value):
        index = self._prepare_index(index)
        node = self._get_node_by_index(index)
        node.value = value

    def __iter__(self):
        node = self.first
        while node is not None:
            yield node.value
            node = node.next

    def reverse(self):
        self.first = reversed(self).first

    def __str__(self):
        return f'[{", ".join(str(value) for value in self)}]'

    def __repr__(self):
        return f'{self.__class__.__name__}[{", ".join(repr(value) for value in self)}]'

    def __len__(self):
        return self.size


lst = LinkedList()

for i in range(10):
    print(i)
    lst.append(i)

for i in lst:
    print(i)
print(lst)

for i in range(lst.size):
    print(lst.pop())
