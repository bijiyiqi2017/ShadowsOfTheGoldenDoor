# Shadows of the Golden Door

## Game Story

You are Alex, a curious adventurer who has ventured into the Ancient Labyrinth, a mysterious maze said to be filled with treasure and secrets. However, the maze is not just a place of riches – it's also a place of danger, with twisting corridors, hidden traps, and locked doors.

The only way out is through the Golden Door – but it is locked. To escape the maze, you must collect 3 Lost Keys hidden throughout the maze. Each key unlocks a new part of the labyrinth, and ultimately, the Golden Door will open, allowing you to escape.

As you navigate the maze, you will face:
- Dangerous traps that can hurt you if you're not careful
- Locked doors that require keys to open
- Hidden secrets that will help you on your journey

Will you find all the keys and escape the maze, or will you get lost forever?

Here is an 8 image Storyboard to illustrate a desired direction and end results for our game. This image is a placeholder and will be updated as the project proceeds.

![image](https://github.com/user-attachments/assets/c9d56d78-1127-470f-8e84-2645333466bb)

---

## Setup Guide

This guide will help you set up your development environment to run and contribute to "Shadows of the Golden Door".

### Prerequisites

Before you begin, you'll need to have Python 3.x installed on your system.

---

## Step 1: Install Python

### Windows

1. Visit the official Python website: [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3.x installer for Windows
3. Run the installer
   - **Important**: Check the box "Add Python to PATH" during installation
4. Click "Install Now"
5. Verify the installation by opening Command Prompt and typing:
   ```bash
   python --version
   ```
   You should see something like `Python 3.11.x`

### macOS

1. **Option A: Using the Official Installer**
   - Visit [python.org/downloads](https://www.python.org/downloads/)
   - Download the latest Python 3.x installer for macOS
   - Run the `.pkg` file and follow the installation wizard

2. **Option B: Using Homebrew** (Recommended)
   - If you have Homebrew installed, open Terminal and run:
     ```bash
     brew install python3
     ```

3. Verify the installation:
   ```bash
   python3 --version
   ```
   You should see something like `Python 3.11.x`

### Linux

Most Linux distributions come with Python pre-installed. If not:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

Verify the installation:
```bash
python3 --version
```

---

## Step 2: Install Pygame

Once Python is installed, you can install Pygame using pip (Python's package manager).

### All Operating Systems

Open your terminal or command prompt and run:

```bash
pip install pygame
```

**For macOS/Linux users**, you might need to use `pip3`:
```bash
pip3 install pygame
```

### Verify Pygame Installation

Test that Pygame is installed correctly by running the built-in aliens example:

```bash
python -m pygame.examples.aliens
```

If a game window opens with aliens, Pygame is installed correctly!

---

## Step 3: Set Up a Virtual Environment (Recommended)

A virtual environment keeps your project dependencies isolated from other Python projects.

### Creating a Virtual Environment

**Windows:**
```bash
# Navigate to your project directory
cd path\to\ShadowsOfTheGoldenDoor

# Create virtual environment
python -m venv venv
```

**macOS/Linux:**
```bash
# Navigate to your project directory
cd path/to/ShadowsOfTheGoldenDoor

# Create virtual environment
python3 -m venv venv
```

### Activating the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

When activated, you should see `(venv)` at the beginning of your command prompt.

### Installing Dependencies in Virtual Environment

With the virtual environment activated, install Pygame:

```bash
pip install pygame
```

### Deactivating the Virtual Environment

When you're done working on the project:

```bash
deactivate
```

---

## Step 4: Verify Your Setup

Let's make sure everything is working correctly!

### Clone the Repository

If you haven't already:

```bash
git clone https://github.com/bijiyiqi2017/ShadowsOfTheGoldenDoor.git
cd ShadowsOfTheGoldenDoor
```

### Run the Game

1. Activate your virtual environment (if using one)
2. Run the game:

```bash
python main.py
```

If a game window opens with the title "Shadows of the Golden Door", congratulations! Your setup is complete!

---

## Troubleshooting

### "python is not recognized" (Windows)
- Python wasn't added to PATH during installation
- Reinstall Python and check "Add Python to PATH"
- Or manually add Python to your system's PATH environment variable

### "pip: command not found"
- Try using `python -m pip` instead of just `pip`
- On macOS/Linux, try `pip3` instead of `pip`

### Pygame won't install
- Make sure you have the latest pip: `pip install --upgrade pip`
- On Linux, you might need additional dependencies:
  ```bash
  sudo apt-get install python3-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev
  ```

### Permission errors on macOS/Linux
- Use `pip3 install --user pygame` to install for your user only
- Or use a virtual environment (recommended)

---

## Contributor All Time Leaderboard 

### (Contributions tracked from the project's inception, to be updated periodically)

This leaderboard highlights contributors based on the number of merged pull requests and their contributions to the project.

| Rank | Contributor          | Merged PRs | Notes                               |
|------|----------------------|------------|-------------------------------------|
| 1    | **@HirulaAbesignha** | 6          | Enhanced Game Experience, Maze Layout, Title Screen, Setup Guide, etc. |
| 2    | @shanaya-Gupta       | 1          | Basic Player Movement               |
| 3    | @adnan-47            | 1          | Setup Guide Documentation           |


---

## Contributing

Now that your environment is set up, you're ready to contribute! Check out our [Issues](https://github.com/bijiyiqi2017/ShadowsOfTheGoldenDoor/issues) page for tasks you can help with.

### Quick Start for Contributors

1. Fork this repository
2. Clone your fork
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Commit: `git commit -m "feat: description of your changes"`
6. Push: `git push origin feature/your-feature-name`
7. Open a Pull Request

---

## Additional Resources

- [Python Official Documentation](https://docs.python.org/3/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)

---

## License

- [License](https://github.com/HirulaAbesignha/ShadowsOfTheGoldenDoor/blob/main/LICENSE)

---

Good luck on your adventure through the Ancient Labyrinth!

