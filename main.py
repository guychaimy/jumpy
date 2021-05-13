# Jumpy! - Platform game
# KidsCanCode - Game Development with python
# Art from Kenney.nl

import pygame as pg
import random
from settings import *
from sprites import *
from os import path


class Game:
    def __init__(self):
        # Initialize game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        #     load high score
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        #     load spritesheet image
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        # load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump33.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'powerup16.wav'))

    def new(self):
        # Initialzing the game
        self.score = 0
        # initializing all the sprites groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.mob_timer = pg.time.get_ticks()
        # Add a player
        self.player = Player(self)
        # Create platforms
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        # Spawn some clouds
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        # loading the game music
        pg.mixer.music.load(path.join(self.snd_dir, 'Happy Tune.ogg'))
        pg.mixer.music.set_volume(VOLUME)
        self.run()

    def run(self):
        # Game loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            # Keep the running at the right speed
            self.clock.tick(FPS)
            self.envents()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        # Game loop update
        # update Sprites
        self.all_sprites.update()

        # Spawn a mob
        now = pg.time.get_ticks()
        if now - self.mob_timer > MOB_FREQ + random.choice([1000, -500, 250, -1000]):
            self.mob_timer = now
            Mob(self)

        # Check if the player hits any platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x > lowest.rect.left and self.player.pos.x < lowest.rect.right:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top  # puts the player on top of the platform
                        self.player.vel.y = 0  # set the y acceleration to 0
                        self.player.jumping = False
        # Check is player hit a powerup
        hits_pow = pg.sprite.spritecollide(self.player, self.powerups, True)
        if hits_pow:
            for hit in hits_pow:
                if hit.type == 'boost':
                    self.player.vel.y = -BOOST_POWER
                    self.player.jumping = False

        # Check is player hit a mob
        hits_mob = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if hits_mob:
            for hit in hits_mob:
                self.playing = False

        # if player reaches top 1/4 of screen
        if self.player.rect.top < HEIGHT / 4:
            # spawn a cloud - 1% chance
            if random.randrange(100) < 5:
                Cloud(self)
            # move the player down
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            # move the platforms down - scrolling up
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top > HEIGHT:
                    plat.kill()
                    self.score += 10
            # move the mobs down when scrolling up
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
                if mob.rect.top > HEIGHT:
                    mob.kill()
            # move the mobs down when scrolling up
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / random.randrange(1, 4)), 1)
                if cloud.rect.top > HEIGHT:
                    cloud.kill()

        #  if we die
        if self.player.rect.top > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep average number
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width),
                     random.randrange(-70, -35))

    def envents(self):
        # Game events
        # process input (events)
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game loop - draw
        # Drae / render
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text('Your score: ' + str(self.score), 22, WHITE, WIDTH / 2, 15)

        # *After* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # Game splash/Start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.set_volume(VOLUME)
        pg.mixer.music.play(loops=-1)

        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text('Arrows to move, Space to jump', 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text('Press a key to play', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text('High score: ' + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.set_volume(VOLUME)
        pg.mixer.music.play(loops=-1)
        if self.running:
            # Game over screen
            self.screen.fill(BGCOLOR)
            self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
            self.draw_text('Score: ' + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text('Press a key to play again', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
            if self.score > self.highscore:
                self.draw_text('NEW HIGH SCORE!', 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
                self.highscore = self.score
                with open(path.join(self.dir, HS_FILE), 'w') as f:
                    f.write(str(self.score))
            else:
                self.draw_text('High score: ' + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

            pg.display.flip()
            self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if self.playing:
                            self.playing = False
                        self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


def main():
    # main function for this app
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()

    pg.quit()


if __name__ == '__main__':
    main()
