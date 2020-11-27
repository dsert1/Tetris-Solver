import unittest
from solver_2 import solver

from game import Board


def check(test, solution):
    rows, columns, possible, shapes = test

    # If not possible, check if they return `None`.
    if not possible:
        if solution is None:
            return True
        return False

    if len(shapes) != len(solution):
        return False

    board = Board(rows, columns)

    for shape_name, (x, rotation) in zip(shapes, solution):
        try:
            board.move(shape_name, x, rotation)
        except ValueError:
            return False

    return True


tests = [
    (5, 5, True, ["T", "S", "I", "T", "LFlip", "I"]),
    (7, 5, True, ["S", "I", "LFlip", "L", "O", "T", "S", "O"]),
    (7, 5, True, ["S", "I", "LFlip", "T", "L", "I", "T", "T"]),
    (10, 4, True, ["S", "I", "SFlip", "O", "SFlip", "LFlip", "I", "I", "T"]),
    (
        10,
        4,
        False,
        ["S", "LFlip", "LFlip", "L", "LFlip", "SFlip", "O", "O", "LFlip", "SFlip"],
    ),
]


class TestCases(unittest.TestCase):
    def test_01(self):
        test = tests[0]
        rows, columns, _, shapes = test
        solution = solver(rows, columns, shapes)
        print('sol: ', solution)
        self.assertTrue(check(test, solution))

    def test_02(self):
        test = tests[1]
        rows, columns, _, shapes = test
        solution = solver(rows, columns, shapes)
        self.assertTrue(check(test, solution))

    def test_03(self):
        test = tests[2]
        rows, columns, _, shapes = test
        solution = solver(rows, columns, shapes)
        self.assertTrue(check(test, solution))

    def test_04(self):
        test = tests[3]
        rows, columns, _, shapes = test
        solution = solver(rows, columns, shapes)
        self.assertTrue(check(test, solution))

    def test_05(self):
        test = tests[4]
        rows, columns, _, shapes = test
        solution = solver(rows, columns, shapes)
        self.assertTrue(check(test, solution))


if __name__ == "__main__":
    res = unittest.main(verbosity=3, exit=False)
