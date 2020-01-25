import pygame
import sys

from bullet import Bullet
from alien import Alien
from time import sleep


def keydown_event(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet( ai_settings, screen, ship, bullets )


def fire_bullet(ai_settings, screen, ship, bullets):
    if len( bullets ) < ai_settings.bullet_allowed:
        new_bullet = Bullet( ai_settings, screen, ship )
        bullets.add( new_bullet )


def keyup_event(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def game_events(ai_settings, screen, stats,score, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            start_button( ai_settings, screen, stats,score, play_button, ship, aliens, bullets, mouse_x, mouse_y )
        elif event.type == pygame.KEYDOWN:
            keydown_event( event, ai_settings, screen, ship, bullets )

        elif event.type == pygame.KEYUP:
            keyup_event( event, ship )


def start_button(ai_settings, screen,stats,score, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint( mouse_x, mouse_y )
    if button_clicked and not stats.game_active:
        ai_settings.dynamic_settings()
        pygame.mouse.set_visible( False )
        stats.reset_stats()
        stats.game_active = True
        score.prep_score()
        score.prep_high_score()
        aliens.empty()
        bullets.empty()
        alien_fleet( ai_settings, screen, ship, aliens )
        ship.center_ship()


def screen_function(ai_settings, screen, stats,score, ship, alien, bullets, play_button):
    screen.fill( ai_settings.bg_color )
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    alien.draw( screen )
    score.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(ai_settings, screen,stats,score, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove( bullet )
    bullet_collisions( ai_settings, screen,stats,score, ship, aliens, bullets )


def bullet_collisions(ai_settings, screen,stats,score, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide( bullets, aliens, True, True )
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            score.prep_score()
        update_high_score(stats,score)
    if len( aliens ) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        alien_fleet( ai_settings, screen, ship, aliens )

def update_high_score(stats,score):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()

def alien_group(ai_settings, alien_width):
    screen_space = ai_settings.game_width - (2 * alien_width)
    alien_count = int( screen_space / (2 * alien_width) )
    return alien_count


def alien_countrows(ai_settings, ship_height, alien_height):
    screen_space = (ai_settings.game_height - (3 * alien_height) - ship_height)
    alien_rows = int( screen_space / (2 * alien_height) )
    return alien_rows


def creat_alien(ai_settings, screen, aliens, alien_value, alien_rows):
    alien = Alien( ai_settings, screen )
    alien_width = alien.rect.width
    alien.x = alien_width + (2 * alien_width * alien_value)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * alien_rows
    aliens.add( alien )


def alien_fleet(ai_settings, screen, ship, aliens):
    alien = Alien( ai_settings, screen )
    alien_count = alien_group( ai_settings, alien.rect.width )
    alien_rows = alien_countrows( ai_settings, ship.rect.height, alien.rect.height )
    for alien_row in range( alien_rows ):
        for alien_value in range( alien_count ):
            creat_alien( ai_settings, screen, aliens, alien_value, alien_row )


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction( ai_settings, aliens )
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen,stats,score, ship, aliens, bullets):
    if stats.ship_left >1:
        print( stats.ship_left )
        stats.ship_left -= 1
        score.prep_score()


    else:
        stats.game_active = False
        pygame.mouse.set_visible( True )
    aliens.empty()
    bullets.empty()
    alien_fleet( ai_settings, screen, ship, aliens )
    ship.center_ship()
    sleep( 0.5 )



def update_aliens(ai_settings, screen, stats,score, ship, aliens, bullets):
    check_fleet_edges( ai_settings, aliens )
    aliens.update()
    if pygame.sprite.spritecollideany( ship, aliens ):
        ship_hit( ai_settings, screen, stats,score, ship, aliens, bullets )
    bottom_aliens( ai_settings, screen, stats, score,ship, aliens, bullets )


def bottom_aliens(ai_settings, screen, stats,score, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit( ai_settings, screen,stats,score, ship, aliens, bullets )
            break
