import pygame

# Initializes all important modules (audio, events, display...)
pygame.init()

# ---------------Constants------------------
SCREEN_W = 1000  # Width
SCREEN_H = 600  # Height
FPS = 60  # Frames per second

# Player Properties
PLAYER_WIDTH = 300
PLAYER_HEIGHT = 300
PLAYER_SPEED = 300  # Pixels per second

# Colors
WHITE = (255, 255, 255)

# Screen Setup
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Game Window")
# ---------------Until here-----------------


def load_sprite_sheet(path, frame_count, frame_width, frame_height):
    """
    Loads frames from a sprite sheet.
    :param path: Path to the sprite sheet image.
    :param frame_count: Number of frames in the sprite sheet.
    :param frame_width: Width of each frame.
    :param frame_height: Height of each frame.
    :return: List of frames as surfaces.
    """
    sprite_sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for i in range(frame_count):
        # Extract each frame using subsurface
        frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT))  # Scale frame
        frames.append(frame)
    return frames


def draw_window():
    """
    Clears the screen with a white background.
    """
    screen.fill(WHITE)


def draw_sPlayer(x, y, frame, facing_left):
    """
    Draws the player animation frame at the specified position.
    Flips the frame if facing left.
    """
    if facing_left:
        frame = pygame.transform.flip(frame, True, False)  # Flip horizontally
    screen.blit(frame, (x, y))


def main():

    run = True
    clock = pygame.time.Clock()

    # Local Variables here for the cords of the player
    player_x, player_y = 0, SCREEN_H - PLAYER_HEIGHT
    facing_left = False  # Tracks which direction the player is facing
    is_moving = False  # Tracks whether the player is moving
    is_attacking = False  # Tracks whether the player is attacking
    attack_timer = 0  # Timer to control attack duration
    current_attack = None  # Tracks which attack animation is playing

    # Load frames from the sprite sheets
    try:
        run_frames = load_sprite_sheet("assets/Samurai/Run.png", 8, 128, 128)  # Running animation
        idle_frames = load_sprite_sheet("assets/Samurai/Idle.png", 4, 128, 128)  # Idle animation
        attack_1_frames = load_sprite_sheet("assets/Samurai/Attack_1.png", 6, 128, 128)  # Attack 1
        attack_2_frames = load_sprite_sheet("assets/Samurai/Attack_2.png", 4, 128, 128)  # Attack 2
        attack_3_frames = load_sprite_sheet("assets/Samurai/Attack_3.png", 3, 128, 128)  # Attack 3
    except pygame.error as e:
        print(f"Error loading sprite sheet: {e}")
        return

    # Animation Variables
    current_frame = 0
    animation_timer = 0  # Timer to control animation speed
    animation_speed = 0.1  # Seconds per frame
    current_animation = idle_frames  # Default to idle animation

    while run:

        delta_time = clock.tick(FPS) / 1000  # Time since last frame in seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and not is_attacking:
                if event.key == pygame.K_j:
                    current_animation = attack_1_frames
                    is_attacking = True
                    attack_timer = 0  # Reset attack timer
                    current_frame = 0  # Start attack animation from first frame
                    print("Attack 1 triggered!")
                elif event.key == pygame.K_k:
                    current_animation = attack_2_frames
                    is_attacking = True
                    attack_timer = 0
                    current_frame = 0
                    print("Attack 2 triggered!")
                elif event.key == pygame.K_l:
                    current_animation = attack_3_frames
                    is_attacking = True
                    attack_timer = 0
                    current_frame = 0
                    print("Attack 3 triggered!")

        # Update Animation
        if is_attacking:
            attack_timer += delta_time
            animation_timer += delta_time
            if animation_timer >= animation_speed:
                animation_timer = 0
                current_frame = (current_frame + 1) % len(current_animation)

            # Check if attack animation is complete
            if attack_timer >= len(current_animation) * animation_speed:
                is_attacking = False  # End attack
                current_animation = idle_frames  # Return to idle animation
                current_frame = 0  # Reset to idle frame

        elif is_moving:
            if current_animation != run_frames:
                current_frame = 0  # Reset to the first frame
            current_animation = run_frames

            animation_timer += delta_time
            if animation_timer >= animation_speed:
                animation_timer = 0
                current_frame = (current_frame + 1) % len(run_frames)  # Cycle through run frames

        else:
            if current_animation != idle_frames:
                current_frame = 0  # Reset to the first frame
            current_animation = idle_frames

            animation_timer += delta_time
            if animation_timer >= animation_speed:
                animation_timer = 0
                current_frame = (current_frame + 1) % len(idle_frames)  # Cycle through idle frames

        # Player Movement
        if not is_attacking:  # Disable movement during attack
            keys = pygame.key.get_pressed()
            is_moving = False  # Reset movement flag
            if keys[pygame.K_d] and player_x < SCREEN_W - PLAYER_WIDTH:
                player_x += PLAYER_SPEED * delta_time
                is_moving = True
                facing_left = False  # Face right
            if keys[pygame.K_a] and player_x > 0:
                player_x -= PLAYER_SPEED * delta_time
                is_moving = True
                facing_left = True  # Face left

        # Redraw
        draw_window()
        draw_sPlayer(player_x, player_y, current_animation[current_frame], facing_left)
        pygame.display.update()  # Update the screen

    pygame.quit()

if __name__ == "__main__":
    main()