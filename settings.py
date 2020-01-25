
class Settings:
    """Creating settings for game"""

    def __init__(self):
        """Screen settings"""
        self.game_height = 650
        self.game_width = 900
        self.bg_color = (230, 230, 230)

        #bullet settings:

        self.bullet_height = 15
        self.bullet_width = 1
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3
        # Alien settings.

        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right, -1 represents left.

        self.ship_limit = 3
        self.speed_up = 1.1
        self.score_scale= 1.5
        self.dynamic_settings()

    def dynamic_settings(self):
        self.ship_speed = 0.9
        self.bullet_speed = 2
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 50
    def increase_speed(self):
        self.ship_speed *=self.speed_up
        self.bullet_speed *= self.speed_up
        self.alien_speed_factor *= self.speed_up
        self.alien_points = int(self.alien_points * self.score_scale)





