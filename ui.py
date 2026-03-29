import pygame
from constants import *

_fc = {}
def _f(size):
    if size not in _fc:
        _fc[size] = pygame.font.SysFont(None, size)
    return _fc[size]


def draw_hud(screen, player, wave_manager, win_w, win_h):
    px = ARENA_OX + ARENA_SIZE * SCALE + 14
    pw = win_w - px - 6

    # Panel background
    pygame.draw.rect(screen, (22, 22, 32), (px - 4, 0, pw + 10, win_h))
    pygame.draw.line(screen, GRAY, (px - 4, 0), (px - 4, win_h), 1)

    y = 18

    # Wave
    wt = _f(30).render(f'WAVE  {wave_manager.current_wave + 1} / 10', True, YELLOW)
    screen.blit(wt, (px, y)); y += 36

    # Enemies left
    alive = sum(1 for e in wave_manager.enemies if e.alive)
    et = _f(22).render(f'Enemies left: {alive}', True, ORANGE)
    screen.blit(et, (px, y)); y += 30

    _hline(screen, px, pw, y); y += 10

    # Health
    screen.blit(_f(22).render('HEALTH', True, WHITE), (px, y)); y += 22
    _bar(screen, px, y, pw, 18, player.health / player.max_health,
         (200, 50, 50), GREEN, ORANGE)
    ht = _f(18).render(f'{player.health} / {player.max_health}', True, WHITE)
    screen.blit(ht, (px + pw // 2 - ht.get_width() // 2, y + 1)); y += 28

    _hline(screen, px, pw, y); y += 10

    # Shotgun
    screen.blit(_f(20).render('SHOTGUN  (left click)', True, WHITE), (px, y)); y += 22
    if player.sg_cooling:
        st = _f(18).render(f'  reloading...  {player.sg_timer:.0f}s', True, ORANGE)
    else:
        st = _f(18).render(f'  ammo: {player.sg_ammo} / {player.sg_max}', True, LIME)
    screen.blit(st, (px, y)); y += 26

    # Machine gun
    screen.blit(_f(20).render('MACHINE GUN  (hold right)', True, WHITE), (px, y)); y += 22
    if player.mg_cooling:
        mt = _f(18).render(f'  reloading...  {player.mg_timer:.0f}s', True, ORANGE)
    else:
        mt = _f(18).render(f'  ammo: {player.mg_ammo} / {player.mg_max}', True, LIME)
    screen.blit(mt, (px, y)); y += 30

    _hline(screen, px, pw, y); y += 10

    # Power-ups
    screen.blit(_f(20).render('POWER-UPS  [R to use]', True, CYAN), (px, y)); y += 22
    if player.jetpack_active:
        jt = _f(18).render(f'  JETPACK: {player.jetpack_timer:.1f}s', True, (100, 220, 255))
        screen.blit(jt, (px, y)); y += 20
    if player.powerup_queue:
        for i, pt in enumerate(player.powerup_queue):
            col = CYAN if pt == 'jetpack' else ORANGE
            screen.blit(_f(18).render(f'  {i + 1}. {pt.upper()}', True, col), (px, y))
            y += 20
    else:
        screen.blit(_f(18).render('  none', True, GRAY), (px, y)); y += 20

    # Legend at bottom
    y = win_h - 145
    _hline(screen, px, pw, y); y += 8
    legend = [
        ('Cyan circle',   'Jetpack power-up'),
        ('Orange circle', 'Bomb power-up'),
        ('Green circle',  '+5 HP pickup'),
        ('Green enemy',   'Range (2 HP)'),
        ('Red enemy',     'Melee (3 HP)'),
        ('Purple enemy',  'Caster (4 HP)'),
    ]
    for key, desc in legend:
        line = _f(16).render(f'{key}: {desc}', True, (150, 150, 160))
        screen.blit(line, (px, y)); y += 18


# ---------------------------------------------------------------------------
# Screens
# ---------------------------------------------------------------------------
def draw_start_screen(screen, win_w, win_h):
    _overlay(screen, win_w, win_h, (0, 0, 0, 200))
    cx = win_w // 2

    title = _f(74).render("CALEB'S EPIC SHOOTER", True, YELLOW)
    screen.blit(title, (cx - title.get_width() // 2, 80))

    sub = _f(34).render('Top-Down Wave Survival  —  10 Waves', True, (190, 190, 190))
    screen.blit(sub, (cx - sub.get_width() // 2, 158))

    rows = [
        ('WASD',          'Move'),
        ('Mouse',         'Aim'),
        ('Left Click',    'Shotgun  —  2 dmg, 25 shots, 10 s reload'),
        ('Hold R-Click',  'Machine Gun  —  1 dmg, 85 shots, 10 s reload'),
        ('R',             'Use next power-up from queue'),
        ('Walk over',     'Cyan = Jetpack  |  Orange = Bomb  |  Green = +5 HP'),
        ('Bomb warning',  'Explodes 5-unit radius — hurts YOU too!'),
        ('Death',         'Restart current wave, lose all power-ups'),
    ]
    y = 210
    for key, desc in rows:
        kt = _f(24).render(f'{key}:', True, CYAN)
        dt = _f(24).render(desc, True, WHITE)
        screen.blit(kt, (cx - 310, y))
        screen.blit(dt, (cx - 190, y))
        y += 32

    prompt = _f(38).render('Press  ENTER  to Start', True, LIME)
    screen.blit(prompt, (cx - prompt.get_width() // 2, y + 16))


def draw_wave_banner(screen, win_w, win_h, wave_manager):
    next_w = wave_manager.current_wave + 2   # 1-indexed next wave
    timer  = wave_manager.between_timer
    line1  = f'Wave {wave_manager.current_wave + 1} Cleared!'
    line2  = f'Wave {next_w} starts in  {timer:.0f}s...'
    _banner(screen, win_w, win_h, [line1, line2], YELLOW)


def draw_death_screen(screen, win_w, win_h, timer, current_wave):
    _overlay(screen, win_w, win_h, (140, 0, 0, 110))
    cx = win_w // 2
    t1 = _f(88).render('YOU DIED!', True, (255, 70, 70))
    screen.blit(t1, (cx - t1.get_width() // 2, win_h // 2 - 80))
    t2 = _f(34).render(f'Respawning in  {max(0, timer):.0f}s  —  wave {current_wave + 1} restarts', True, WHITE)
    screen.blit(t2, (cx - t2.get_width() // 2, win_h // 2 + 10))
    t3 = _f(28).render('All power-ups lost', True, ORANGE)
    screen.blit(t3, (cx - t3.get_width() // 2, win_h // 2 + 54))


def draw_victory_screen(screen, win_w, win_h):
    _overlay(screen, win_w, win_h, (0, 0, 0, 190))
    cx = win_w // 2
    t1 = _f(110).render('VICTORY!', True, YELLOW)
    screen.blit(t1, (cx - t1.get_width() // 2, win_h // 2 - 130))
    t2 = _f(42).render('You survived all 10 waves!', True, WHITE)
    screen.blit(t2, (cx - t2.get_width() // 2, win_h // 2 - 10))
    t3 = _f(42).render('Caleb WINS!', True, LIME)
    screen.blit(t3, (cx - t3.get_width() // 2, win_h // 2 + 46))
    t4 = _f(30).render('Press  ENTER  to play again', True, CYAN)
    screen.blit(t4, (cx - t4.get_width() // 2, win_h // 2 + 108))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _hline(surface, x, w, y):
    pygame.draw.line(surface, GRAY, (x, y), (x + w, y), 1)


def _bar(surface, x, y, w, h, ratio, bg, fg_hi, fg_lo):
    pygame.draw.rect(surface, bg, (x, y, w, h))
    col = fg_hi if ratio > 0.5 else (fg_lo if ratio > 0.25 else (200, 50, 50))
    pygame.draw.rect(surface, col, (x, y, int(w * max(0, ratio)), h))
    pygame.draw.rect(surface, WHITE, (x, y, w, h), 1)


def _overlay(screen, w, h, rgba):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    s.fill(rgba)
    screen.blit(s, (0, 0))


def _banner(screen, win_w, win_h, lines, col):
    s = pygame.Surface((win_w, 100), pygame.SRCALPHA)
    s.fill((0, 0, 0, 170))
    screen.blit(s, (0, win_h // 2 - 50))
    y = win_h // 2 - 40
    for line in lines:
        t = _f(44).render(line, True, col)
        screen.blit(t, (win_w // 2 - t.get_width() // 2, y))
        y += 48
