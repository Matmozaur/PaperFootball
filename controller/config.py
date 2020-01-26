# For self-playing
EPISODES =3
MEMORY_SIZE = 30000
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
PARAMS_DNN = {
                'activation_hidden': 'sigmoid', 'activation': 'sigmoid', 'optimizer': 'adam',
                'architectures': [[100, 0.0], [400, 0.000001], ['dropout', 0.1], [200, 0.000001], ['dropout', 0.2],
                                  [200, 0.000001],
                                  ['dropout', 0.3], [100, 0.0], [20, 0.0]]}
BATCH_SIZE = 32
EPOCHS = 1
TRAINING_LOOPS = 1
VALIDATION_SPLIT = 0.1
REG_CONST = 0.05
LEARNING_RATE = 0.05
MOMENTUM = 0.01
INPUT_SHAPE = (48,8,1)


# For evaluate
EVAL_EPISODES = 4
SCORING_THRESHOLD = 1.1

# For logging
LOG = False
LOG_IMPORTANT = True
