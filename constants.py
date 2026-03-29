"""
constants.py – All magic numbers live here.
"""

# ── Window ────────────────────────────────────────────────────────────────────
SCREEN_W   = 960
SCREEN_H   = 640
FPS        = 60
TITLE      = "CareerQuest"

# ── Colours (RGB) ─────────────────────────────────────────────────────────────
C_BLACK      = (  0,   0,   0)
C_WHITE      = (255, 255, 255)
C_BG         = ( 30,  30,  50)
C_PANEL      = ( 15,  15,  35, 220)      # alpha for surfaces
C_BORDER     = (245, 197,  24)           # gold
C_TEXT       = (240, 236, 226)
C_TEXT_DIM   = (160, 155, 145)
C_GREEN      = ( 74, 222, 128)
C_RED        = (248, 113, 113)
C_BLUE       = ( 96, 165, 250)
C_PINK       = (244, 114, 182)
C_PURPLE     = (167, 139, 250)
C_YELLOW     = (253, 224,  71)
C_GRASS      = ( 80, 160,  70)
C_PATH       = (180, 160, 120)
C_SKY        = (100, 180, 240)

# Building zone colours (roof colours used in map renderer)
C_CLINIC     = (180,  80,  80)
C_HOTEL      = ( 80, 120, 200)
C_REALESTATE = ( 80, 180,  80)

# ── Tile / map ─────────────────────────────────────────────────────────────────
TILE        = 32          # pixels per tile
MAP_COLS    = 30
MAP_ROWS    = 20

# ── Player ─────────────────────────────────────────────────────────────────────
PLAYER_SPEED   = 140      # px / second
PLAYER_SIZE    = 28       # collision rect

# ── Scenes (state machine keys) ───────────────────────────────────────────────
SCENE_INTRO       = "intro"
SCENE_WORLD       = "world"
SCENE_CLINIC      = "clinic"
SCENE_HOTEL       = "hotel"
SCENE_REALESTATE  = "realestate"
SCENE_RESULT      = "result"

# ── Building entry zones (tile rectangles in world space) ─────────────────────
# Each is (col, row, w_tiles, h_tiles)
ZONE_CLINIC      = (4,  3, 5, 4)
ZONE_HOTEL       = (13, 3, 5, 4)
ZONE_REALESTATE  = (22, 3, 5, 4)

# ── Dialogue config ────────────────────────────────────────────────────────────
MAX_TURNS    = 7          # max player messages per session
WAGE_GREAT   = 500
WAGE_OK      = 250
WAGE_POOR    = 100
