import math
import random
import pygame
from constants import *  # includes get_font


class PlayerBullet:
    def __init__(self, x, y, vx, vy, damage):
        self.x, self.y   = x, y
        self.vx, self.vy = vx, vy
        self.damage      = damage
        self.owner       = 'player'
        self.alive       = True

    def update(self, dt, arena):
        self.x += self.vx * dt
        self.y += self.vy * dt
        if abs(self.x) > 25.5 or abs(self.y) > 25.5:
            self.alive = False
        elif arena.bullet_hits_pillar(self.x, self.y):
            self.alive = False

    def draw(self, surface):
        px, py = w2s(self.x, self.y)
        pygame.draw.circle(surface, YELLOW, (px, py), 3)


class Player:
    RADIUS   = 0.5
    SPEED    = 8.0
    JET_BONUS = 7.0   # extra speed during jetpack

    def __init__(self):
        self.x = self.y = 0.0
        self.health     = 20
        self.max_health = 20
        self.alive      = True

        # Shotgun
        self.sg_ammo    = 25
        self.sg_max     = 25
        self.sg_cooling = False
        self.sg_timer   = 0.0

        # Machine gun
        self.mg_ammo    = 85
        self.mg_max     = 85
        self.mg_cooling = False
        self.mg_timer   = 0.0
        self.mg_accum   = 0.0   # accumulated time for next MG shot
        self.MG_RATE    = 0.1   # seconds between shots

        # Power-up queue
        self.powerup_queue  = []
        self.jetpack_active = False
        self.jetpack_timer  = 0.0

        # Sabre
        self.has_sabre   = False
        self.sabre_cd    = 0.0
        self.sabre_swing = 0.0   # visual flash timer

        # Visual
        self.hit_flash = 0.0

    # ------------------------------------------------------------------
    def update(self, dt, keys, mouse_world, mouse_buttons, arena):
        if not self.alive:
            return

        # --- Movement ---
        dx = dy = 0.0
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy += 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy -= 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += 1
        if dx or dy:
            length = math.sqrt(dx * dx + dy * dy)
            dx /= length
            dy /= length

        spd = self.SPEED + (self.JET_BONUS if self.jetpack_active else 0.0)
        nx, ny = self.x + dx * spd * dt, self.y + dy * spd * dt
        nx, ny = arena.clamp_to_bounds(nx, ny, self.RADIUS)
        if not self.jetpack_active:
            nx, ny = arena.push_out_of_pillars(nx, ny, self.RADIUS)
        self.x, self.y = nx, ny

        # --- Cooldowns ---
        if self.sg_cooling:
            self.sg_timer -= dt
            if self.sg_timer <= 0:
                self.sg_cooling = False
                self.sg_ammo = self.sg_max

        if self.mg_cooling:
            self.mg_timer -= dt
            if self.mg_timer <= 0:
                self.mg_cooling = False
                self.mg_ammo = self.mg_max

        # --- MG accumulate (right mouse held) ---
        if mouse_buttons[2] and not self.mg_cooling and self.mg_ammo > 0:
            self.mg_accum += dt
        else:
            self.mg_accum = 0.0

        # --- Sabre cooldown ---
        if self.sabre_cd > 0:
            self.sabre_cd -= dt
        if self.sabre_swing > 0:
            self.sabre_swing -= dt

        # --- Jetpack ---
        if self.jetpack_active:
            self.jetpack_timer -= dt
            if self.jetpack_timer <= 0:
                self.jetpack_active = False

        if self.hit_flash > 0:
            self.hit_flash -= dt

    # ------------------------------------------------------------------
    def fire_shotgun(self, mouse_world, bullets):
        if self.sg_cooling or self.sg_ammo <= 0 or not self.alive:
            return
        mx, my = mouse_world
        angle = math.atan2(my - self.y, mx - self.x)
        spd = 26.0
        bullets.append(PlayerBullet(self.x, self.y,
                                    math.cos(angle) * spd,
                                    math.sin(angle) * spd, damage=2))
        self.sg_ammo -= 1
        if self.sg_ammo <= 0:
            self.sg_cooling = True
            self.sg_timer   = 10.0

    def fire_mg_held(self, mouse_world, bullets):
        """Call every frame while right mouse is held; fires based on accumulated time."""
        if self.mg_cooling or self.mg_ammo <= 0 or not self.alive:
            return
        while self.mg_accum >= self.MG_RATE:
            self.mg_accum -= self.MG_RATE
            mx, my = mouse_world
            angle  = math.atan2(my - self.y, mx - self.x)
            angle += random.uniform(-0.06, 0.06)   # slight spread
            spd    = 26.0
            bullets.append(PlayerBullet(self.x, self.y,
                                        math.cos(angle) * spd,
                                        math.sin(angle) * spd, damage=1))
            self.mg_ammo -= 1
            if self.mg_ammo <= 0:
                self.mg_cooling = True
                self.mg_timer   = 10.0
                self.mg_accum   = 0.0
                break

    # ------------------------------------------------------------------
    def take_damage(self, amount):
        if not self.alive:
            return
        self.health = max(0, self.health - amount)
        self.hit_flash = 0.3
        if self.health <= 0:
            self.alive = False

    def respawn(self):
        self.x = self.y = 0.0
        self.health     = self.max_health
        self.alive      = True
        self.sg_ammo    = self.sg_max
        self.sg_cooling = False
        self.mg_ammo    = self.mg_max
        self.mg_cooling = False
        self.mg_accum   = 0.0
        self.powerup_queue.clear()
        self.jetpack_active = False
        self.sabre_cd    = 0.0
        self.sabre_swing = 0.0
        self.hit_flash   = 0.0

    # ------------------------------------------------------------------
    def add_powerup(self, ptype):
        self.powerup_queue.append(ptype)

    def activate_powerup(self, arena, bullets, enemies):
        if not self.powerup_queue or not self.alive:
            return
        ptype = self.powerup_queue.pop(0)
        if ptype == 'jetpack':
            self.jetpack_active = True
            self.jetpack_timer  = 5.0
        elif ptype == 'bomb':
            self._activate_bomb(enemies)

    def swing_sabre(self, mouse_world, enemies):
        if not self.has_sabre or self.sabre_cd > 0 or not self.alive:
            return
        mx, my = mouse_world
        aim_angle = math.atan2(my - self.y, mx - self.x)
        for e in enemies:
            if not e.alive:
                continue
            d = math.sqrt((self.x - e.x) ** 2 + (self.y - e.y) ** 2)
            if d > 2.0:
                continue
            ea   = math.atan2(e.y - self.y, e.x - self.x)
            diff = abs(math.atan2(math.sin(ea - aim_angle), math.cos(ea - aim_angle)))
            if diff <= math.pi / 2:   # 180-degree arc centred on mouse
                e.take_damage(3)
        self.sabre_cd    = 0.5
        self.sabre_swing = 0.15

    def _activate_bomb(self, enemies):
        for e in list(enemies):
            if e.alive:
                d = math.sqrt((self.x - e.x) ** 2 + (self.y - e.y) ** 2)
                if d <= 5.0:
                    e.take_damage(999)
        self.take_damage(5)   # bomb always hurts the player too
        self.hit_flash = 0.5

    # ------------------------------------------------------------------
    def draw(self, surface, mouse_screen):
        px, py = w2s(self.x, self.y)
        r = int(SCALE * self.RADIUS) + 2

        # Body colour
        if self.hit_flash > 0:
            col = (255, 80, 80)
        elif self.jetpack_active:
            col = (80, 200, 255)
        else:
            col = BLUE

        pygame.draw.circle(surface, col, (px, py), r)
        pygame.draw.circle(surface, WHITE, (px, py), r, 2)

        # Aim line toward mouse
        mx, my = mouse_screen
        angle = math.atan2(-(my - py), mx - px)
        ex = px + int(math.cos(angle) * (r + 10))
        ey = py + int(math.sin(angle) * -(r + 10))  # screen y flipped already
        # Recalculate using screen coords directly
        length = math.sqrt((mx - px) ** 2 + (my - py) ** 2)
        if length > 0:
            ex = px + int((mx - px) / length * (r + 10))
            ey = py + int((my - py) / length * (r + 10))
        pygame.draw.line(surface, WHITE, (px, py), (ex, ey), 2)

        # Jetpack glow
        if self.jetpack_active:
            pygame.draw.circle(surface, (80, 200, 255, 80), (px, py), r + 4, 2)

        # Sabre slash arc
        if self.sabre_swing > 0 and self.has_sabre:
            mx, my = mouse_screen
            length  = max(1, math.sqrt((mx - px) ** 2 + (my - py) ** 2))
            dx, dy  = (mx - px) / length, (my - py) / length
            slash_r = int(2.0 * SCALE)
            ex      = px + int(dx * slash_r)
            ey      = py + int(dy * slash_r)
            pygame.draw.line(surface, (255, 230, 80), (px, py), (ex, ey), 4)

        # Name tag
        font = get_font(16)
        tag  = font.render('Player', True, WHITE)
        surface.blit(tag, (px - tag.get_width() // 2, py - r - 18))
