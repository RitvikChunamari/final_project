import math
import random
import pygame

class VisualObject:
    def update(self, dt):
        pass

    def display(self, surface, *args, **kwargs):
        pass


class SongOrb(VisualObject):
    def __init__(
        self,
        row,
        center,
        min_tempo,
        max_tempo,
        min_dance,
        max_dance,
        min_pop,
        max_pop,
        screen_radius
    ):
        self.center = center

        self.track_name = row.get("track_name", "Unknown")
        self.artist_name = row.get("track_artist", "Unknown")

        self.tempo = float(row.get("tempo", 120) or 120)
        self.danceability = float(row.get("danceability", 0.5) or 0.5)
        self.energy = float(row.get("energy", 0.5) or 0.5)
        self.valence = float(row.get("valence", 0.5) or 0.5)
        self.popularity = int(row.get("track_popularity", 50) or 50)

        self.angle = random.uniform(0, 2 * math.pi)

        min_radius = 80
        max_radius = max(min_radius + 10, int(screen_radius))
        base_radius = self._map(
            self.danceability,
            min_dance, max_dance,
            min_radius, max_radius
        )

        jitter = random.uniform(-screen_radius * 0.12, screen_radius * 0.12)
        self.radius = max(20, min(screen_radius, base_radius + jitter))


        self.speed = self._map(
            self.tempo,
            min_tempo, max_tempo,
            0.05, 0.3
        )

        self.size = self._map(
            self.popularity,
            min_pop, max_pop,
            3, 12
        )

        self.color = self._valence_to_color(self.valence)

        self.glow_alpha = 60 + int(self.energy * 130)

    def update(self, dt):
        self.angle += self.speed * dt

    def display(self, surface, center, zoom):
        cx, cy = center
        x = cx + math.cos(self.angle) * self.radius * zoom
        y = cy + math.sin(self.angle) * self.radius * zoom

        display_size = max(1, int(self.size * zoom))
        glow_size = max(4, display_size * 3)
        glow = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        pygame.draw.circle(
            glow,
            (*self.color, self.glow_alpha),
            (glow_size // 2, glow_size // 2),
            int(display_size * 1.8)
        )
        surface.blit(glow, (x - glow_size // 2, y - glow_size // 2))

        pygame.draw.circle(surface, self.color, (int(x), int(y)), display_size)

        return (x, y, display_size)

    def _map(self, v, in_min, in_max, out_min, out_max):
        if in_max - in_min == 0:
            return out_min
        return out_min + (v - in_min) * (out_max - out_min) / (in_max - in_min)

    def _valence_to_color(self, valence):
        cold = (80, 120, 255)
        warm = (255, 200, 80)
        t = max(0.0, min(1.0, valence))
        return (
            int(cold[0] + t * (warm[0] - cold[0])),
            int(cold[1] + t * (warm[1] - cold[1])),
            int(cold[2] + t * (warm[2] - cold[2])),
        )

class SongGalaxy:
    def __init__(self, rows, center, screen_radius):
        self.orbs = []
        self.center = center
        self.zoom = 1.0
        self.min_zoom = 0.25
        self.max_zoom = 4.0

        if not rows:
            return

        tempos = [float(r.get("tempo", 120) or 120) for r in rows]
        dances = [float(r.get("danceability", 0.5) or 0.5) for r in rows]
        pops = [int(r.get("track_popularity", 50) or 50) for r in rows]

        min_tempo, max_tempo = min(tempos), max(tempos)
        min_dance, max_dance = min(dances), max(dances)
        min_pop, max_pop = min(pops), max(pops)

        for row in rows:
            orb = SongOrb(
                row,
                center,
                min_tempo, max_tempo,
                min_dance, max_dance,
                min_pop, max_pop,
                screen_radius
            )
            self.orbs.append(orb)

    def update(self, dt):
        for orb in self.orbs:
            orb.update(dt)

    def display(self, surface, mouse_pos=None, font=None):
        hovered = None
        hovered_screen_pos = None

        for orb in self.orbs:
            x, y, display_size = orb.display(surface, self.center, self.zoom)
            if mouse_pos is not None:
                mx, my = mouse_pos
                dist = math.hypot(mx - x, my - y)
                if dist <= display_size + 3:
                    hovered = orb
                    hovered_screen_pos = (x, y)

        if hovered and font:
            label = f"{hovered.track_name} — {hovered.artist_name} ({int(round(hovered.tempo))} BPM)"
            text_surf = font.render(label, True, (250, 250, 250))
            padding = 6
            bg = pygame.Surface((text_surf.get_width() + padding * 2, text_surf.get_height() + padding * 2), pygame.SRCALPHA)
            bg.fill((10, 10, 10, 200))
            mx, my = mouse_pos
            tx = mx + 12
            ty = my + 12
            sw, sh = surface.get_size()
            if tx + bg.get_width() > sw:
                tx = mx - 12 - bg.get_width()
            if ty + bg.get_height() > sh:
                ty = my - 12 - bg.get_height()

            surface.blit(bg, (tx, ty))
            surface.blit(text_surf, (tx + padding, ty + padding))