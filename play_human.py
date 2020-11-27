"""Optional file to play tetris yourself.

Run it as,
    python play_human.py --rows 20 --columns 10

"""

from gui import GUI
from tests import tests

try:
    from absl import flags
    from absl import app
except ModuleNotFoundError:
    print("Hey! absl was not found. Did you run `pip install -r requirements.txt` ?")
    exit()

flags.DEFINE_integer("rows", 20, "Number of rows in this game.")
flags.DEFINE_integer("columns", 10, "Number of columns in this game.")
flags.DEFINE_integer("test", -1, "Test sequence to load, -1 is random.")
FLAGS = flags.FLAGS


def main(argv):
    sequence = None
    rows = FLAGS.rows
    columns = FLAGS.columns

    if FLAGS.test != -1:
        rows, columns, _, sequence = tests[FLAGS.test]

    gui = GUI(rows, columns, sequence=sequence)
    gui.print_instructions()

    while gui.running:
        gui.update(human_input=True)


if __name__ == "__main__":
    app.run(main)
