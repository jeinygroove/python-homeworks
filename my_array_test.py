"""This file contains tests for Array class."""

from unittest import TestCase

from my_array import Array


class TestArray(TestCase):
    """This class tests that Array class was implemented correctly."""

    def test_empty_array_creation(self):
        """Test that empty array can be created and it has 0 size."""
        empty_array = Array()

        self.assertEqual(0, len(empty_array))

    def test_one_elem_array_creation(self):
        """
        Test that one element array can be created.

        It has size 1 and correct element.
        """
        one_elem_array = Array(1)

        self.assertEqual(1, len(one_elem_array))
        self.assertEqual(1, one_elem_array[0])

    def test_many_elem_array_creation(self):
        """
        Test that array with N elements can be created.

        It has size N and its elements are in the right order.
        """
        many_elem_array = Array(1, 2, 3)

        self.assertEqual(3, len(many_elem_array))
        self.assertEqual(1, many_elem_array[0])
        self.assertEqual(2, many_elem_array[1])
        self.assertEqual(3, many_elem_array[2])

    def test_append_to_empty_array(self):
        """Test that we can append element to empty array."""
        array = Array()
        new_elem = 'Jerry'

        array.append(new_elem)

        self.assertEqual(1, len(array))
        self.assertEqual(new_elem, array[0])

    def test_add_many_to_array(self):
        """
        Test that we can append many elements to the array.

        They must be appended in the right order.
        """
        array = Array()
        new_elems = 'Uno', 'Dos', 'Tres'

        for elem in new_elems:
            array.append(elem)

        self.assertEqual(len(new_elems), len(array))
        for index, arr_elem in enumerate(array):
            self.assertEqual(new_elems[index], arr_elem)

    def test_copy_array(self):
        """
        Test that we can create a copy of the array.

        Changing the copy must not affect the original array.
        """
        original_array = Array(1, 2, 3)
        copied_array = original_array.copy()
        copied_array.append(4)

        self.assertEqual(3, len(original_array))
        self.assertEqual(4, len(copied_array))

    def test_add_arrays(self):
        """
        Test that we can add two arrays.

        Changing the result array must not affect the original arrays.
        """
        fst_array = Array(1, 2, 3)
        snd_array = Array(4, 5)

        add_array = fst_array + snd_array
        self.assertEqual(5, len(add_array))

        add_array.append(7)
        self.assertEqual(6, len(add_array))
        # Check that appending to the new array
        # haven't changed previous ones
        self.assertEqual(3, len(fst_array))
        self.assertEqual(2, len(snd_array))

    def test_add_array_to_empty(self):
        """
        Test that we can add array to an empty one.

        Changing the result array must not affect the original arrays.
        """
        fst_array = Array()
        snd_array = Array(1, 2)

        add_array = fst_array + snd_array
        self.assertEqual(2, len(add_array))

        add_array.append(3)
        self.assertEqual(3, len(add_array))
        # Check that appending to the new array
        # haven't changed previous ones
        self.assertEqual(0, len(fst_array))
        self.assertEqual(2, len(snd_array))

    def test_add_empty_array(self):
        """
        Test that we can add empty array to another array.

        Changing the result array must not affect the original arrays.
        """
        fst_array = Array(1, 2)
        snd_array = Array()

        add_array = fst_array + snd_array
        self.assertEqual(2, len(add_array))

        add_array.append(3)
        self.assertEqual(3, len(add_array))
        # Check that appending to the new array
        # haven't changed previous ones
        self.assertEqual(2, len(fst_array))
        self.assertEqual(0, len(snd_array))

    def test_find_index_if_exists(self):
        """Test that index() finds the first occurrence of the element."""
        array = Array(1, 2, 3, 2)
        found_index = array.index(2)
        expected_index = 1

        self.assertEqual(expected_index, found_index)

    def test_find_index_if_not_exists(self):
        """Test that index returns -1 if array doesn't contain the element."""
        array = Array(1, 2, 3)
        found_index = array.index(4)
        expected_index = -1

        self.assertEqual(expected_index, found_index)

    def test_get_elem_by_index(self):
        """Test that we can get an element from the array by index."""
        array = Array(1, 2, 3)
        found_elem = array[2]
        expected_elem = 3

        self.assertEqual(expected_elem, found_elem)

    def test_get_elem_by_negative_index(self):
        """Test that we can get an element from the array by negative index."""
        array = Array(1, 2, 3)
        found_elem = array[-2]
        expected_elem = 2

        self.assertEqual(expected_elem, found_elem)

    def test_get_elem_by_incorrect_index(self):
        """
        Test that there's an error when index that is out of bounds.

        Returns:
            element found by index (exists to avoid 'no-effect' warning)
        """
        with self.assertRaises(IndexError):
            return Array(1, 2, 3)[4]

    def test_array_of_arrays(self):
        """Test that we can create array of arrays."""
        array_with_arrays = Array(Array(1), Array(2, 3))

        self.assertEqual(2, len(array_with_arrays))
        self.assertEqual(0, array_with_arrays.index(Array(1)))
