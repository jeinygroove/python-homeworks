"""This module contains implementation of the Array class."""

from __future__ import annotations
from typing import Optional, Tuple


class Node(object):
    """
    Represents a node which contains value and reference to the next node.

    Attributes:
        _node_value: some object that node keeps
        _next: next Node
    """

    __slots__ = ('_node_value', '_next')

    def __init__(self, node_value) -> None:
        """
        Init Node.

        Parameters:
            node_value: some object that this node will be keeping
        """
        self._node_value = node_value
        self._next: Optional[Node] = None

    def __eq__(self, other: Optional[object]) -> bool:
        """
        Check if two nodes are equal.

        Parameters:
            other: some object

        Returns:
            True if values are equal and False instead
        """
        if not isinstance(other, Node):
            return False
        return self._node_value == other.get_value()

    def set_next(self, next_node: Optional[Node]):
        """
        Set next node.

        Parameters:
            next_node: next node.
        """
        self._next = next_node

    def get_next(self) -> Optional[Node]:
        """
        Get next node.

        Returns:
            Node: next node or None if node doesn't have the next one.
        """
        return self._next

    def get_value(self) -> object:
        """
        Get value of the node.

        Returns:
             object: value of the node.
        """
        return self._node_value


class Array(object):
    """
    Represents array of objects.

    Attributes:
        _num_of_elems: size of the array
        _array_ends: the first and the last element of the array
    """

    __slots__ = ('_num_of_elems', '_array_ends')

    def __init__(self, *args) -> None:
        """
        Init array with given elements.

        Parameters:
            args: array elements
        """
        self._num_of_elems = 0
        self._array_ends: Tuple[Optional[Node], Optional[Node]] = (None, None)
        for array_elem in args:
            self.append(array_elem)

    def __eq__(self, other: Optional[object]) -> bool:
        """
        Check if arrays are equal.

        Parameters:
            other: some object.

        Returns:
            True if all corresponding elements of two arrays are equal.
        """
        if not isinstance(other, Array) or self._num_of_elems != len(other):
            return False
        for elem1, elem2 in zip(self, other):
            if elem1 != elem2:
                return False
        return True

    def __len__(self) -> int:
        """
        Get number of elements in the array.

        Returns:
             int: number of elements
        """
        return self._num_of_elems

    def append(self, elem: object):
        """
        Add element at the end of the array.

        Parameters:
            elem: value of the new element

        Raises:
            TypeError: if state of the object is illegal
        """
        self._num_of_elems += 1
        head, tail = self._array_ends
        if head is None:
            head = Node(elem)
            self._array_ends = (head, head)
            return
        new_tail: Node = Node(elem)
        if tail is None:
            raise TypeError('Unexpected error: tail is None when head is not')
        tail.set_next(new_tail)
        self._array_ends = (head, new_tail)

    def __copy__(self) -> Array:
        """
        Create copy of the array.

        Returns:
             Array: copy of the array
        """
        array_copy = Array()
        for elem in self:
            array_copy.append(elem)
        return array_copy

    def __add__(self, other: Array) -> Array:
        """
        Concatenate two arrays.

        Parameters:
            other: second array

        Returns:
            Array: new array, the result of concatenation
        """
        fst_arr = self.copy()
        snd_arr = other.copy()
        if not len(fst_arr):
            return snd_arr
        for elem in snd_arr:
            fst_arr.append(elem)
        return fst_arr

    def index(self, elem: object) -> int:
        """
        Get index of the first occurrence of the given value.

        Parameters:
            elem: value that we are looking for

        Returns:
            int: index of given value in the array
             or -1 if there's no such value.
        """
        index = 0
        for arr_elem in self:
            if arr_elem == elem:
                return index
            index += 1
        return -1

    def __getitem__(self, index: int):
        """
        Access element of the array by index.

        Parameters:
            index: index in the array

        Returns:
            object: element of the array with this index.

        Raises:
            IndexError: if index is out of the array.
            TypeError: if state of the object is illegal
        """
        if index < 0:
            index += self._num_of_elems
        if index >= self._num_of_elems or index < 0:
            raise IndexError
        node = self._array_ends[0]
        while index != 0 and node is not None:
            node = node.get_next()
            index -= 1
        if node is None:
            raise TypeError('Node that must exist is None.')
        return node.get_value()

    def pop(self):
        """
        Remove the last element from the array.

        Raises:
            IndexError: if array is empty.
            TypeError: if state of the object is illegal.
        """
        if not self._num_of_elems:
            raise IndexError
        curr_node = self._array_ends[0]
        prev_node = None
        if curr_node is None:
            raise TypeError(
                'number of elements is positive' +
                " but front element doesn't exist.",
            )
        next_node = curr_node.get_next()
        while next_node is not None:
            prev_node = curr_node
            curr_node = next_node
            next_node = curr_node.get_next()
        if prev_node is not None:
            prev_node.set_next(None)
        self._num_of_elems -= 1

    def remove(self, elem: object):
        """
        Remove the first occurrence of the given element.

        Parameters:
            elem: element
        """
        if not self._num_of_elems:
            return

        curr_node = self._array_ends[0]
        prev_node = None
        while curr_node is not None and curr_node.get_value() != elem:
            prev_node = curr_node
            curr_node = curr_node.get_next()
        if curr_node is not None:
            if prev_node is None:
                new_head = curr_node.get_next()
                if new_head is None:
                    self._array_ends = (new_head, new_head)
                else:
                    self._array_ends = (new_head, self._array_ends[1])
            elif curr_node.get_next() is None:
                self._array_ends = (self._array_ends[0], prev_node)
            else:
                prev_node.set_next(curr_node.get_next())
        self._num_of_elems -= 1

    def __str__(self) -> str:
        """
        Convert array to string.

        Returns:
            str: string representation of the array.
        """
        arr_string = '['
        first = True
        for elem in self:
            if first:
                first = False
            else:
                arr_string = '{0}, '.format(arr_string)
            arr_string += str(elem)
        return '{0}]'.format(arr_string)

    def __iter__(self) -> ArrayIterator:
        """
        Return iterator for the array.

        Returns:
            ArrayIterator: array iterator
        """
        return ArrayIterator(self)

    def copy(self) -> Array:
        """
        Create copy of the array.

        Returns:
            Array: copy of the array
        """
        return self.__copy__()


class ArrayIterator(object):
    """
    Represents iterator for the array.

    Attributes:
        array_ref: Array object to which it refers
        curr_index: current index
    """

    __slots__ = ('array_ref', 'curr_index')

    def __init__(self, array: Array):
        """
        Init array iterator for given array.

        Parameters:
            array: array
        """
        self.array_ref = array
        self.curr_index = 0

    def __iter__(self) -> ArrayIterator:
        """
        Get iterator.

        Returns:
            ArrayIterator: self
        """
        return self

    def __next__(self) -> object:
        """
        Get next element of the array.

        Returns:
            object: element from the array.

        Raises:
            StopIteration: when current node is None.
        """
        if self.curr_index < len(self.array_ref):
            elem = self.array_ref[self.curr_index]
            self.curr_index += 1
            return elem
        raise StopIteration
