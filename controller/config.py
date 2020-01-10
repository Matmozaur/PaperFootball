EPISODES = 2000
MCTS_SIMS = 50
MEMORY_SIZE = 4000000
TURNS_UNTIL_DET = 4
CPUCT = 1
EPSILON = 0.2
ALPHA = 0.8

max_moves = 200
max_final_moves = 20
max_checked_moves = 100
MAX_TIME_CHECKING = 5

BATCH_SIZE = 64
EPOCHS = 3
REG_CONST = 0.05
LEARNING_RATE = 0.05
MOMENTUM = 0.1
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
