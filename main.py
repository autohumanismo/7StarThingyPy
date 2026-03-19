import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1250, 1000
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
MAX_RADIUS = 380
CIRCLE_RADIUS = 12
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (80, 80, 80)
TOOLTIP_BG = (40, 40, 50)
TOOLTIP_TEXT = (240, 240, 200)

# Themes
THEMES = {
    'Clásico': {'a': (220,50,50), 'g':(200,50,50), 'b':(150,80,200), 'c':(255,140,60),
                'd':(255,220,60), 'e':(60,200,220), 'f':(80,200,100), 'star':(70,100,150)},
    'Océano': {'a':(200,30,70), 'g':(180,40,80), 'b':(120,80,180), 'c':(230,120,50),
               'd':(100,180,200), 'e':(50,150,200), 'f':(60,180,140), 'star':(40,80,120)},
    'Bosque': {'a':(180,50,50), 'g':(160,40,50), 'b':(140,100,60), 'c':(200,140,70),
               'd':(160,160,70), 'e':(100,150,100), 'f':(60,140,60), 'star':(50,80,50)},
    'Fuego': {'a':(220,40,40), 'g':(200,50,60), 'b':(180,60,120), 'c':(255,120,40),
              'd':(255,200,40), 'e':(100,180,180), 'f':(100,200,120), 'star':(100,60,60)},
}

# ==================== TABLA EXACTA QUE DISTE ====================
WARNING_ZONES = {
    'Nada': {
        'name': 'Ninguna zona seleccionada',
        'scores': {},
        'tooltip': 'Sin restricciones. Puntúa libremente para explorar.'
    },
    'ZA-1': {
        'name': 'ZA-1: Transferencia Oculta de Poder',
        'scores': {'d': 4, 'g': 1},
        'tooltip': 'Coordinación que redistribuye poder sin admitirlo.\n\n'
                   'Alta coordinación casi siempre implica cambio en balance político.'
    },
    'ZA-2': {
        'name': 'ZA-2: Desliz de Soberanía',
        'scores': {'c': 4, 'g': 1},
        'tooltip': 'Cambios en control que transfieren soberanía.'
    },
    'ZA-3': {
        'name': 'ZA-3: Fusión Política',
        'scores': {'d': 5, 'g': 4},
        'tooltip': 'Unión política disfrazada de “compartir recursos”.'
    },
    'ZA-4': {
        'name': 'ZA-4: Planificación Despolitizada',
        'scores': {'b': 4, 'a': 1, 'g': 1},
        'tooltip': 'Planes estratégicos que niegan impacto en identidad y poder.'
    },
    'ZA-5': {
        'name': 'ZA-5: Coordinación Desbocada',
        'scores': {'d': 4, 'c': 2},
        'tooltip': 'Coordinación a velocidad blockchain sin frenos.'
    },
    'ZA-6': {
        'name': 'ZA-6: Coordinación Ingenua de Escasez',
        'scores': {'d': 4, 'b': 1},
        'tooltip': 'Recursos vitales sin planificación de crisis.'
    },
    'ZA-7': {
        'name': 'ZA-7: Coordinación Ciega',
        'scores': {'d': 4, 'e': 1},
        'tooltip': 'Coordinación rápida sin monitoreo.'
    },
    'ZA-8': {
        'name': 'ZA-8: Deriva Estratégica',
        'scores': {'b': 4, 'c': 1},
        'tooltip': 'Planes largos sin mecanismos de corrección.'
    },
    'ZA-9': {
        'name': 'ZA-9: Vigilancia Restrictiva',
        'scores': {'e': 4, 'g': 1},
        'tooltip': 'Vigilancia masiva de humanos sin salvaguardas.'
    },
    'ZA-10': {
        'name': 'ZA-10: Acción Simbólica',
        'scores': {'a': 4, 'f': 0, 'e': 0},
        'tooltip': 'Simbolismo vacío sin acción real.'
    },
    'ZA-11': {
        'name': 'ZA-11: Revolución Operativa Despolitizada',
        'scores': {'f': 5, 'a': 1, 'g': 1},
        'tooltip': 'Cambio operativo masivo que niega su impacto social.'
    },
    'ZA-12': {
        'name': 'ZA-12: Normalización Progresiva',
        'scores': {'c': 3, 'b': 0},
        'tooltip': 'Medidas de control que se vuelven permanentes sin nuevo voto.'
    },
    'ZA-13': {
        'name': 'ZA-13: Operaciones Ciegas',
        'scores': {'f': 4, 'e': 1},
        'tooltip': 'Revoluciones operativas masivas sin capacidad de ver efectos secundarios.'
    },
    'ZA-14': {
        'name': 'ZA-14: Captura Operativa Irreversible',
        'scores': {'f': 5, 'b': 1},
        'tooltip': 'Infraestructura operativa que encierra el futuro (costos de reversión altísimos).'
    },
    'ZA-15': {
        'name': 'ZA-15: Hiper-optimización Frágil',
        'scores': {'f': 5, 'e': 1, 'b': 1},
        'tooltip': 'Optimización extrema poco resiliente ante shocks futuros.'
    }
}

DIM_LABELS = ['f', 'e', 'd', 'c', 'b', 'a', 'g']

DIM_NAMES = {
    'a': 'Identidad', 'b': 'Planificación', 'c': 'Control', 'd': 'Coordinación',
    'e': 'Sensibilidad', 'f': 'Operaciones', 'g': 'Balance Político'
}

LEVELS = [
    ('○', 0.2), ('○○', 0.4), ('○○○', 0.6),
    ('○○○○', 0.8), ('○○○○○', 1.0)
]


class Star7System:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Autohumanismo - Sistema 7★")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 19)
        self.font_tiny = pygame.font.Font(None, 16)

        self.current_theme = 'Clásico'
        self.theme_colors = THEMES[self.current_theme]

        self.scores = {dim: None for dim in DIM_LABELS}
        self.current_zone = 'Nada'

        self.show_zone_menu = False
        self.zone_menu_rects = []

        self.circles = self._calculate_circle_positions()
        self.star_vertices = self._calculate_star_vertices()

        self.reset_button = pygame.Rect(WIDTH - 280, HEIGHT - 65, 100, 40)
        self.theme_button = pygame.Rect(WIDTH - 160, HEIGHT - 65, 140, 40)
        self.zone_button = pygame.Rect(25, HEIGHT - 65, 340, 40)

        self.show_tooltip = False
        self.tooltip_text = ""
        self.tooltip_pos = (0, 0)

    def _calculate_star_vertices(self):
        verts = []
        for i in range(7):
            angle = math.pi - (2 * math.pi * i / 7)
            x = CENTER_X + MAX_RADIUS * math.cos(angle)
            y = CENTER_Y + MAX_RADIUS * math.sin(angle)
            verts.append((x, y))
        return verts

    def _calculate_circle_positions(self):
        circles = {}
        for i, dim in enumerate(DIM_LABELS):
            angle = math.pi - (2 * math.pi * i / 7)
            circles[dim] = []
            for lvl, (label, ratio) in enumerate(LEVELS):
                r = MAX_RADIUS * ratio
                x = CENTER_X + r * math.cos(angle)
                y = CENTER_Y + r * math.sin(angle)
                circles[dim].append({'pos': (x, y), 'level': lvl, 'label': label})
        return circles

    def _apply_zone(self, zone_id):
        if zone_id == 'Nada':
            return
        zone = WARNING_ZONES[zone_id]
        for dim, level in zone.get('scores', {}).items():
            if dim in self.scores:
                self.scores[dim] = level

    # ==================== DRAW FUNCTIONS ====================
    def _draw_background_star(self):
        if len(self.star_vertices) >= 3:
            pygame.draw.polygon(self.screen, self.theme_colors['star'], self.star_vertices)
            pygame.draw.polygon(self.screen, BLACK, self.star_vertices, 3)

    def _draw_axes(self):
        for i, dim in enumerate(DIM_LABELS):
            angle = math.pi - (2 * math.pi * i / 7)
            ex = CENTER_X + MAX_RADIUS * math.cos(angle)
            ey = CENTER_Y + MAX_RADIUS * math.sin(angle)
            pygame.draw.line(self.screen, self.theme_colors[dim], (CENTER_X, CENTER_Y), (ex, ey), 5)

    def _draw_rings(self):
        for _, ratio in LEVELS:
            pygame.draw.circle(self.screen, GRAY, (CENTER_X, CENTER_Y), int(MAX_RADIUS * ratio), 1)

    def _draw_circles(self):
        for dim in DIM_LABELS:
            sel = self.scores[dim]
            for c in self.circles[dim]:
                x, y = c['pos']
                lvl = c['level']
                filled = (sel is not None and lvl <= sel)
                color = self.theme_colors[dim] if filled else BLACK
                pygame.draw.circle(self.screen, color, (int(x), int(y)), CIRCLE_RADIUS)
                pygame.draw.circle(self.screen, WHITE, (int(x), int(y)), CIRCLE_RADIUS, 3)

    def _draw_labels(self):
        for i, dim in enumerate(DIM_LABELS):
            angle = math.pi - (2 * math.pi * i / 7)
            r = MAX_RADIUS + 85
            x = CENTER_X + r * math.cos(angle)
            y = CENTER_Y + r * math.sin(angle)

            pygame.draw.circle(self.screen, WHITE, (int(x), int(y)), 29)
            pygame.draw.circle(self.screen, self.theme_colors[dim], (int(x), int(y)), 29, 3)

            txt = self.font_large.render(dim, True, self.theme_colors[dim])
            self.screen.blit(txt, txt.get_rect(center=(x, y)))

            name = self.font_small.render(DIM_NAMES[dim], True, BLACK)
            nr = name.get_rect(center=(x, y + 38))
            pygame.draw.rect(self.screen, WHITE, nr.inflate(8, 4))
            self.screen.blit(name, nr)

    def _draw_score_polygon(self):
        pts = []
        for dim in DIM_LABELS:
            if self.scores[dim] is not None and self.scores[dim] < len(self.circles[dim]):
                c = self.circles[dim][self.scores[dim]]
                pts.append(c['pos'])
            else:
                pts.append((CENTER_X, CENTER_Y))
        if len(pts) >= 3:
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.polygon(s, (100, 150, 255, 130), pts)
            self.screen.blit(s, (0, 0))
            pygame.draw.polygon(self.screen, (60, 120, 220), pts, 4)

    def _draw_buttons(self):
        # Reset
        pygame.draw.rect(self.screen, (190, 60, 60), self.reset_button)
        pygame.draw.rect(self.screen, BLACK, self.reset_button, 2)
        self.screen.blit(self.font.render("Reset", True, WHITE),
                         self.font.render("Reset", True, WHITE).get_rect(center=self.reset_button.center))

        # Theme
        pygame.draw.rect(self.screen, (70, 110, 190), self.theme_button)
        pygame.draw.rect(self.screen, BLACK, self.theme_button, 2)
        self.screen.blit(self.font_small.render(f"Tema: {self.current_theme}", True, WHITE),
                         self.font_small.render(f"Tema: {self.current_theme}", True, WHITE).get_rect(center=self.theme_button.center))

        # Zone Button
        col = (180, 50, 50) if self.current_zone != 'Nada' else (90, 90, 90)
        pygame.draw.rect(self.screen, col, self.zone_button)
        pygame.draw.rect(self.screen, BLACK, self.zone_button, 2)
        txt = self.font_small.render(f"Zona: {self.current_zone}", True, WHITE)
        self.screen.blit(txt, txt.get_rect(center=self.zone_button.center))

    def _draw_zone_menu(self):
        if not self.show_zone_menu:
            return
        self.zone_menu_rects = []
        start_y = self.zone_button.y - 30 - len(WARNING_ZONES) * 42

        for i, (zid, data) in enumerate(WARNING_ZONES.items()):
            rect = pygame.Rect(self.zone_button.x, start_y + i*42, 340, 40)
            self.zone_menu_rects.append((rect, zid))

            color = (160, 60, 60) if zid == self.current_zone else (110, 110, 120)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)

            txt = self.font_small.render(data['name'], True, WHITE)
            self.screen.blit(txt, txt.get_rect(center=rect.center))

    def _handle_click(self, pos):
        x, y = pos

        if self.reset_button.collidepoint(pos):
            self.scores = {dim: None for dim in DIM_LABELS}
            self.current_zone = 'Nada'
            return

        if self.theme_button.collidepoint(pos):
            themes = list(THEMES.keys())
            idx = themes.index(self.current_theme)
            self.current_theme = themes[(idx + 1) % len(themes)]
            self.theme_colors = THEMES[self.current_theme]
            return

        if self.zone_button.collidepoint(pos):
            self.show_zone_menu = not self.show_zone_menu
            return

        # Click on zone menu
        if self.show_zone_menu:
            for rect, zid in self.zone_menu_rects:
                if rect.collidepoint(pos):
                    self.current_zone = zid
                    self._apply_zone(zid)
                    self.show_zone_menu = False
                    return

        # Click on circles
        for dim in DIM_LABELS:
            for c in self.circles[dim]:
                cx, cy = c['pos']
                if math.hypot(x - cx, y - cy) <= CIRCLE_RADIUS + 10:
                    lvl = c['level']
                    self.scores[dim] = None if self.scores[dim] == lvl else lvl
                    return

    def _handle_motion(self, pos):
        self.show_tooltip = False
        if self.show_zone_menu:
            for rect, zid in self.zone_menu_rects:
                if rect.collidepoint(pos):
                    self.show_tooltip = True
                    self.tooltip_text = WARNING_ZONES[zid]['tooltip']
                    self.tooltip_pos = (rect.right + 15, rect.top)
                    return

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._handle_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self._handle_motion(event.pos)

            self.screen.fill(LIGHT_GRAY)

            self._draw_background_star()
            self._draw_rings()
            self._draw_axes()
            self._draw_score_polygon()
            self._draw_circles()
            self._draw_labels()
            self._draw_buttons()
            self._draw_zone_menu()

            if self.show_tooltip:
                # Simple tooltip
                lines = self.tooltip_text.split('\n')
                h = len(lines)*20 + 20
                rect = pygame.Rect(self.tooltip_pos[0], self.tooltip_pos[1], 520, h)
                pygame.draw.rect(self.screen, TOOLTIP_BG, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 2)
                for i, line in enumerate(lines):
                    t = self.font_tiny.render(line, True, TOOLTIP_TEXT)
                    self.screen.blit(t, (rect.x+12, rect.y+10 + i*20))

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Star7System().run()