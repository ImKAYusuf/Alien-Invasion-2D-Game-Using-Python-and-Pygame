import sys
import pygame as py
from time import sleep

from game_stat import Game_stat
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scorecard

class AlienInvasion:
    def __init__(self):
        py.init()
        self.settings = Settings()

        self.screen = py.display.set_mode(
            (self.settings.width, self.settings.length)
        )
        py.display.set_caption("Alien Invasion made by YUSUF")

        self.ship = Ship(self)
        self.bullets = py.sprite.Group()
        self.aliens = py.sprite.Group()
        self.stats = Game_stat(self)
        self.sb = Scorecard(self)

        self.play_button = Button(self, "Play")
        self.create_fleet()

    def run_game(self):
        while True:
            self.check_events()

            if self.stats.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()

            self.update_screen()

    def check_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            elif event.type == py.KEYDOWN:
                self.keydown(event)
            elif event.type == py.KEYUP:
                self.keyup(event)
            elif event.type == py.MOUSEBUTTONDOWN:
                mouse_pos = py.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def keydown(self, event):
        if event.key == py.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == py.K_LEFT:
            self.ship.moving_left = True
        elif event.key == py.K_UP:
            self.ship.moving_top = True
        elif event.key == py.K_DOWN:
            self.ship.moving_bottom = True
        elif event.key == py.K_q:
            py.quit()
            sys.exit()
        elif event.key == py.K_SPACE:
            self.fire_bullet()

    def keyup(self, event):
        if event.key == py.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == py.K_LEFT:
            self.ship.moving_left = False
        elif event.key == py.K_UP:
            self.ship.moving_top = False
        elif event.key == py.K_DOWN:
            self.ship.moving_bottom = False

    def check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stat()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()

            self.aliens.empty()
            self.bullets.empty()
            self.create_fleet()
            self.ship.center_ship()

            py.mouse.set_visible(False)

    def fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collision()

    def check_bullet_alien_collision(self):
        collisions = py.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens_hit in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens_hit)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.settings.increse_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height

        available_space_x = self.settings.width - (2 * alien_width)
        number_alien_x = min(10, available_space_x // (2 * alien_width))

        available_space_y = self.settings.length - ((5 * alien_height) + ship_height)
        number_alien_y = min(4, available_space_y // (2 * alien_height))

        for row_number in range(number_alien_y):
            for alien_number in range(number_alien_x):
                self.create_alien(alien_number, row_number)

    def create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = 2 * alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def update_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()

        if py.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()

        self.check_alien_bottom()

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def ship_hit(self):
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.sb.prep_ship()
            self.bullets.empty()
            self.aliens.empty()
            self.create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
            py.mouse.set_visible(True)

    def check_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        py.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()