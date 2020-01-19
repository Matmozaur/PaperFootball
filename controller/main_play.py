from controller.playing import play_valid
from model.ml_module.agent import Agent
from model.ml_module.dummy_models import RandomModel, ForwardModel
from view.board_gui import BoardGui

b = BoardGui()
b.start()

# current_player = Agent('current_player', RandomModel(), search_mode='simple')
# best_player = Agent('best_player',  ForwardModel())
#
# sc = play_valid(current_player, best_player, episodes=20)
# print(sc)
