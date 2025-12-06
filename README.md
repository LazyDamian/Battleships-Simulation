# Battleship Game (Schiffe Versenken)

This project is a Python implementation of the classic Battleship game ("Schiffe versenken").  
Ships of different lengths are randomly placed on a 10×10 game board while ensuring they do not touch each other.  
The logic includes collision checks, spacing rules, and randomized placement using NumPy.

---

## 🚀 Features
- Random ship placement on a 10×10 grid  
- Ships do not overlap and do not touch (1-cell safety margin)  
- Configurable ship lengths and quantities  
- Uses NumPy for efficient computations  
- Easily extendable for full game logic (shooting, scoring, GUI, etc.)

---

## 📦 Dependencies

The project uses the following Python packages (stored in `requirements.txt`):

numpy==2.3.5
pandas==2.3.3
python-dateutil==2.9.0.post0
pytz==2025.2
six==1.17.0
tzdata==2025.2

👉 **Only NumPy is required for the Battleship logic**,  
but the other packages may be used by other project modules.

---

## 🛠 Installation

Make sure you have Python 3 installed.

Install all required dependencies:

```bash
pip install -r requirements.txt
Alternatively, install manually what you need:

pip install numpy
Run the main script:

python spielaufbau.py


This will generate a 10×10 game board with randomly placed ships.
pythonproject0/
│
├── src/                # (optional) main source files
├── tests/              # test scripts
├── spielaufbau.py      # main Battleship placement logic
├── requirements.txt    # dependencies
└── README.md           # project documentation
Future Improvements

-Add a shooting mechanic (hit/miss)

-Track game state and score

-Add Matplotlib visualization of the board

-Implement full player vs AI gameplay

-Add a GUI using Tkinter or PyGame
