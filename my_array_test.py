"""This file contains tests for Array class."""

from hypothesis import example, given
from hypothesis import strategies as st
from my_array import Array
from typing import List
from unittest import TestCase


class TestArray(TestCase):
    """This class tests that Array class was implemented correctly."""

    @given(lst=st.lists(st.integers()))
    @example(lst=[])
    @example(lst=[1])
    @example(lst=[1, 2, 3])
    def test_array_creation(self, lst):
        """Test that array can be created and has correct size and elements.

        Parameters:
            lst: list of elements we want to init with Array
        """
        my_array = Array(*lst)

        self.assertEqual(len(lst), len(lst))
        for elem1, elem2 in zip(lst, my_array):
            self.assertEqual(elem1, elem2)

    @given(lst=st.lists(st.text()), new_elems=st.lists(st.text()))
    @example(lst=[], new_elems=['Uno'])
    @example(lst=[], new_elems=['Uno', 'Dos', 'Tres'])
    def test_add_many_to_array(self, lst: List[int], new_elems: List[int]):
        """
        Test that we can append elements to the array.

        They must be appended in the right order.

        Parameters:
            lst: list of elements we want to init with Array
            new_elems: elements we want to append
        """
        array = Array(*lst)
        array_length = len(lst)

        for elem in new_elems:
            array.append(elem)

        self.assertEqual(
            array_length + len(new_elems),
            len(array),
        )
        for index, array_elem in enumerate(array):
            self.assertEqual(
                lst[index]
                if index < array_length
                else new_elems[index - array_length],
                array_elem,
            )

    @given(lst=st.lists(st.integers()), new_elem=st.integers())
    def test_copy_array(self, lst: List[int], new_elem: int):
        """
        Test that we can create a copy of the array.

        Changing the copy must not affect the original array.

        Parameters:
            lst: list of elements that we want to init with Array
            new_elem: element to append and check original array
        """
        original_array = Array(*lst)
        copied_array = original_array.copy()
        copied_array.append(new_elem)
        num_of_elems = len(lst)

        self.assertEqual(num_of_elems, len(original_array))
        self.assertEqual(num_of_elems + 1, len(copied_array))

    @given(
        elems1=st.lists(st.integers()),
        elems2=st.lists(st.integers()),
        new_elem=st.integers(),
    )
    @example(elems1=[], elems2=[1, 2, 3], new_elem=4)
    @example(elems1=[1, 2, 3], elems2=[], new_elem=4)
    @example(elems1=[], elems2=[], new_elem=4)
    def test_add_arrays(
        self,
        elems1: List[int],
        elems2: List[int],
        new_elem: int,
    ):
        """
        Test that we can add two arrays.

        Changing the result array must not affect the original arrays.

        Parameters:
            elems1: list of elements for the first Array
            elems2: list of elements for the second Array
            new_elem: element to append and check 1'st and 2'nd array
        """
        fst_array = Array(*elems1)
        snd_array = Array(*elems2)
        fst_array_length = len(elems1)
        snd_array_length = len(elems2)

        add_array = fst_array + snd_array
        add_array_length = fst_array_length + snd_array_length
        self.assertEqual(
            add_array_length,
            len(add_array),
        )

        add_array.append(new_elem)
        self.assertEqual(add_array_length + 1, len(add_array))
        self.assertEqual(fst_array_length, len(fst_array))
        self.assertEqual(snd_array_length, len(snd_array))

    @given(lst=st.lists(st.integers()), search_elem=st.integers())
    @example(lst=[1, 2, 3, 2], search_elem=2)
    @example(lst=[1, 2, 3], search_elem=4)
    def test_find_index_if_exists(self, lst: List[int], search_elem: int):
        """
        Test that index() finds the first occurrence of the element.

        Parameters:
            lst: list of elements that we want to init with Array
            search_elem: element that we want to find
        """
        array = Array(*lst)
        found_index = array.index(search_elem)
        expected_index = -1
        for index, elem in enumerate(lst):
            if elem == search_elem:
                expected_index = index
                break

        self.assertEqual(expected_index, found_index)

    @given(
        lst=st.lists(elements=st.integers()),
        search_index=st.integers(),
    )
    def test_get_elem_by_index(self, lst: List[int], search_index: int):
        """

        Test that we can get an element from the array by index.

        Parameters:
            lst: list of elements that we want to init with Array
            search_index: index of the element that we want to find

        Returns:
            object: return to avoid no-effect warning (expecting error)
        """
        array = Array(*lst)
        if search_index >= len(lst) or search_index < -len(lst):
            with self.assertRaises(IndexError):
                return array[search_index]
        else:
            found_elem = array[search_index]
            expected_elem = lst[search_index]
            self.assertEqual(expected_elem, found_elem)

    @given(lst_of_lsts=st.lists(st.lists(st.integers())))
    def test_array_of_arrays(self, lst_of_lsts: List[List[int]]):
        """
        Test that we can create array of arrays.

        Parameters:
            lst_of_lsts: list of lists we want to init with Array
        """
        array_with_arrays: Array = Array(*[Array(*lst) for lst in lst_of_lsts])
        self.assertEqual(len(lst_of_lsts), len(array_with_arrays))
        for lst_index, lst in enumerate(lst_of_lsts):
            array_elem: Array = array_with_arrays[lst_index]
            self.assertEqual(len(lst), len(array_elem))
            for elem_index, elem in enumerate(lst):
                self.assertEqual(elem, array_elem[elem_index])
