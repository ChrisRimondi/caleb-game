import sys
import math
import pygame

from constants import WIN_W, WIN_H, FPS, s2w
from arena import Arena
from player import Player
from waves import WaveManager
from ui import (draw_hud, draw_start_screen, draw_wave_banner,
                draw_death_screen, draw_victory_screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Caleb's Epic Shooter")
    clock = pygame.time.Clock()

    arena        = Arena()
    player       = Player()
    wave_manager = WaveManager(player, arena)
    bullets      = []   # shared list of all active projectiles

    # States: 'start' | 'playing' | 'dead' | 'victory'
    state       = 'start'
    death_timer = 0.0

    # ------------------------------------------------------------------ helpers
    def start_game():
        nonlocal state
        bullets.clear()
        player.respawn()
        wave_manager.reset()
        wave_manager.start_wave(0)
        state = 'playing'

    # ------------------------------------------------------------------ loop
    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)
        mx, my      = pygame.mouse.get_pos()
        mouse_world = s2w(mx, my)
        mb          = pygame.mouse.get_pressed()

        # ---- events ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_RETURN:
                    if state in ('start', 'victory'):
                        start_game()
                if event.key == pygame.K_r and state == 'playing' and player.alive:
                    player.activate_powerup(arena, bullets, wave_manager.enemies)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and state == 'playing' and player.alive:
                    player.fire_shotgun(mouse_world, bullets)

        # ---- update ----
        if state == 'playing' and player.alive:
            keys = pygame.key.get_pressed()
            player.update(dt, keys, mouse_world, mb, arena)
            if mb[2]:
                player.fire_mg_held(mouse_world, bullets)

            # Update bullets
            for b in list(bullets):
                b.update(dt, arena)
            bullets[:] = [b for b in bullets if b.alive]

            # Player bullets → enemies
            for b in list(bullets):
                if b.owner != 'player':
                    continue
                for e in wave_manager.enemies:
                    if not e.alive:
                        continue
                    d = math.sqrt((b.x - e.x) ** 2 + (b.y - e.y) ** 2)
                    if d < e.RADIUS + 0.25:
                        e.take_damage(b.damage)
                        b.alive = False
                        break
            bullets[:] = [b for b in bullets if b.alive]

            # Enemy bullets → player
            for b in list(bullets):
                if b.owner != 'enemy':
                    continue
                d = math.sqrt((b.x - player.x) ** 2 + (b.y - player.y) ** 2)
                if d < player.RADIUS + 0.2:
                    player.take_damage(b.damage)
                    b.alive = False
            bullets[:] = [b for b in bullets if b.alive]

            # Update enemies
            for e in wave_manager.enemies:
                if e.alive:
                    e.update(dt, player, wave_manager.enemies, bullets)

            # Update pickups
            for p in wave_manager.pickups:
                p.update(dt)
                p.check_collect(player)
            wave_manager.pickups[:] = [p for p in wave_manager.pickups if p.alive]

            # Wave logic
            result = wave_manager.update(dt)
            if result == 'victory':
                state = 'victory'

            # Player death
            if not player.alive:
                state       = 'dead'
                death_timer = 2.0
                wave_manager._clear_enemies()
                wave_manager._clear_pickups()
                bullets.clear()

        elif state == 'playing' and wave_manager.between_waves:
            # Countdown handled inside wave_manager.update(); call it even between waves
            wave_manager.update(dt)

        elif state == 'dead':
            death_timer -= dt
            if death_timer <= 0:
                player.respawn()
                wave_manager.start_wave(wave_manager.current_wave)
                bullets.clear()
                state = 'playing'

        # ---- draw ----
        screen.fill((15, 15, 20))

        if state != 'start':
            arena.draw(screen)
            for p in wave_manager.pickups:
                p.draw(screen)
            for e in wave_manager.enemies:
                if e.alive:
                    e.draw(screen)
            for b in bullets:
                b.draw(screen)
            player.draw(screen, (mx, my))
            draw_hud(screen, player, wave_manager, WIN_W, WIN_H)

        # Overlay screens
        if state == 'start':
            draw_start_screen(screen, WIN_W, WIN_H)
        elif state == 'dead':
            draw_death_screen(screen, WIN_W, WIN_H, death_timer,
                              wave_manager.current_wave)
        elif state == 'victory':
            draw_victory_screen(screen, WIN_W, WIN_H)
        elif wave_manager.between_waves:
            draw_wave_banner(screen, WIN_W, WIN_H, wave_manager)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
