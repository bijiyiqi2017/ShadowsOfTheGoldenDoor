import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (34, 34, 34)  # Dark gray
FPS = 60

# Colors
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

# Game states
TITLE_SCREEN = "title"
GAME_PLAYING = "playing"

# Display window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shadows of the Golden Door")

# Clock for controlling frame rate and delta time
clock = pygame.time.Clock()

# Fonts
subtitle_font = pygame.font.Font(None, 36)
instruction_font = pygame.font.Font(None, 24)

# Load logo image
try:
    logo_image = pygame.image.load('assets/logo/SH logo.png')
    logo_width = 800
    logo_height = int(logo_image.get_height() * (logo_width / logo_image.get_width()))
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    logo_loaded = True
except (pygame.error, FileNotFoundError):
    logo_loaded = False
    print("Warning: Could not load assets/logo/SH logo.png")

# Load button images
try:
    button_normal = pygame.image.load('assets/button/start_button.png')
    button_hover = pygame.image.load('assets/button/start_button_hover.png')
    button_images_loaded = True
    print(f"Button images loaded successfully")
    print(f"Button size: {button_normal.get_width()}x{button_normal.get_height()}")
except (pygame.error, FileNotFoundError) as e:
    button_images_loaded = False
    print(f"Warning: Could not load button images. Error: {e}")

# Button class
class Button:
    def __init__(self, x, y, clickable_area=None):
        if button_images_loaded:
            self.normal_image = button_normal
            self.hover_image = button_hover
            self.rect = self.normal_image.get_rect(topleft=(x, y))
            # Use full button rect for clicking
            self.clickable_rect = self.rect
        self.hovered = False
    
    def draw(self, surface):
        if button_images_loaded:
            image = self.hover_image if self.hovered else self.normal_image
            surface.blit(image, self.rect)
    
    def check_hover(self, pos):
        was_hovered = self.hovered
        self.hovered = self.clickable_rect.collidepoint(pos)
        
        # Change cursor to hand when hovering over button
        if self.hovered and not was_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif not self.hovered and was_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def is_clicked(self, pos):
        return self.clickable_rect.collidepoint(pos)

# Player properties
player_width = 50
player_height = 50
player_color = (255, 255, 0)  # Yellow
player_speed = 300  # Pixels per second

# Player initial position using a Vector2 for float precision
player_pos = pygame.math.Vector2(
    WINDOW_WIDTH / 2 - player_width / 2,
    WINDOW_HEIGHT / 2 - player_height / 2
)

# Initialize game objects
# Button positioned at bottom center of screen
# Button will use its actual PNG dimensions
start_button = Button(WINDOW_WIDTH // 2 - button_normal.get_width() // 2, WINDOW_HEIGHT - 300, None) if button_images_loaded else None
game_state = TITLE_SCREEN

def draw_title_screen():
    """Draw the title screen"""
    # First, fill the background
    screen.fill(BACKGROUND_COLOR)
    
    # Then draw logo if loaded
    if logo_loaded:
        logo_rect = logo_image.get_rect(center=(WINDOW_WIDTH // 2, 290))
        screen.blit(logo_image, logo_rect)
    
    # Draw instructions
    instruction_text = "Use WASD or Arrow Keys to move"
    instruction_surface = instruction_font.render(instruction_text, True, WHITE)
    instruction_rect = instruction_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
    screen.blit(instruction_surface, instruction_rect)
    
    # Draw the button LAST so it appears on top
    if start_button:
        start_button.draw(screen)

def draw_game_screen():
    """Draw the main game screen"""
    screen.fill(BACKGROUND_COLOR)
    
    # Draw a simple maze border
    pygame.draw.rect(screen, GOLD, (50, 50, WINDOW_WIDTH - 100, WINDOW_HEIGHT - 100), 3)
    
    # Create a Rect from the float-based player_pos for rendering
    player_rect = pygame.Rect(round(player_pos.x), round(player_pos.y), player_width, player_height)
    pygame.draw.rect(screen, player_color, player_rect)
    
    # Draw game title at top
    game_title = subtitle_font.render("Ancient Labyrinth", True, GOLD)
    game_title_rect = game_title.get_rect(center=(WINDOW_WIDTH // 2, 30))
    screen.blit(game_title, game_title_rect)
    
    # Draw instructions
    instruction_text = "Move with WASD or Arrow Keys | ESC to return to title"
    instruction_surface = instruction_font.render(instruction_text, True, WHITE)
    instruction_rect = instruction_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
    screen.blit(instruction_surface, instruction_rect)

# Game loop
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
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Reset cursor
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_state == GAME_PLAYING:
                game_state = TITLE_SCREEN
    
    # Update
    if game_state == TITLE_SCREEN:
        if start_button:
            start_button.check_hover(mouse_pos)
    elif game_state == GAME_PLAYING:
        # Get state of all keys currently pressed
        keys = pygame.key.get_pressed()
        
        # Calculate movement direction vector
        direction = pygame.math.Vector2(
            (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a]),
            (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        )
        
        # Normalize the direction vector to ensure consistent speed
        if direction.length_squared() > 0:
            direction.normalize_ip()
        
        # Update player position based on speed, direction, and delta time
        player_pos += direction * player_speed * dt
        
        # Implement boundary detection (clamping)
        player_pos.x = max(0, min(player_pos.x, WINDOW_WIDTH - player_width))
        player_pos.y = max(0, min(player_pos.y, WINDOW_HEIGHT - player_height))
    
    # Rendering
    if game_state == TITLE_SCREEN:
        draw_title_screen()
    elif game_state == GAME_PLAYING:
        draw_game_screen()
    
    # Update the display
    pygame.display.flip()

# Quit Pygame and exit the program
pygame.quit()
sys.exit()