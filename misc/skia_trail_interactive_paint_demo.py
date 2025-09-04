import rp#pip install rp
import sys, io, math
import numpy as np
import pygame

# ------------------------------------------------------------
# Config
# ------------------------------------------------------------
W, H = 1260, 800
CANVAS_W = 980
SIDEBAR_W = W - CANVAS_W
BG_COLOR = (245, 245, 248, 255)

POINT_ADD_THRESHOLD = 3.0
RESAMPLE_STEP = 2.5
SMOOTH_PASSES = 1
INTERP = "bilinear"
MIPMAP = True
V_SUBDIVS = 30

# OnlyGFX Vol.2 pack (30 images)
ONLYGFX_PREFIX = "https://www.onlygfx.com/wp-content/uploads/2017/05/"
TEXTURE_URLS = [
    f"{ONLYGFX_PREFIX}colorful-watercolor-brush-stroke-banner-2-{i}.png"
    for i in range(1, 31)
]
TEXTURE_URLS += [
    f"https://www.onlygfx.com/wp-content/uploads/2017/07/paint-brush-stroke-10-{i}.png"
    for i in range(1, 50)
]

TEXTURE_URLS+=["https://www.clker.com/cliparts/9/b/2/8/11949855961746203850arrow-right-blue_benji_p_01.svg.hi.png"]
TEXTURE_URLS+=[
        "https://t3.ftcdn.net/jpg/06/10/33/46/360_F_610334619_KWi9z8SdeRRyBBRTfQ0hUoQctWEBVL81.png",
        "https://huggingface.co/datasets/OneOverZero/MAGICK/resolve/main/images/6J/6JQUhsQZ9l.png",
]

TEXTURE_URLS = rp.download_urls_to_cache(TEXTURE_URLS,cache_dir=rp.r._rp_downloads_folder+'/brushstroke_images',show_progress=True)

DEFAULT_INDEX = 11  # 0-based; pick your fav default

# UI theme
PAD = 12
SIDEBAR_BG = (250, 250, 252, 255)
SIDEBAR_BORDER = (220, 222, 230, 255)
THUMB_BG = (255, 255, 255, 255)
HILITE = (46, 125, 255, 180)
TEXT = (80, 84, 92)
LINE = (220, 222, 230)
SCROLL_TRACK = (232, 235, 242)
SCROLL_THUMB = (180, 186, 200)

THUMB_W = SIDEBAR_W - PAD * 2 - 14  # leave space for scrollbar
THUMB_MAX_H = 120
THUMB_MARGIN = 10

# Sliders
SIZE_MIN = 6
SIZE_MAX = 140
DEFAULT_SIZE_START = 38
DEFAULT_SIZE_END   = 68

# Blend modes (user supplied map)
_SKIA_BLEND_MODES = {
    'blend': 'kSrcOver', 'replace': 'kSrc', 'add': 'kPlus', 'multiply': 'kMultiply',
    'screen': 'kScreen', 'overlay': 'kOverlay', 'darken': 'kDarken', 'lighten': 'kLighten',
    'difference': 'kDifference', 'exclusion': 'kExclusion', 'burn': 'kColorBurn',
    'dodge': 'kColorDodge', 'hue': 'kHue', 'saturation': 'kSaturation', 'luminosity': 'kLuminosity'
}
BLEND_NAMES = list(_SKIA_BLEND_MODES.keys())
DEFAULT_BLEND = 'blend'

# ------------------------------------------------------------
# Helpers (math & resampling)
# ------------------------------------------------------------
def dist(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.hypot(dx, dy)

def chaikin(points: np.ndarray, passes: int = 1) -> np.ndarray:
    if len(points) < 3 or passes <= 0:
        return points
    P = points
    for _ in range(passes):
        new_pts = [P[0]]
        for i in range(len(P) - 1):
            p, q = P[i], P[i + 1]
            Q = 0.75 * p + 0.25 * q
            R = 0.25 * p + 0.75 * q
            new_pts.extend([Q, R])
        new_pts.append(P[-1])
        P = np.asarray(new_pts, dtype=np.float32)
    return P

def resample_uniform(points: np.ndarray, step: float = 10.5) -> np.ndarray:
    if len(points) < 2:
        return points
    diffs = np.diff(points, axis=0)
    seglens = np.sqrt((diffs ** 2).sum(axis=1))
    total = float(seglens.sum())
    if total < 1e-6:
        return points[:1].copy()
    n = max(2, int(total / max(1e-6, step)) + 1)
    cum = np.concatenate([[0.0], np.cumsum(seglens)])
    t = cum / total
    xi = np.linspace(0.0, 1.0, n)
    x = np.interp(xi, t, points[:, 0])
    y = np.interp(xi, t, points[:, 1])
    return np.stack([x, y], axis=1).astype(np.float32)

def ensure_rgba_uint8(arr, w, h):
    arr = np.ascontiguousarray(arr, dtype=np.uint8)
    assert arr.shape == (h, w, 4), f"Canvas shape must be {(h, w, 4)}, got {arr.shape}"
    return arr

def surface_from_rgba(rgba: np.ndarray) -> pygame.Surface:
    h, w, _ = rgba.shape
    view = rgba.tobytes()
    return pygame.image.frombuffer(view, (w, h), "RGBA").convert_alpha()

# ------------------------------------------------------------
# Trail renderer (taper + wobble + selected blend mode)
# ------------------------------------------------------------
def render_trail(canvas_rgba: np.ndarray,
                 points_xy: np.ndarray,
                 texture_rgba: np.ndarray,
                 size_start_px: float,
                 size_end_px: float,
                 blend_mode_name: str) -> np.ndarray:
    if len(points_xy) < 2:
        return canvas_rgba

    sm = chaikin(points_xy, SMOOTH_PASSES)
    sm = resample_uniform(sm, RESAMPLE_STEP)

    n = len(sm)
    u = np.linspace(0.0, 1.0, n, dtype=np.float32)

    # Linear taper: thickness(u) = lerp(start, end, u)
    thickness = (1.0 - u) * size_start_px + u * size_end_px

    # Subtle shape variation (wobble)
    wobble = 0.15 * np.sin(2.0 * math.pi * 3.0 * u)

    # Split into inner/outer radii with a gentle asymmetry (brushier look)
    # inner ~ 45% of width, outer ~ 55% of width
    inner = 0.45 * thickness * (1.0 + 0.10 * wobble)
    outer = 0.55 * thickness * (1.0 + 0.18 * wobble)

    mode = blend_mode_name if blend_mode_name in _SKIA_BLEND_MODES else 'blend'

    return rp.skia_draw_trail(
        canvas_rgba,
        sm.astype(np.float32),
        texture_rgba,
        thickness=None,
        alpha=1.0,
        loop=False,
        mode=mode,
        copy=True,
        inner_radius=inner,
        outer_radius=outer,
        interp=INTERP,
        mipmap=MIPMAP,
    )

# ------------------------------------------------------------
# UI widgets: Slider & Dropdown
# ------------------------------------------------------------
class Slider:
    def __init__(self, rect, vmin, vmax, value, label, units="px"):
        self.rect = pygame.Rect(rect)
        self.vmin = float(vmin)
        self.vmax = float(vmax)
        self.value = float(value)
        self.label = label
        self.units = units
        self.dragging = False
        self.handle_radius = 7
        self.font = pygame.font.SysFont(None, 18)

    def _track_rect(self):
        x, y, w, h = self.rect
        return pygame.Rect(x, y + h//2 - 2, w, 4)

    def _value_to_x(self, v):
        t = (v - self.vmin) / (self.vmax - self.vmin)
        t = max(0.0, min(1.0, t))
        return self.rect.x + int(t * self.rect.w)

    def _x_to_value(self, x):
        t = (x - self.rect.x) / max(1, self.rect.w)
        t = max(0.0, min(1.0, t))
        return self.vmin + t * (self.vmax - self.vmin)

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.rect.collidepoint(e.pos):
                self.dragging = True
                self.value = self._x_to_value(e.pos[0])
                return True
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            self.dragging = False
        elif e.type == pygame.MOUSEMOTION and self.dragging:
            self.value = self._x_to_value(e.pos[0])
            return True
        return False

    def draw(self, screen):
        # label
        cap = f"{self.label}: {int(round(self.value))}{self.units}"
        label_surface = self.font.render(cap, True, TEXT)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 18))

        # track
        track = self._track_rect()
        pygame.draw.rect(screen, LINE, track, border_radius=2)

        # handle
        hx = self._value_to_x(self.value)
        hy = track.centery
        pygame.draw.circle(screen, (30, 30, 32), (hx, hy), self.handle_radius + 2)
        pygame.draw.circle(screen, (240, 240, 245), (hx, hy), self.handle_radius)

class Dropdown:
    def __init__(self, rect, options, value, label):
        self.rect = pygame.Rect(rect)
        self.options = list(options)
        self.value = value if value in options else options[0]
        self.open = False
        self.font = pygame.font.SysFont(None, 18)
        self.label = label
        self.item_h = 22

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.open:
                # click an option?
                opt_rects = self._option_rects()
                for i, r in enumerate(opt_rects):
                    if r.collidepoint(e.pos):
                        self.value = self.options[i]
                        self.open = False
                        return True
                # click outside closes
                if not self.rect.collidepoint(e.pos):
                    self.open = False
            else:
                if self.rect.collidepoint(e.pos):
                    self.open = True
                    return True
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button != 1:
            self.open = False
        return False

    def _option_rects(self):
        rects = []
        x, y, w, h = self.rect
        for i, _ in enumerate(self.options):
            rects.append(pygame.Rect(x, y + h + i * self.item_h, w, self.item_h))
        return rects

    def draw(self, screen):
        # label
        label_surface = self.font.render(self.label, True, TEXT)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 18))

        # main box
        pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=6)
        pygame.draw.rect(screen, LINE, self.rect, 1, border_radius=6)

        txt = self.font.render(self.value, True, (40, 44, 52))
        screen.blit(txt, (self.rect.x + 8, self.rect.y + 4))

        # chevron
        cx = self.rect.right - 16
        cy = self.rect.y + self.rect.h // 2
        pygame.draw.polygon(screen, (120, 124, 134),
                            [(cx - 6, cy - 3), (cx + 6, cy - 3), (cx, cy + 4)])

        # options
        if self.open:
            for i, r in enumerate(self._option_rects()):
                pygame.draw.rect(screen, (255, 255, 255), r)
                pygame.draw.rect(screen, LINE, r, 1)
                t = self.font.render(self.options[i], True, (40, 44, 52))
                screen.blit(t, (r.x + 8, r.y + 3))

# ------------------------------------------------------------
# Sidebar with visible scrollbar
# ------------------------------------------------------------
class TextureSidebar:
    def __init__(self, rect, urls):
        self.rect = pygame.Rect(rect)
        self.urls = urls
        self.textures = [None] * len(urls)  # numpy RGBA (cached)
        self.thumbs = [None] * len(urls)    # pygame.Surface thumbnails
        self.scroll = 0                     # px
        self.selected = DEFAULT_INDEX if 0 <= DEFAULT_INDEX < len(urls) else 0
        self.font = pygame.font.SysFont(None, 18)

        # UI controls
        controls_top = 44
        controls_x = self.rect.x + PAD
        controls_w = THUMB_W
        self.slider_start = Slider((controls_x, controls_top + 0, controls_w, 28),
                                   SIZE_MIN, SIZE_MAX, DEFAULT_SIZE_START, "Start size")
        self.slider_end   = Slider((controls_x, controls_top + 50, controls_w, 28),
                                   SIZE_MIN, SIZE_MAX, DEFAULT_SIZE_END,   "End size")
        self.dropdown_blend = Dropdown((controls_x, controls_top + 100, controls_w, 26),
                                       BLEND_NAMES, DEFAULT_BLEND, "Blend mode")

        # Preload selected texture (cached via user's load_image)
        self._ensure_loaded(self.selected)

    # ---- data/load ----
    def _ensure_loaded(self, idx):
        if self.textures[idx] is None:
            try:
                # IMPORTANT: use your cache-aware loader
                tex = rp.load_image(self.urls[idx], use_cache=True)
                tex = rp.resize_image_to_fit(tex, height=SIZE_MAX, allow_growth=False)
                # Ensure RGBA uint8 contiguous
                if tex.ndim == 2:
                    tex = tex[..., None]
                if tex.shape[-1] == 3:
                    # pad an opaque alpha
                    a = np.full((*tex.shape[:2], 1), 255, dtype=np.uint8)
                    tex = np.concatenate([tex, a], axis=2)
                tex = np.ascontiguousarray(tex, dtype=np.uint8)
            except Exception as e:
                print(f"Failed to load texture {idx+1}: {e}")
                tex = np.zeros((32, 32, 4), dtype=np.uint8)
            self.textures[idx] = tex
        if self.thumbs[idx] is None:
            self.thumbs[idx] = self._make_thumb(self.textures[idx])

    def _make_thumb(self, rgba: np.ndarray) -> pygame.Surface:
        h, w, _ = rgba.shape
        # Scale to fit card
        scale = THUMB_W / max(1, w)
        th = min(int(h * scale), THUMB_MAX_H)
        img = surface_from_rgba(rgba)
        img = pygame.transform.smoothscale(img, (THUMB_W, th))
        # Composite over white card
        card = pygame.Surface((THUMB_W, th), pygame.SRCALPHA)
        card.fill(THUMB_BG)
        card.blit(img, (0, 0))
        return card

    def current_texture(self):
        self._ensure_loaded(self.selected)
        return self.textures[self.selected]

    def current_sizes(self):
        return float(self.slider_start.value), float(self.slider_end.value)

    def current_blend(self):
        return self.dropdown_blend.value

    # ---- content geometry ----
    def _content_height(self):
        # space for header + controls + thumbs
        header = 28
        controls_block = 140
        thumbs_count = len(self.urls)
        return header + controls_block + THUMB_MARGIN + thumbs_count * (THUMB_MAX_H + THUMB_MARGIN)

    def _thumb_rects(self):
        rects = []
        y = self.rect.y + 28 + 140 + THUMB_MARGIN - self.scroll
        for _ in self.urls:
            rects.append(pygame.Rect(self.rect.x + PAD, int(y), THUMB_W, THUMB_MAX_H))
            y += THUMB_MAX_H + THUMB_MARGIN
        return rects

    # ---- events ----
    def handle_event(self, e):
        # Controls first
        if self.slider_start.handle_event(e): return True
        if self.slider_end.handle_event(e):   return True
        if self.dropdown_blend.handle_event(e): return True

        if e.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            if self.rect.collidepoint(mx, my):
                self._scroll_by(-e.y * 40)
                return True

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mx, my = e.pos
            if self.rect.collidepoint(mx, my):
                # clicking scrollbar?
                sb = self._scrollbar_rect()
                if sb.collidepoint(mx, my):
                    # jump to proportional position
                    self._scroll_to(self._scroll_from_mouse(my))
                    return True
                # clicking a thumb?
                for i, r in enumerate(self._thumb_rects()):
                    if r.collidepoint(mx, my):
                        self.selected = i
                        self._ensure_loaded(i)
                        return True
        return False

        # (Drag scrollbar thumb could be added; click-to-jump keeps code compact.)

    def _scrollbar_rect(self):
        # vertical scrollbar track on the right of sidebar
        return pygame.Rect(self.rect.right - (PAD + 8), self.rect.y + 28, 8, self.rect.h - 40)

    def _scroll_by(self, dy):
        self._scroll_to(self.scroll + dy)

    def _scroll_to(self, val):
        max_scroll = max(0, self._content_height() - self.rect.h)
        self.scroll = max(0, min(max_scroll, int(val)))

    def _scroll_from_mouse(self, my):
        track = self._scrollbar_rect()
        if track.h <= 0: return 0
        t = (my - track.y) / max(1, track.h)
        return t * max(0, self._content_height() - self.rect.h)

    # ---- draw ----
    def draw(self, screen):
        # Panel BG + border
        panel = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        panel.fill(SIDEBAR_BG)
        screen.blit(panel, self.rect.topleft)
        pygame.draw.rect(screen, SIDEBAR_BORDER, self.rect, 1)

        font = self.font
        label = font.render("Brushes (OnlyGFX Vol.2)", True, TEXT)

        # Thumb list
        y = self.rect.y + 28 + 140 + THUMB_MARGIN - self.scroll
        for i, url in enumerate(self.urls):
            self._ensure_loaded(i)
            thumb = self.thumbs[i]
            th = thumb.get_height()
            card_rect = pygame.Rect(self.rect.x + PAD, int(y), THUMB_W, min(THUMB_MAX_H, th))
            # highlight
            if i == self.selected:
                pygame.draw.rect(screen, HILITE, card_rect.inflate(6, 6), 2, border_radius=6)
            pygame.draw.rect(screen, (235, 237, 242), card_rect, 1, border_radius=6)
            screen.blit(thumb, card_rect.topleft)
            cap = font.render(f"#{i+1}", True, (90, 94, 102))
            screen.blit(cap, (card_rect.x, card_rect.bottom + 2))
            y += THUMB_MAX_H + THUMB_MARGIN

        # Title
        screen.blit(label, (self.rect.x + PAD, self.rect.y + 8))

        # Controls
        self.slider_start.draw(screen)
        self.slider_end.draw(screen)
        self.dropdown_blend.draw(screen)

        # Visible scrollbar
        track = self._scrollbar_rect()
        pygame.draw.rect(screen, SCROLL_TRACK, track, border_radius=4)
        # thumb size proportional to viewport/content
        content_h = self._content_height()
        if content_h > 0:
            view_ratio = min(1.0, self.rect.h / content_h)
        else:
            view_ratio = 1.0
        thumb_h = max(24, int(track.h * view_ratio))
        max_scroll = max(1, content_h - self.rect.h)
        t = self.scroll / max_scroll if max_scroll > 0 else 0.0
        thumb_y = track.y + int((track.h - thumb_h) * t)
        thumb_rect = pygame.Rect(track.x, thumb_y, track.w, thumb_h)
        pygame.draw.rect(screen, SCROLL_THUMB, thumb_rect, border_radius=4)

        # Tiny hint
        hint = font.render("scroll", True, (140, 144, 154))
        screen.blit(hint, (track.x - 36, track.bottom - 16))

# ------------------------------------------------------------
# App
# ------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H), pygame.SRCALPHA)
    pygame.display.set_caption("Textured Brush Trails (Skia) — Brush Picker + Sliders + Blend")
    clock = pygame.time.Clock()

    # Base canvas RGBA
    base = np.zeros((H, CANVAS_W, 4), dtype=np.uint8)
    base[...] = BG_COLOR
    base_surface = surface_from_rgba(ensure_rgba_uint8(base, CANVAS_W, H))

    # Sidebar
    sidebar = TextureSidebar((CANVAS_W, 0, SIDEBAR_W, H), TEXTURE_URLS)

    # Current stroke
    drawing = False
    current_pts = []
    last_pt = None
    preview_surface = None

    running = True
    while running:
        for event in pygame.event.get():
            # Sidebar UI first
            if sidebar.handle_event(event):
                # if brush/size/mode changes during a drag, live re-render preview
                if drawing and len(current_pts) >= 2:
                    tex = sidebar.current_texture()
                    s0, s1 = sidebar.current_sizes()
                    mode = sidebar.current_blend()
                    preview_img = render_trail(base, np.array(current_pts, dtype=np.float32), tex, s0, s1, mode)
                    preview_surface = surface_from_rgba(ensure_rgba_uint8(preview_img, CANVAS_W, H))
                continue

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_c:
                    base[...] = BG_COLOR
                    base_surface = surface_from_rgba(base)
                    current_pts.clear()
                    preview_surface = None
                elif event.key == pygame.K_s:
                    pygame.image.save(base_surface, "painting.png")
                    print("Saved painting.png")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.mouse.get_pos()[0] < CANVAS_W:
                    drawing = True
                    pos = pygame.mouse.get_pos()
                    current_pts = [np.array(pos, dtype=np.float32)]
                    last_pt = current_pts[0]

            elif event.type == pygame.MOUSEMOTION and drawing:
                x, y = pygame.mouse.get_pos()
                if x >= CANVAS_W:
                    continue
                p = np.array((x, y), dtype=np.float32)
                if last_pt is None or dist(p, last_pt) >= POINT_ADD_THRESHOLD:
                    current_pts.append(p)
                    last_pt = p
                    tex = sidebar.current_texture()
                    s0, s1 = sidebar.current_sizes()
                    mode = sidebar.current_blend()
                    preview_img = render_trail(base, np.array(current_pts, dtype=np.float32), tex, s0, s1, mode)
                    preview_surface = surface_from_rgba(ensure_rgba_uint8(preview_img, CANVAS_W, H))

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
                drawing = False
                if len(current_pts) >= 2:
                    tex = sidebar.current_texture()
                    s0, s1 = sidebar.current_sizes()
                    mode = sidebar.current_blend()
                    base = render_trail(base, np.array(current_pts, dtype=np.float32), tex, s0, s1, mode)
                    base_surface = surface_from_rgba(ensure_rgba_uint8(base, CANVAS_W, H))
                current_pts.clear()
                last_pt = None
                preview_surface = None

        # Draw frame
        screen.fill((0, 0, 0, 0))
        screen.blit(base_surface, (0, 0))
        if preview_surface is not None:
            screen.blit(preview_surface, (0, 0))
        sidebar.draw(screen)

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()
    sys.exit()


main()