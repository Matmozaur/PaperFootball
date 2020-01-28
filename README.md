# 
Project name: Paper football
Authors: Maciej Dobrzański, Izabela Dąbrowska


Overview

The result of our project  is a program to play the game called paper football with choosen computer opponent or to simulate a match between two choosen bots. The rules are described here: https://en.wikipedia.org/wiki/Paper_soccer. Additionally we included framework allowing us to create and train our own bots based i.a on methods of artificial intelligence. The result are also a few bots which we have already trained.

Project structure

We divided our project into model, view and controller packages. Below, there is a more detailed description of files included in the project.

File path	Description

view\* 	Folder with files for GUI 
model\game.py	Interface for files: model\gameState.py and model\gameStateUtils;
Includes functions to get allowable moves (on 3 modes: simple, deepcheck and random), to make moves etc.
model\ml-module\agent.py	Class standing for computer player. There are 3 modes of getting a move and2 modesof choosing one (described below).
model\ml_module\*	Implementation of predictors, MCTS, memory, deterministic models
controller\playing.py 	Set of functions for playing training matches (with saving to memory and retraining) and validation ones
controller\main_training.py	File with training loop for models
controller\main_play.py 	Start of a game
controller\config 	Includes configuration options for the first game (depth of search, max times, learning parameters


There are 3 modes of getting allowable moves avaliable for user and 2 modes of choosing one of them.
Getting allowable moves
‘simple’ - all allowable moves that are not losing. If there is the winning move, it should be returned as the only one.
‘deepcheck’ - all allowable moves that are not losing and the moves and the moves after which the opponent has not winning move. 
‘random’

Choosing a move

‘model’ - we choose move with the best result returned by the model (‘probability of win’)
‘mcts.simple’ - simple MCTS
‘mcts.boosted’ - MCTS, where the initial weights are initialized from the model


Models

We trained two model, one dedicated for simple model evaluation mode of the agent, and secound for mcts boosted approach.

