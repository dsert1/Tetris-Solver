"""This is the main file you'll edit.
"""

try:
    from game import board_from_heights
except ModuleNotFoundError:
    pass

# 4 possible rotations for any piece.
ROTATIONS = [0, 1, 2, 3]


def make_move(rows, columns, heights, shape_name, x, rotation):
    """Takes a the tetris board as column heights and applies a particular move.

    Args:
        rows (int): Number of rows in this tetris game.
        columns (int): Number of columns in this tetris game.
        heights (Tuple[int]): List of column heights in the current board.
        shape_name (str): Name of the piece shape (like "L" or "O" etc.)
        x (int): Which column to drop the piece in.
        rotation (int): Rotation of the piece, either 0, 1, 2, or 3.

    Returns:
        Modified heights _after_ the piece at `x` and `rotation` have been dropped.
        `None` if move is invalid.
    """

    board = board_from_heights(heights, rows, columns)

    try:
        board.move(shape_name, x, rotation)
    except ValueError:
        return None

    return tuple(board.skyline())


###
# DO NOT MODIFY ABOVE THIS FILE.
###


def solver(rows, columns, shape_sequence, place=0, memo={}):
    """Solve a given tetris game.

    Args:
        rows (int): Number of rows in this game.
        columns (int): Number of columns in this game.
        shape_sequence (List[str]): List of shape names to come (This list is of size n).
                                    e.g. `shape_sequence = ["L", "O", "I", "L"]`
    
    Returns:
        A list of `(x, rotation)` pairs corresponding to the ideal moves to be made to survive.
        `None` if there is no possible way to survive.
    """



    parent = {}
    memo = {}
    heights = tuple([0 for _ in range(columns)])


    # O(nc(r+1)**c)
    def DP(ix, heights):
        '''DP that returns True or False'''

        # ran out of tiles -> shape_seq length
        if ix >= len(shape_sequence):
            if any([i > rows for i in heights]):
                return False
            return True

        if (ix, heights) in memo: # we've seen this exact config b4
            return memo[(ix, heights)]





        # current shape
        shape = shape_sequence[ix]
        for c in range(columns):
            for rot in ROTATIONS:
                new_heights = make_move(rows, columns, heights, shape, c, rot)

                if not new_heights: # don't bother computing further. Seq is invalid
                    continue

                try: # have we seen this config before?
                    result_from_b4 = memo[(ix, new_heights)] # yes we have
                    if result_from_b4:
                        parent[(ix, heights)] = (c, rot)
                        memo[(ix, heights)] = True
                        return True

                except KeyError: # no we haven't
                    indicator = DP(ix+1, new_heights)
                    if indicator:
                        memo[(ix, heights)] = True
                        parent[(ix, heights)] = (c, rot)
                        return True

        memo[(ix, heights)] = False
        return False

    start = DP(0, heights)
    if not start:
        return None


    out = []
    now = heights
    for p in range(len(shape_sequence)):
        parent_r, parent_c = parent[(p, now)]
        out.append((parent_r, parent_c))
        now = make_move(rows, columns, now, shape_sequence[p], parent_r, parent_c)
    return out












