# --- Window ---
WIN_W  = 900
WIN_H  = 700
FPS    = 60

# --- Arena display ---
SCALE      = 12   # pixels per world unit
ARENA_OX   = 50   # screen-x of arena left edge
ARENA_OY   = 50   # screen-y of arena top edge
ARENA_SIZE = 50   # world units (50 x 50)

# --- Colors ---
BLACK        = (0,   0,   0)
WHITE        = (255, 255, 255)
GRAY         = (120, 120, 120)
DARK_GRAY    = (40,  40,  40)
RED          = (200, 50,  50)
GREEN        = (50,  200, 50)
LIME         = (50,  255, 50)
BLUE         = (50,  100, 255)
YELLOW       = (255, 220, 50)
ORANGE       = (255, 140, 0)
CYAN         = (50,  220, 220)
PURPLE       = (160, 50,  220)
FLOOR_COLOR  = (55,  80,  50)
WALL_COLOR   = (80,  80,  95)
PILLAR_COLOR = (130, 110, 90)


_font_cache = {}
def get_font(size):
    if size not in _font_cache:
        import pygame
        _font_cache[size] = pygame.font.SysFont(None, size)
    return _font_cache[size]


def w2s(wx, wy):
    """World (x, y) → screen pixel (px, py).
    World origin is arena centre; y-up. Screen y is inverted."""
    px = ARENA_OX + (wx + 25) * SCALE
    py = ARENA_OY + (25 - wy) * SCALE
    return (int(px), int(py))


def s2w(px, py):
    """Screen pixel → world (x, y)."""
    wx = (px - ARENA_OX) / SCALE - 25
    wy = 25 - (py - ARENA_OY) / SCALE
    return (wx, wy)
