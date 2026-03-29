import math
import random
import pygame
from constants import *


class Arena:
    PILLAR_RADIUS = 1.0   # world units

    def __init__(self):
        self.pillars = []   # list of (x, y) world positions
        self._place_pillars()

    # ------------------------------------------------------------------
    def _place_pillars(self):
        count = random.randint(5, 7)
        placed, tries = 0, 0
        while placed < count and tries < 300:
            tries += 1
            x = random.uniform(-21, 21)
            y = random.uniform(-21, 21)
            if math.sqrt(x * x + y * y) < 8:
                continue
            if any(math.sqrt((x - px) ** 2 + (y - py) ** 2) < 6
                   for px, py in self.pillars):
                continue
            self.pillars.append((x, y))
            placed += 1

    def random_open_position(self, min_dist_from_center=5):
        for _ in range(300):
            x = random.uniform(-22, 22)
            y = random.uniform(-22, 22)
            if math.sqrt(x * x + y * y) < min_dist_from_center:
                continue
            if any(math.sqrt((x - px) ** 2 + (y - py) ** 2) < 3
                   for px, py in self.pillars):
                continue
            return (x, y)
        return (12.0, 12.0)

    # ------------------------------------------------------------------
    def clamp_to_bounds(self, x, y, radius=0.5):
        limit = 25.0 - radius
        return max(-limit, min(limit, x)), max(-limit, min(limit, y))

    def push_out_of_pillars(self, x, y, radius=0.5):
        for px, py in self.pillars:
            dx, dy = x - px, y - py
            dist = math.sqrt(dx * dx + dy * dy)
            min_dist = self.PILLAR_RADIUS + radius
            if 0 < dist < min_dist:
                x = px + (dx / dist) * min_dist
                y = py + (dy / dist) * min_dist
        return x, y

    def bullet_hits_pillar(self, bx, by, brad=0.25):
        for px, py in self.pillars:
            if math.sqrt((bx - px) ** 2 + (by - py) ** 2) < self.PILLAR_RADIUS + brad:
                return True
        return False

    # ------------------------------------------------------------------
    def draw(self, surface):
        arena_px = ARENA_SIZE * SCALE

        # Floor
        pygame.draw.rect(surface, FLOOR_COLOR,
                         (ARENA_OX, ARENA_OY, arena_px, arena_px))

        # Subtle grid
        for i in range(0, ARENA_SIZE + 1, 5):
            x = ARENA_OX + i * SCALE
            y = ARENA_OY + i * SCALE
            gc = (48, 68, 44)
            pygame.draw.line(surface, gc, (x, ARENA_OY), (x, ARENA_OY + arena_px))
            pygame.draw.line(surface, gc, (ARENA_OX, y), (ARENA_OX + arena_px, y))

        # Border walls
        pygame.draw.rect(surface, WALL_COLOR,
                         (ARENA_OX, ARENA_OY, arena_px, arena_px), 5)

        # Pillars
        for px, py in self.pillars:
            cx, cy = w2s(px, py)
            r = int(self.PILLAR_RADIUS * SCALE)
            pygame.draw.circle(surface, PILLAR_COLOR, (cx, cy), r)
            pygame.draw.circle(surface, (100, 85, 68), (cx, cy), r, 2)
