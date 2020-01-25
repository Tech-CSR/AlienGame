class GameStats:
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()

    def reset_stats(self):
        self.ship_left = 3
        self.game_active = False
        self.score = 0
        self.high_score = 0
