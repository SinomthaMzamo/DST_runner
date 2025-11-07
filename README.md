# 🚀 Space Runner

**Space Runner** is a 2D side-scrolling arcade game built with **Pygame Zero**.  
You play as a space explorer who must jump, slide, and dodge obstacles while collecting coins and racking up points.

---

## 🎮 Game Modes

### 🕹️ Arcade Mode
Classic endless runner gameplay! Survive as long as possible, avoid obstacles, collect coins, and set new high scores. The game gets progressively faster and more challenging as your score increases.

### 🎯 Mission Mode
Complete structured challenges with specific goals! Each mission has:
- **Target Score** - Minimum score required to complete the mission
- **Target Balance** - Minimum coins required to complete the mission
- **Score Multiplier Reward** - Unlock permanent score multipliers by completing missions (2.0x, 3.0x, 4.0x, etc.)

Complete missions to unlock the next challenge and build up your multiplier for faster scoring!

---

## 🧰 Libraries Used

| Library | Purpose |
|----------|----------|
| **pgzrun** | Runs the game using the Pygame Zero engine. |
| **random** | Generates randomness for obstacle and coin spawning. |
| **pygame.Rect** | Used for collision detection between the player and obstacles. |
| **os** | Used to centre the game window on the screen. |
| **math** | Used for mission difficulty scaling calculations. |

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
| **UP**    | Jump over obstacles        |
| **DOWN**  | Slide under obstacles      |


---

## 🎯 Gameplay Features

### Obstacles
- **Ground Obstacles** - Volcanic hazards on the ground that must be jumped over
- **Floating Obstacles** - Debris and black holes that move up and down
- **Cloud Platforms** - Land on clouds from above to collect coins, but watch out - you can't jump through them from below!

### Coins & Scoring
- Collect **gold coins** (8 points) that spawn above cloud platforms
- Score increases automatically while playing
- **Score multipliers** earned from missions make you score faster
- Build your **Vault Balance** by collecting coins across all runs

### Difficulty Progression
- Game speed increases every 500 points
- Obstacle spawn rate varies randomly
- Cloud platforms with coins appear more frequently after score 30

### Audio
- **Background Music** - Different tracks for menu, missions, and gameplay
- **Sound Effects** - Jump, slide, collision, coin collection, and win/lose sounds
- Toggle music and sound on/off from the main menu

### UI Features
- **Pause Button** - Pause and resume gameplay at any time
- **Menu Button** - Return to main menu from anywhere
- Real-time score, high score, and balance tracking
- Mission progress indicators

---

## 🎵 Sound and Music

* Background music plays throughout gameplay.
* Sound effects trigger for:
  * Jumping
  * Sliding
  * Collisions (obstacles and cloud platforms)
  * Collecting coins
  * Winning/losing missions

---

## 🧑‍💻 Developer Notes

* The game starts in an **idle state** with an animated player.
* A **menu screen** allows selecting game mode and toggling **sound**, **music**, and **exit** options.
* **Mission system** uses a hybrid exponential-logarithmic growth model for balanced difficulty scaling.
* Obstacles and coins spawn dynamically with increasing speed as the score grows.
* **Cloud collision detection** prevents players from jumping through platforms from below.
* **Score multipliers** persist across game sessions and stack with each completed mission.

---

## 📁 Project Structure

```
app/
├── __init__.py
├── constants.py           # Game configuration and obstacle definitions
├── entities/
│   ├── __init__.py
│   ├── enemies.py        # Obstacle classes and behavior
│   ├── entity.py         # Base entity class
│   ├── player.py         # Player character and states
│   └── rewards.py        # Coin system
├── game.py               # Core game logic and state management
├── mission_classes.py    # Mission system and progression
├── utils.py              # Helper functions for difficulty scaling
├── images/               # Game sprites and graphics
├── music/                # Background music tracks
├── sounds/               # Sound effects
├── ui/
│   ├── buttons.py        # Button creation and layout
│   └── colours.py        # Color definitions
├── .gitignore
├── README.md
├── readme.txt
├── requirements.txt
└── run_game.py          # Main game entry point
```

---

## 🏆 Tips for Success

1. **Arcade Mode**: Focus on survival and high scores. The game gets faster, so perfect your timing!
2. **Mission Mode**: Balance score and coin collection. Don't rush - coins are just as important as points!
3. **Cloud Platforms**: Time your jumps to land on clouds and grab the gold coins above them.
4. **Multipliers**: Complete missions in order to unlock higher multipliers for faster scoring.
5. **Practice**: Use the pause button to take breaks during long runs.

---

Enjoy playing **Space Runner**! 🪐