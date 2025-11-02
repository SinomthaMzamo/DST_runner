# 🚀 Space Runner

**Space Runner** is a 2D side-scrolling arcade game built with **Pygame Zero**.  
You play as a space explorer who must jump, slide, and dodge obstacles while collecting coins and racking up points.

---

## 🧰 Libraries Used

| Library | Purpose |
|----------|----------|
| **pgzrun** | Runs the game using the Pygame Zero engine. |
| **random** | Generates randomness for obstacle and coin spawning. |
| **pygame.Rect** | Used for collision detection between the player and obstacles. |
| **os** | Used to centre the game window on the screen. |

---

## 🕹️ Running the Project

### 1️⃣ Install Python
Download and install Python (3.9+ recommended):  
👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

### 2️⃣ Set up a Virtual Environment
In your project directory, run:

```bash
python3 -m venv .venv/
source .venv/bin/activate   # On macOS/Linux
# OR
.venv\Scripts\activate      # On Windows
```
---


### 3️⃣ Install Dependencies

Once the virtual environment is active, install all required libraries:

```bash
pip install -r requirements.txt
```

*(Make sure your `requirements.txt` includes `pgzero` and `pygame`.)*

---

### 4️⃣ Run the Game

You can run **Space Runner** in two ways:

#### Option A — Using Python:

```bash
python3 run_game.py
```

#### Option B — Using Pygame Zero:

```bash
pgzrun run_game.py
```

---

## 🎮 Controls

| Key       | Action                     |
| --------- | -------------------------- |
| **UP**    | Jump                       |
| **DOWN**  | Slide                      |
| **SPACE** | Start / Restart the game   |

---

## 🎵 Sound and Music

* Background music plays throughout gameplay.
* Sound effects trigger for:

  * Jumping
  * Sliding
  * Collisions
  * Collecting coins

---

## 🧑‍💻 Developer Notes

* The game starts in an **idle state** with an animated player.
* A **menu screen** allows toggling **sound**, **music**, and **exit** options.
* Obstacles and coins spawn dynamically with increasing speed as the score grows.

---

## 📁 Project Structure

```
SpaceRunner/
│
├── app/
│   ├── run_game.py              # Entry point
│   ├── game.py                  # Main game logic
│   ├── entities/
│   │   ├── player.py            # Player class and animations
│   │   ├── enemies.py           # Enemy and obstacle logic
│   │   ├── coin.py              # Coin logic and spin animation
│   │   └── entity.py            # Base entity class
│
├── images/                      # Sprite and background images
├── sounds/                      # Sound effects and background music
├── requirements.txt
└── README.md
```

---

Enjoy playing **Space Runner**! 🪐

