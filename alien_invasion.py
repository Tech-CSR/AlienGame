import pygame

from button import Button
from game_stats import GameStats
from score_board import ScoreBoard
from settings import Settings
from ship import Ship
import game_functions as function
from pygame.sprite import Group
from alien import Alien


def run_game():
    """ initialising the game and creating the screen"""
    pygame.init()

    ai_settings = Settings()
    bullets= Group()
    aliens = Group()
    stats = GameStats(ai_settings)


    screen = pygame.display.set_mode( (ai_settings.game_width, ai_settings.game_height) )
    ship: Ship = Ship( ai_settings, screen )
    alien = Alien( ai_settings, screen )
    play_button = Button( ai_settings, screen, "Play" )
    pygame.display.set_caption( "____Alien Invasion____" )
    function.alien_fleet(ai_settings,screen,ship,aliens)
    score = ScoreBoard(ai_settings,screen,stats)

    """main loop"""
    while True:

        function.game_events( ai_settings,screen,stats,score,play_button,ship,aliens,bullets )

        if stats.game_active:

            ship.update()
            function.update_aliens(ai_settings,screen,stats,score,ship,aliens, bullets)
            function.update_bullets(ai_settings, screen,stats,score,ship,aliens,bullets)
        function.screen_function( ai_settings, screen, stats,score, ship, aliens, bullets, play_button )





run_game()
