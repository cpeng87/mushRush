from enum import Enum

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL = 2
    PAUSE = 3
    INSTRUCTION = 4
    LEVEL = 5
    GAME_OVER = 6