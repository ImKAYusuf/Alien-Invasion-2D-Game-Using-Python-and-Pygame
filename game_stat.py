class Game_stat:
    def __init__(self,ai_game):
        self.settings=ai_game.settings
        self.high_score=0
        self.reset_stat()
        self.game_active=False
        
            
    def reset_stat(self):
        self.ship_left=self.settings.ship_limit
        self.score=0
        self.level=1
