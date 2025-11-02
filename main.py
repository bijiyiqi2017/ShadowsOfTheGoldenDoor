import pygame
import sys
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize audio mixer

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (34, 34, 34)  # Dark gray
FPS = 60

# Colors
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
RED = (255, 50, 50)
WALL_COLOR = (100, 80, 60)  # Brownish color for walls
PATH_COLOR = (50, 50, 50)  # Darker gray for paths
WALL_COLLISION_COLOR = (150, 100, 80)  # Lighter brown for collision flash

# Maze Configuration
GRID_SIZE = 10
CELL_SIZE = 50  # Each cell is 50x50 pixels
MAZE_OFFSET_X = (WINDOW_WIDTH - (GRID_SIZE * CELL_SIZE)) // 2
MAZE_OFFSET_Y = 80  # Offset from top to leave room for title

# Game States
TITLE_SCREEN = "title"
GAME_PLAYING = "playing"

# Display Window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shadows of the Golden Door")

# Clock for controlling frame rate and delta time
clock = pygame.time.Clock()

# Fonts
subtitle_font = pygame.font.Font(None, 36)
instruction_font = pygame.font.Font(None, 24)


# === UTILITY FUNCTIONS ===

def load_image(path, scale_width=None):
    """
    Load an image with optional scaling and error handling.
    Returns (image, success_bool).
    """
    try:
        image = pygame.image.load(path)
        if scale_width:
            scale_height = int(image.get_height() * (scale_width / image.get_width()))
            image = pygame.transform.scale(image, (scale_width, scale_height))
        print(f"✓ Loaded: {path}")
        return image, True
    except (pygame.error, FileNotFoundError) as e:
        print(f"✗ Warning: Could not load {path}. Error: {e}")
        return None, False


def load_sound(path):
    """
    Load a sound effect with error handling.
    Returns (sound, success_bool).
    """
    try:
        sound = pygame.mixer.Sound(path)
        print(f"✓ Loaded sound: {path}")
        return sound, True
    except (pygame.error, FileNotFoundError) as e:
        print(f"✗ Warning: Could not load sound {path}. Error: {e}")
        return None, False


def create_placeholder_surface(width, height, text):
    """Create a placeholder surface when assets fail to load."""
    surface = pygame.Surface((width, height))
    surface.fill((100, 100, 100))
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    surface.blit(text_surface, text_rect)
    return surface


# === ASSET LOADING ===

# Load logo
logo_image, logo_loaded = load_image('assets/logo/SH logo.png', scale_width=800)
if not logo_loaded:
    logo_image = create_placeholder_surface(400, 100, "GAME LOGO")
    logo_loaded = True  # Use placeholder

# Load button images
button_normal, btn_normal_loaded = load_image('assets/button/start_button.png')
button_hover, btn_hover_loaded = load_image('assets/button/start_button_hover.png')
button_images_loaded = btn_normal_loaded and btn_hover_loaded

# Create placeholder buttons if needed
if not button_images_loaded:
    button_normal = create_placeholder_surface(200, 60, "START GAME")
    button_hover = create_placeholder_surface(200, 60, ">>> START <<<")
    button_images_loaded = True

# Load sound effects
move_sound, _ = load_sound('assets/sounds/move.wav')
collision_sound, _ = load_sound('assets/sounds/collision.wav')
button_click_sound, _ = load_sound('assets/sounds/button_click.wav')

# Try to load background music
try:
    pygame.mixer.music.load('assets/sounds/background_music.mp3')
    pygame.mixer.music.set_volume(0.3)
    music_loaded = True
    print("✓ Loaded background music")
except (pygame.error, FileNotFoundError):
    music_loaded = False
    print("✗ Warning: Could not load background music")


# === BUTTON CLASS ===

class Button:
    """Interactive button with hover effects and animations."""
    
    def __init__(self, x, y):
        self.normal_image = button_normal
        self.hover_image = button_hover
        self.rect = self.normal_image.get_rect(topleft=(x, y))
        self.clickable_rect = self.rect
        self.hovered = False
        self.glow_alpha = 0  # For glow animation
        self.glow_direction = 1  # 1 for increasing, -1 for decreasing
    
    def draw(self, surface):
        """Draw the button with optional glow effect."""
        # Draw glow effect FIRST (behind the button)
        if self.hovered:
            # Create a glow border effect
            glow_size = int(10 + (self.glow_alpha / 40) * 5)  # Pulsing size
            glow_rect = self.rect.inflate(glow_size * 2, glow_size * 2)
            
            # Draw multiple layers for a softer glow
            for i in range(3):
                alpha = int(self.glow_alpha * (1 - i * 0.3))
                if alpha > 0:
                    glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                    glow_color = (*GOLD, alpha)
                    pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), border_radius=40)
                    surface.blit(glow_surface, glow_rect.topleft)
        
        # Draw button image on top
        image = self.hover_image if self.hovered else self.normal_image
        surface.blit(image, self.rect)
    
    def update(self, dt):
        """Update glow animation."""
        if self.hovered:
            self.glow_alpha += self.glow_direction * 200 * dt
            if self.glow_alpha >= 80:
                self.glow_alpha = 80
                self.glow_direction = -1
            elif self.glow_alpha <= 30:
                self.glow_alpha = 30
                self.glow_direction = 1
        else:
            self.glow_alpha = 0
            self.glow_direction = 1
    
    def check_hover(self, pos):
        """Check if mouse is hovering over button."""
        was_hovered = self.hovered
        self.hovered = self.clickable_rect.collidepoint(pos)
        
        # Change cursor to hand when hovering
        if self.hovered and not was_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif not self.hovered and was_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def is_clicked(self, pos):
        """Check if button was clicked."""
        return self.clickable_rect.collidepoint(pos)


# === PLAYER CLASS ===

class Player:
    """Player character with movement and collision detection."""
    
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.color = (255, 255, 0)  # Yellow
        self.speed = 200
        self.pos = pygame.math.Vector2(x, y)
        self.edge_warning_flash = 0  # Timer for edge warning
        self.collision_flash = 0  # Timer for collision flash
        self.last_move_sound_time = 0  # Cooldown for move sound
    
    def get_rect(self):
        """Return the player's collision rectangle."""
        return pygame.Rect(round(self.pos.x), round(self.pos.y), self.width, self.height)
    
    def move(self, direction, dt, wall_rectangles):
        """Move the player and handle collisions."""
        if direction.length_squared() > 0:
            direction.normalize_ip()
        
        old_pos = self.pos.copy()
        self.pos += direction * self.speed * dt
        
        # Check collision with walls
        player_rect = self.get_rect()
        collision = False
        for wall in wall_rectangles:
            if player_rect.colliderect(wall):
                collision = True
                break
        
        # Revert if collision occurred
        if collision:
            self.pos = old_pos
            self.collision_flash = 0.2  # Flash for 0.2 seconds
            if collision_sound:
                collision_sound.play()
        else:
            # Play move sound (with cooldown to avoid spam)
            current_time = pygame.time.get_ticks() / 1000.0
            if direction.length_squared() > 0 and move_sound:
                if current_time - self.last_move_sound_time > 0.2:
                    move_sound.play()
                    self.last_move_sound_time = current_time
        
        # Keep player within window bounds
        self.pos.x = max(0, min(self.pos.x, WINDOW_WIDTH - self.width))
        self.pos.y = max(0, min(self.pos.y, WINDOW_HEIGHT - self.height))
        
        # Check if near edges (within 30 pixels)
        if (self.pos.x < 30 or self.pos.x > WINDOW_WIDTH - self.width - 30 or
            self.pos.y < 30 or self.pos.y > WINDOW_HEIGHT - self.height - 30):
            self.edge_warning_flash = 0.3
    
    def update(self, dt):
        """Update player state (timers, animations, etc.)."""
        if self.collision_flash > 0:
            self.collision_flash -= dt
        if self.edge_warning_flash > 0:
            self.edge_warning_flash -= dt
    
    def draw(self, surface):
        """Draw the player with visual effects."""
        player_rect = self.get_rect()
        
        # Draw edge warning
        if self.edge_warning_flash > 0:
            warning_surf = pygame.Surface((self.width + 10, self.height + 10))
            warning_surf.set_alpha(int(150 * (self.edge_warning_flash / 0.3)))
            warning_surf.fill(RED)
            warning_rect = warning_surf.get_rect(center=player_rect.center)
            surface.blit(warning_surf, warning_rect)
        
        # Draw player
        player_color = self.color
        if self.collision_flash > 0:
            # Flash red on collision
            flash_intensity = self.collision_flash / 0.2
            player_color = (255, int(255 * (1 - flash_intensity)), 0)
        
        pygame.draw.rect(surface, player_color, player_rect)
        pygame.draw.rect(surface, GOLD, player_rect, 2)  # Gold border


# === MAZE LAYOUT ===

maze_layout = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Create wall rectangles from the maze layout
wall_rectangles = []
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        if maze_layout[row][col] == 1:
            wall_rect = pygame.Rect(
                MAZE_OFFSET_X + col * CELL_SIZE,
                MAZE_OFFSET_Y + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            wall_rectangles.append(wall_rect)


# === INITIALIZE GAME OBJECTS ===

# Initialize button after ensuring button_normal exists
if button_images_loaded:
    start_button = Button(WINDOW_WIDTH // 2 - button_normal.get_width() // 2, WINDOW_HEIGHT - 300)
else:
    start_button = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 300)  # Default position

player = Player(MAZE_OFFSET_X + CELL_SIZE + 5, MAZE_OFFSET_Y + CELL_SIZE + 5)
game_state = TITLE_SCREEN


# === DRAWING FUNCTIONS ===

def draw_title_screen():
    """Draw the title screen."""
    screen.fill(BACKGROUND_COLOR)
    
    # Draw logo
    logo_rect = logo_image.get_rect(center=(WINDOW_WIDTH // 2, 290))
    screen.blit(logo_image, logo_rect)
    
    # Draw instructions
    instruction_text = "Use WASD or Arrow Keys to move"
    instruction_surface = instruction_font.render(instruction_text, True, WHITE)
    instruction_rect = instruction_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
    screen.blit(instruction_surface, instruction_rect)
    
    # Draw button
    if start_button:
        start_button.draw(screen)


def draw_game_screen():
    """Draw the main game screen."""
    screen.fill(BACKGROUND_COLOR)
    
    # Draw maze background
    maze_bg_rect = pygame.Rect(MAZE_OFFSET_X, MAZE_OFFSET_Y, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
    pygame.draw.rect(screen, PATH_COLOR, maze_bg_rect)
    
    # Draw walls
    for wall in wall_rectangles:
        # Check if this wall should flash (collision effect)
        wall_color = WALL_COLOR
        if player.collision_flash > 0:
            player_rect = player.get_rect()
            if wall.colliderect(player_rect.inflate(10, 10)):  # Check nearby walls
                flash_intensity = player.collision_flash / 0.2
                wall_color = (
                    int(WALL_COLOR[0] + (WALL_COLLISION_COLOR[0] - WALL_COLOR[0]) * flash_intensity),
                    int(WALL_COLOR[1] + (WALL_COLLISION_COLOR[1] - WALL_COLOR[1]) * flash_intensity),
                    int(WALL_COLOR[2] + (WALL_COLLISION_COLOR[2] - WALL_COLOR[2]) * flash_intensity)
                )
        
        pygame.draw.rect(screen, wall_color, wall)
        pygame.draw.rect(screen, GOLD, wall, 1)  # Gold border
    
    # Draw player
    player.draw(screen)
    
    # Draw game title
    game_title = subtitle_font.render("Ancient Labyrinth", True, GOLD)
    game_title_rect = game_title.get_rect(center=(WINDOW_WIDTH // 2, 30))
    screen.blit(game_title, game_title_rect)
    
    # Draw instructions
    instruction_text = "Move with WASD or Arrow Keys | ESC to return to title"
    instruction_surface = instruction_font.render(instruction_text, True, WHITE)
    instruction_rect = instruction_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 8))
    screen.blit(instruction_surface, instruction_rect)


# === MAIN GAME LOOP ===

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    mouse_pos = pygame.mouse.get_pos()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == TITLE_SCREEN and start_button and start_button.is_clicked(mouse_pos):
                game_state = GAME_PLAYING
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                if button_click_sound:
                    button_click_sound.play()
                if music_loaded:
                    pygame.mixer.music.play(-1)  # Loop background music
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_state == GAME_PLAYING:
                game_state = TITLE_SCREEN
                pygame.mixer.music.stop()
    
    # Update
    if game_state == TITLE_SCREEN:
        if start_button:
            start_button.check_hover(mouse_pos)
            start_button.update(dt)
    
    elif game_state == GAME_PLAYING:
        # Get movement input
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(
            (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a]),
            (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        )
        
        # Move player
        player.move(direction, dt, wall_rectangles)
        player.update(dt)
    
    # Rendering
    if game_state == TITLE_SCREEN:
        draw_title_screen()
    elif game_state == GAME_PLAYING:
        draw_game_screen()
    
    pygame.display.flip()

# Cleanup
pygame.quit()
sys.exit()