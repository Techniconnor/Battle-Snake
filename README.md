# Battle Snake

A simple Python-based snake battle game using `pygame`.

## Overview

This project includes the following files:

- `main.py` — game entry point and main loop
- `game.py` — game state, rules, and round handling
- `rendering.py` — drawing the game board and UI
- `enemy_ai.py` — enemy snake logic
- `constants.py` — game settings and key constants

## Requirements

- Python 3.12 or later
- `pygame` 2.6.1

## Setup

1. Clone the repository:

```powershell
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

2. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install pygame
```

## Run the game

From the project folder:

```powershell
python main.py
```

If the virtual environment is active, you can also run:

```powershell
.\venv\Scripts\python.exe main.py
```

## Controls

- `1` — Player vs Enemy
- `2` — Player vs Player
- `3` — Computer vs Computer
- `R` — Restart round (after game over or match over)
- `M` — Return to menu (after match over)
- `W`, `A`, `S`, `D` — Player movement
- Arrow keys — Second player movement in Player vs Player mode
