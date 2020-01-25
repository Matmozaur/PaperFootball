# For self-playing
EPISODES =30
MEMORY_SIZE = 4000
TURNS_UNTIL_DET = 4

# For MCTS
MAX_TIME_MCTS = 5
MAX_MOVES_MCTS_ROOT = 50
MAX_MOVES_MCTS_DEEP = 25
MAX_TIME_MCTS_DEEP = 0.01
MCTS_C = 0.5

# For deep search
MAX_MOVES = 200
MAX_FINAL_MOVES = 20
MAX_CHECKED_MOVES = 100
MAX_TIME_CHECKING = 5

# For simple search
MAX_MOVES_SIMPLE = 1000
MAX_TIME_CHECKING_SIMPLE = 5

# For random search
MAX_TIME_RANDOM = 0.001

# for learning
SHUFFLE = True

BATCH_SIZE = 32
EPOCHS = 20
VALIDATION_SPLIT = 0.1
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

# For evaluate
EVAL_EPISODES = 8
SCORING_THRESHOLD = 1.1

# For logging
LOG = False
LOG_IMPORTANT = True
