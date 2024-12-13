import pygame
from pygame import Rect

pygame.init()

# ---------------Constants------------------
SCREEN_W = 1000  # Width
SCREEN_H = 600  # Height
FPS = 60  # Frames per second

CH_WIDTH = 300
CH_HEIGHT = 300
CH_SPEED = 300  # Pixels per second
HURT_DURATION = 1.0

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Game Window")


def load_sprite_sheet(path, frame_count, frame_width, frame_height):
    sprite_sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for i in range(frame_count):
        frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (CH_WIDTH, CH_HEIGHT))
        frames.append(frame)
    return frames


def draw_window():
    screen.fill(WHITE)


def draw_sPlayer(x, y, frame, facing_left):
    if facing_left:
        frame = pygame.transform.flip(frame, True, False)
    screen.blit(frame, (x, y))


def draw_sDummy(x, y, frame, facing_left):
    # If you want the dummy to face a particular direction, control it here.
    # For now, we won't flip to avoid confusion:
    # frame = pygame.transform.flip(frame, True, False)  # Remove flipping if not desired
    screen.blit(frame, (x, y))


def main():
    run = True
    clock = pygame.time.Clock()

    player_x, player_y = 0, SCREEN_H - CH_HEIGHT
    facing_left = False
    is_moving = False
    is_attacking = False
    attack_timer = 0

    dummy_x, dummy_y = SCREEN_W - CH_WIDTH, SCREEN_H - CH_HEIGHT
    dummy_state = "idle"
    dummy_hurt_timer = 0

    try:
        dummy_idle_frames = load_sprite_sheet("assets/Dummy/Idle.png", 6, 128, 128)
        dummy_hurt_frames = load_sprite_sheet("assets/Dummy/Hurt.png", 3, 128, 128)
        run_frames = load_sprite_sheet("assets/Samurai/Run.png", 8, 128, 128)
        idle_frames = load_sprite_sheet("assets/Samurai/Idle.png", 4, 128, 128)
        attack_1_frames = load_sprite_sheet("assets/Samurai/Attack_1.png", 6, 128, 128)
        attack_2_frames = load_sprite_sheet("assets/Samurai/Attack_2.png", 4, 128, 128)
        attack_3_frames = load_sprite_sheet("assets/Samurai/Attack_3.png", 3, 128, 128)
    except pygame.error as e:
        print(f"Error loading sprite sheet: {e}")
        return

    current_frame = 0
    animation_timer = 0
    animation_speed = 0.1
    current_player_animation = idle_frames

    current_dummy_frame = 0
    dummy_animation_timer = 0
    dummy_animation_speed = 0.1
    current_dummy_animation = dummy_idle_frames

    while run:
        delta_time = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and not is_attacking:
                if event.key == pygame.K_j:
                    current_player_animation = attack_1_frames
                    is_attacking = True
                    attack_timer = 0
                    current_frame = 0
                elif event.key == pygame.K_k:
                    current_player_animation = attack_2_frames
                    is_attacking = True
                    attack_timer = 0
                    current_frame = 0
                elif event.key == pygame.K_l:
                    current_player_animation = attack_3_frames
                    is_attacking = True
                    attack_timer = 0
                    current_frame = 0

        # Update Dummy Animation
        dummy_animation_timer += delta_time
        if dummy_animation_timer >= dummy_animation_speed:
            dummy_animation_timer = 0
            current_dummy_frame = (current_dummy_frame + 1) % len(current_dummy_animation)

        # Update Player Animation
        if is_attacking:
            attack_timer += delta_time
            animation_timer += delta_time
            if animation_timer >= animation_speed:
                animation_timer = 0
                current_frame = (current_frame + 1) % len(current_player_animation)

            # Check if attack animation is complete
            if attack_timer >= len(current_player_animation) * animation_speed:
                is_attacking = False
                current_player_animation = idle_frames
                current_frame = 0

        elif is_moving:
            if current_player_animation != run_frames:
                current_frame = 0
            current_player_animation = run_frames

            animation_timer += delta_time
            if animation_timer >= animation_speed:
                animation_timer = 0
                current_frame = (current_frame + 1) % len(run_frames)
        else:
            if current_player_animation != idle_frames:
                current_frame = 0
            current_player_animation = idle_frames

            animation_timer += delta_time
            if animation_timer >= animation_speed:
                animation_timer = 0
                current_frame = (current_frame + 1) % len(idle_frames)

        # Player Movement
        if not is_attacking:
            keys = pygame.key.get_pressed()
            is_moving = False
            if keys[pygame.K_d] and player_x < SCREEN_W - CH_WIDTH:
                player_x += CH_SPEED * delta_time
                is_moving = True
                facing_left = False
            if keys[pygame.K_a] and player_x > 0:
                player_x -= CH_SPEED * delta_time
                is_moving = True
                facing_left = True

        # Collision Check
        # Define the sword's attack hit box ONLY if attacking
        if is_attacking:
            if facing_left:
                attack_hitbox = pygame.Rect(player_x - 50, player_y + 100, 50, 100)
            else:
                attack_hitbox = pygame.Rect(player_x + CH_WIDTH, player_y + 100, 50, 100)

            dummy_rect = pygame.Rect(dummy_x, dummy_y, CH_WIDTH, CH_HEIGHT)

            if dummy_state == "idle" and attack_hitbox.colliderect(dummy_rect):
                dummy_state = "hurt"
                current_dummy_animation = dummy_hurt_frames
                dummy_hurt_timer = 0
                current_dummy_frame = 0

        # Manage Dummy State (MOVED OUTSIDE of is_attacking block)
        if dummy_state == "hurt":
            dummy_hurt_timer += delta_time
            if dummy_hurt_timer >= HURT_DURATION:
                dummy_state = "idle"
                current_dummy_animation = dummy_idle_frames
                current_dummy_frame = 0

        # Redraw
        draw_window()
        draw_sPlayer(player_x, player_y, current_player_animation[current_frame], facing_left)
        draw_sDummy(dummy_x, dummy_y, current_dummy_animation[current_dummy_frame], facing_left)
        # Debug rectangle for attack hitbox (only when attacking)
        if is_attacking:
            pygame.draw.rect(screen, (255, 0, 0, 100), attack_hitbox, 2)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
