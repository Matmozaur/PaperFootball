EPISODES =100
MEMORY_SIZE = 4000000
TURNS_UNTIL_DET = 4
EPSILON = 0.2
ALPHA = 0.8

MAX_TIME_MCTS = 5
MAX_MOVES_MCTS_ROOT = 50
MAX_MOVES_MCTS_DEEP = 5
MAX_TIME_MCTS_DEEP = 0.01
MCTS_C = 1

MAX_MOVES = 200
MAX_FINAL_MOVES = 20
MAX_CHECKED_MOVES = 100
MAX_TIME_CHECKING = 5

MAX_MOVES_SIMPLE = 1000

BATCH_SIZE = 64
EPOCHS = 3
REG_CONST = 0.05
LEARNING_RATE = 0.05
MOMENTUM = 0.01
TRAINING_LOOPS = 1

INPUT_SHAPE = (48,8,1)

HIDDEN_CNN_LAYERS = [
    {'filters': 384, 'kernel_size': (12, 3)}
    , {'filters': 384, 'kernel_size': (8, 2)}
    # , {'filters': 384, 'kernel_size': (12, 3)}
    # , {'filters': 192, 'kernel_size': (6, 3)}
    # , {'filters': 86, 'kernel_size': (4, 4)}
    # , {'filters': 300, 'kernel_size': (12, 3)}
]

EVAL_EPISODES = 8
SCORING_THRESHOLD = 1.1

LOG = False
