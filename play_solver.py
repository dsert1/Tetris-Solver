"""Optional file to watch your solver play tetris.

Run it as,
    python play_solver.py --test 0

"""


from gui import GUI
from solver import solver
from tests import tests

try:
    from absl import flags
    from absl import app
except ModuleNotFoundError:
    print("Hey! absl was not found. Did you run `pip install -r requirements.txt` ?")
    exit()

flags.DEFINE_integer("test", 0, "Test index to play.")
FLAGS = flags.FLAGS


def main(argv):
    print()

    if FLAGS.test >= len(tests):
        print("Test with index %i does not exist." % FLAGS.test)
        return

    rows, columns, _, sequence = tests[FLAGS.test]
    game = GUI(rows, columns, sequence=sequence)

    print("Running your solver ...")
    solution = solver(rows, columns, sequence)

    if not solution:
        print("Your solver says this is impossible.")
        return

    print(
        """
        Solver found a solution.
        Your solver is playing!
        """
    )

    for (x, rotation), shape in zip(solution, sequence):
        print("Playing move, x={}, rotation={}, shape={}".format(x, rotation, shape))
        game.update(human_input=False)
        game.play_move(x, rotation)
        game.clock.tick(3)

    print("Done! Press Q to quit.")

    while game.running:
        game.update(human_input=False)


if __name__ == "__main__":
    app.run(main)
