import pygame
import sys

# initialize pygame
pygame.init()

# constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (34, 34, 34)  # dark gray
FPS = 60

# colors
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
WALL_COLOR = (100, 80, 60)  # brownish color for walls
PATH_COLOR = (50, 50, 50)  # darker gray for paths

# maze configuration
GRID_SIZE = 10
CELL_SIZE = 50  # each cell is 50x50 pixels
MAZE_OFFSET_X = (WINDOW_WIDTH - (GRID_SIZE * CELL_SIZE)) // 2
MAZE_OFFSET_Y = 80  # offset from top to leave room for title

# game states
TITLE_SCREEN = "title"
GAME_PLAYING = "playing"

# display window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shadows of the Golden Door")

# clock for controlling frame rate and delta time
clock = pygame.time.Clock()

# fonts
subtitle_font = pygame.font.Font(None, 36)
instruction_font = pygame.font.Font(None, 24)

# load logo image
try:
    logo_image = pygame.image.load('assets/logo/SH logo.png')
    logo_width = 800
    logo_height = int(logo_image.get_height() * (logo_width / logo_image.get_width()))
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    logo_loaded = True
except (pygame.error, FileNotFoundError):
    logo_loaded = False
    print("Warning: Could not load assets/logo/SH logo.png")

# load button images
try:
    button_normal = pygame.image.load('assets/button/start_button.png')
    button_hover = pygame.image.load('assets/button/start_button_hover.png')
    button_images_loaded = True
    print(f"Button images loaded successfully")
    print(f"Button size: {button_normal.get_width()}x{button_normal.get_height()}")
except (pygame.error, FileNotFoundError) as e:
    button_images_loaded = False
    print(f"Warning: Could not load button images. Error: {e}")

# button class
class Button:
    def __init__(self, x, y, clickable_area=None):
        if button_images_loaded:
            self.normal_image = button_normal
            self.hover_image = button_hover
            self.rect = self.normal_image.get_rect(topleft=(x, y))
            # use full button rect for clicking
            self.clickable_rect = self.rect
        self.hovered = False
    
    def draw(self, surface):
        if button_images_loaded:
            image = self.hover_image if self.hovered else self.normal_image
            surface.blit(image, self.rect)
    
    def check_hover(self, pos):
        was_hovered = self.hovered
        self.hovered = self.clickable_rect.collidepoint(pos)
        
        # change cursor to hand when hovering over button
        if self.hovered and not was_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif not self.hovered and was_hovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def is_clicked(self, pos):
        return self.clickable_rect.collidepoint(pos)

# player properties
player_width = 40  # made slightly smaller to fit better in cells
player_height = 40
player_color = (255, 255, 0)  # yellow
player_speed = 200  # slowed down a bit for better maze navigation

# player initial position - start at top left of maze
player_pos = pygame.math.Vector2(
    MAZE_OFFSET_X + CELL_SIZE + 5,  # start in second column with some padding
    MAZE_OFFSET_Y + CELL_SIZE + 5   # start in second row with some padding
)

# simple 10x10 maze layout
# 1 = wall, 0 = path
# keeping it simple with a basic layout that has some corridors
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

# create wall rectangles from the maze layout
wall_rects = []
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        if maze_layout[row][col] == 1:
            wall_rect = pygame.Rect(
                MAZE_OFFSET_X + col * CELL_SIZE,
                MAZE_OFFSET_Y + row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            wall_rects.append(wall_rect)

# initialize game objects
# button positioned at bottom center of screen
# button will use its actual png dimensions
start_button = Button(WINDOW_WIDTH // 2 - button_normal.get_width() // 2, WINDOW_HEIGHT - 300, None) if button_images_loaded else None
game_state = TITLE_SCREEN

def draw_title_screen():
    """draw the title screen"""
    # first, fill the background
    screen.fill(BACKGROUND_COLOR)
    
    # then draw logo if loaded
    if logo_loaded:
        logo_rect = logo_image.get_rect(center=(WINDOW_WIDTH // 2, 290))
        screen.blit(logo_image, logo_rect)
    
    # draw instructions
    instruction_text = "Use WASD or Arrow Keys to move"
    instruction_surface = instruction_font.render(instruction_text, True, WHITE)
    instruction_rect = instruction_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
    screen.blit(instruction_surface, instruction_rect)
    
    # draw the button last so it appears on top
    if start_button:
        start_button.draw(screen)

def draw_game_screen():
    """draw the main game screen"""
    screen.fill(BACKGROUND_COLOR)
    
    # draw the maze background first
    maze_bg_rect = pygame.Rect(
        MAZE_OFFSET_X, 
        MAZE_OFFSET_Y, 
        GRID_SIZE * CELL_SIZE, 
        GRID_SIZE * CELL_SIZE
    )
    pygame.draw.rect(screen, PATH_COLOR, maze_bg_rect)
    
    # draw all the walls
    for wall in wall_rects:
        pygame.draw.rect(screen, WALL_COLOR, wall)
        # add a subtle border to each wall for better visibility
        pygame.draw.rect(screen, GOLD, wall, 1)
    
    # draw the player
    player_rect = pygame.Rect(round(player_pos.x), round(player_pos.y), player_width, player_height)
    pygame.draw.rect(screen, player_color, player_rect)
    
    # draw game title at top
    game_title = subtitle_font.render("Ancient Labyrinth", True, GOLD)
    game_title_rect = game_title.get_rect(center=(WINDOW_WIDTH // 2, 30))
    screen.blit(game_title, game_title_rect)
    
    # draw instructions
    instruction_text = "Move with WASD or Arrow Keys | ESC to return to title"
    instruction_surface = instruction_font.render(instruction_text, True, WHITE)
    instruction_rect = instruction_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 8))
    screen.blit(instruction_surface, instruction_rect)

# game loop
running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    mouse_pos = pygame.mouse.get_pos()
    
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == TITLE_SCREEN and start_button and start_button.is_clicked(mouse_pos):
                game_state = GAME_PLAYING
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # reset cursor
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_state == GAME_PLAYING:
                game_state = TITLE_SCREEN
    
    # update
    if game_state == TITLE_SCREEN:
        if start_button:
            start_button.check_hover(mouse_pos)
    elif game_state == GAME_PLAYING:
        # get state of all keys currently pressed
        keys = pygame.key.get_pressed()
        
        # calculate movement direction vector
        direction = pygame.math.Vector2(
            (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a]),
            (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        )
        
        # normalize the direction vector to ensure consistent speed
        if direction.length_squared() > 0:
            direction.normalize_ip()
        
        # save old position in case we need to revert
        old_pos = player_pos.copy()
        
        # update player position based on speed, direction, and delta time
        player_pos += direction * player_speed * dt
        
        # create a rect for collision detection
        player_rect = pygame.Rect(round(player_pos.x), round(player_pos.y), player_width, player_height)
        
        # check collision with walls
        collision = False
        for wall in wall_rects:
            if player_rect.colliderect(wall):
                collision = True
                break
        
        # if there's a collision, revert to old position
        if collision:
            player_pos = old_pos
        
        # also keep player within window bounds as a safety measure
        player_pos.x = max(0, min(player_pos.x, WINDOW_WIDTH - player_width))
        player_pos.y = max(0, min(player_pos.y, WINDOW_HEIGHT - player_height))
    
    # rendering
    if game_state == TITLE_SCREEN:
        draw_title_screen()
    elif game_state == GAME_PLAYING:
        draw_game_screen()
    
    # update the display
    pygame.display.flip()

# quit pygame and exit the program
pygame.quit()
sys.exit()