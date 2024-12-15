# Sprite Manipulation and Animation with Pygame

This project is a learning exercise focused on manipulating and animating sprites using **Pygame**, a Python library for game development. The project uses free sprites sourced from **[Craftpix.net](https://craftpix.net/)** to demonstrate basic techniques in sprite animation, movement, and attack implementation.

---

## Features

- **Smooth Character Movement**: The character can move left and right across the screen, with directional animations.
- **Idle and Running Animations**: The sprite switches between idle and running states based on player input.
- **Attack Animations**: Three unique attack animations (`Attack_1`, `Attack_2`, `Attack_3`) triggered using the `J`, `K`, and `L` keys.
- **Directional Facing**: The character's sprite flips horizontally based on movement direction.
- **Frame-by-Frame Animation**: Demonstrates handling multiple animation states and transitioning between them.

---

## Getting Started

### Prerequisites

- Python
- Pygame

1. Install dependencies:

pip install pygame

2. Run the project:

python3 main.py

## Controls

### Functional commands
- **Move Left**: `A`
- **Move Right**: `D`
- **Attack 1**: `J`
- **Attack 2**: `K`
- **Attack 3**: `L`
### To be made
- **Jump**: 'W'
- **Force slow walk**: 'S'
- **Parry/Block**: 'Spacebar'

## Project Structure

```plaintext
├── assets/
|   ├── Dummy/
|   │   ├── Idle.png         # Idle animation of a dummy (4 frames)
│   │   ├── Hurt.png         # Hurt animation after rect collision (3 frames)
│   ├── Samurai/
│   │   ├── Run.png          # Running animation (8 frames)
│   │   ├── Idle.png         # Idle animation (4 frames)
│   │   ├── Attack_1.png     # Attack 1 animation (6 frames)
│   │   ├── Attack_2.png     # Attack 2 animation (4 frames)
│   │   ├── Attack_3.png     # Attack 3 animation (4 frames)
├── main.py                  # Main project file
├── README.md                # Project documentation
```

## Learning Objectives

This project is designed for beginners who want to:
- Learn how to load and manipulate sprite sheets.
- Understand how to animate sprites frame by frame.
- Gain experience handling user input for movement and actions.
- Implement and manage transitions between various animation states like idle, running, and attacking.
- Experiment with directional sprite flipping for movement.

---

## Credits

- **Sprites**: Free assets sourced from [Craftpix.net](https://craftpix.net/).
- **Framework**: Built with [Pygame](https://www.pygame.org/).

---

## License

This project is for educational purposes. The sprite assets belong to [Craftpix.net](https://craftpix.net/) and are subject to their terms of use.
