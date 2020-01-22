from controller.playing import play_valid
from model.ml_module.agent import Agent
from model.ml_module.dummy_models import RandomModel, ForwardModel
from view.board_gui import BoardGui, GameWindow

# b = BoardGui()
# b.start()
# app = GameWindow()
# app.mainloop()
current_player = Agent('current_player', ForwardModel(), search_mode='simple',eval_mode='mcts_simple')
best_player = Agent('best_player',  RandomModel(), search_mode='simple')
#
sc = play_valid(current_player, best_player, episodes=10)
print(sc)
