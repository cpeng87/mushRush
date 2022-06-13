class Player:
    def __init__(self, shrooms=0, lives=5, current_level=1, drags=0):
        self.shrooms = shrooms
        self.lives = lives
        self.current_level = current_level
        self.drags = drags
        self.mapDrags = [[]]

    def buy(self, shroomCost):
        if self.drags >= 25:
            print("too many dragons on the field. they like their personal space")
        else:
            shrooms = shrooms - shroomCost

    def sell(dragCost):
        shrooms = shrooms + (dragCost / 2)

    def loseLife():
        lives = lives - 1



