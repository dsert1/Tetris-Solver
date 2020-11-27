"""GUI to draw tetris on the screen.
Being able to run this file is purely optional.
"""

from game import Board, tetris_shapes, colors

import random

try:
    import pygame
except ModuleNotFoundError:
    print("Hey! pygame was not found. Did you run `pip install -r requirements.txt` ?")
    exit()


class GUI(object):
    def __init__(self, rows, columns, fps=60, cell_size=20, sequence=None):
        self.board = Board(rows, columns)

        self.running = True
        self.fps = fps
        self.cell_size = 20
        self.sequence = sequence
        self.current_index = 0

        pygame.display.set_caption("6.006 Tetris")
        self.screen = pygame.display.set_mode((columns * cell_size, rows * cell_size))
        self.clock = pygame.time.Clock()

        self.next_piece()

    def next_piece(self):
        if self.sequence is None:
            self.shape_name = random.choice([x for x in tetris_shapes.keys()])
        else:
            if self.current_index >= len(self.sequence):
                return
            self.shape_name = self.sequence[self.current_index]
            self.current_index += 1

        self.rotation = 0
        self.x = 0

    def print_instructions(self):
        print(
            """
            GUI Intructions:
                Left/Right Arrow Key: Move current piece left or right.
                Up Arrow Key:         Rotate current piece clockwise.
                Space Key:            Lock current piece and get next piece.
                Q:                    Quit.
            """
        )

    def play_move(self, x, rotation):
        new_board = self.board.copy()
        new_board.move(self.shape_name, x, rotation)
        self.board = new_board
        self.next_piece()

    def process_human_input(self):
        pass

    def draw_board(self):
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            pygame.Rect(
                0,
                0,
                self.board.columns * self.cell_size,
                self.board.rows * self.cell_size,
            ),
            width=1,
        )

    def draw_matrix(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x + x) * self.cell_size,
                            (off_y + y) * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                        0,
                    )

    def check_valid_move(self, x, rotation):
        new_board = self.board.copy()
        try:
            new_board.move(self.shape_name, x, rotation)
        except ValueError:
            return False

        return True

    def update(self, human_input=True):
        self.screen.fill((0, 0, 0))

        new_board = self.board.copy()

        if human_input:
            try:
                new_board.move(self.shape_name, self.x, self.rotation)
            except:
                pass

        self.draw_matrix(new_board._board, (0, 0))
        self.draw_board()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.running = False

            if event.type == pygame.KEYDOWN and human_input:
                if event.key == pygame.K_LEFT:
                    self.x -= 1
                elif event.key == pygame.K_RIGHT:
                    self.x += 1
                elif event.key == pygame.K_UP:
                    self.rotation += 1
                    self.rotation %= 4
                elif event.key == pygame.K_SPACE:
                    self.board = new_board
                    self.next_piece()

                if not self.check_valid_move(self.x, self.rotation):
                    print(
                        "Invalid Move, Current x = {} and rotation = {}".format(
                            self.x, self.rotation
                        )
                    )

        self.clock.tick(self.fps)
