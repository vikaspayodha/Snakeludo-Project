import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import time

# -----------------------------
# GAME SETTINGS
# -----------------------------
snakes = {99: 54, 70: 55, 52: 42, 25: 2, 95: 72}
ladders = {6: 25, 11: 40, 60: 85, 46: 90, 17: 69}

BOARD_SIZE = 600  # pixels (board will be scaled)
CELL = BOARD_SIZE // 10

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def roll_dice():
    return random.randint(1, 6)

def num_to_xy(num):
    """Convert box number (1–100) to pixel coordinates on board."""
    row = (num - 1) // 10
    col = (num - 1) % 10

    # reverse order every alternate row
    if row % 2 == 1:
        col = 9 - col

    x = col * CELL + CELL // 2
    y = (9 - row) * CELL + CELL // 2
    return x, y

# -----------------------------
# MAIN GAME CLASS
# -----------------------------
class SnakeLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Real Snake & Ladder 🎲")
        self.root.geometry(f"{BOARD_SIZE + 200}x{BOARD_SIZE}")
        self.root.resizable(False, False)

        # Load board image
        img = Image.open("board.png").resize((BOARD_SIZE, BOARD_SIZE))
        self.board_img = ImageTk.PhotoImage(img)

        # Canvas
        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE)
        self.canvas.pack(side="left")
        self.canvas.create_image(0, 0, anchor="nw", image=self.board_img)

        # Player tokens
        self.player_pos = 1
        self.computer_pos = 1

        x, y = num_to_xy(1)
        self.player_token = self.canvas.create_oval(x-12, y-12, x+12, y+12, fill="blue")
        self.computer_token = self.canvas.create_oval(x-12, y-12, x+12, y+12, fill="red")

        # Right side UI
        self.menu = tk.Frame(root, padx=10, pady=10)
        self.menu.pack(side="right", fill="y")

        self.turn_label = tk.Label(self.menu, text="🎮 Your Turn", font=("Helvetica", 14))
        self.turn_label.pack(pady=10)

        self.dice_btn = tk.Button(self.menu, text="Roll Dice 🎲", font=("Helvetica", 14),
                                  bg="#4CAF50", fg="white", command=self.player_turn)
        self.dice_btn.pack(pady=10)

        self.dice_label = tk.Label(self.menu, text="", font=("Helvetica", 20))
        self.dice_label.pack(pady=20)

    # -----------------------------
    # MOVE TOKEN SMOOTHLY
    # -----------------------------
    def animate_move(self, token, start, end):
        sx, sy = num_to_xy(start)
        ex, ey = num_to_xy(end)

        steps = 10
        for k in range(steps):
            nx = sx + (ex - sx) * k / steps
            ny = sy + (ey - sy) * k / steps
            self.canvas.coords(token, nx-12, ny-12, nx+12, ny+12)
            self.canvas.update()
            time.sleep(0.03)

        # final position
        self.canvas.coords(token, ex-12, ey-12, ex+12, ey+12)
        self.canvas.update()

    # -----------------------------
    # CHECK FOR SNAKES/LADDERS
    # -----------------------------
    def apply_snakes_ladders(self, pos):
        if pos in ladders:
            messagebox.showinfo("🪜 Ladder!", f"Climb to {ladders[pos]}")
            return ladders[pos]
        if pos in snakes:
            messagebox.showinfo("🐍 Snake Bite!", f"Fall to {snakes[pos]}")
            return snakes[pos]
        return pos

    # -----------------------------
    # PLAYER TURN
    # -----------------------------
    def player_turn(self):
        self.dice_btn.config(state="disabled")
        dice = roll_dice()
        self.dice_label.config(text=f"{dice}")

        new_pos = self.player_pos + dice
        if new_pos > 100:
            new_pos = 100 - (new_pos - 100)

        # Animate movement
        self.animate_move(self.player_token, self.player_pos, new_pos)
        self.player_pos = new_pos

        # Check snakes/ladders
        final = self.apply_snakes_ladders(self.player_pos)
        if final != self.player_pos:
            self.animate_move(self.player_token, self.player_pos, final)
            self.player_pos = final

        # Win check
        if self.player_pos == 100:
            messagebox.showinfo("🏆 You Win!", "Great job!")
            self.root.destroy()
            return

        self.turn_label.config(text="🤖 Computer's Turn")
        self.root.after(1500, self.computer_turn)

    # -----------------------------
    # COMPUTER TURN
    # -----------------------------
    def computer_turn(self):
        dice = roll_dice()
        self.dice_label.config(text=f"{dice}")

        new_pos = self.computer_pos + dice
        if new_pos > 100:
            new_pos = 100 - (new_pos - 100)

        self.animate_move(self.computer_token, self.computer_pos, new_pos)
        self.computer_pos = new_pos

        final = self.apply_snakes_ladders(self.computer_pos)
        if final != self.computer_pos:
            self.animate_move(self.computer_token, self.computer_pos, final)
            self.computer_pos = final

        if self.computer_pos == 100:
            messagebox.showinfo("💻 Computer Wins!", "Try again!")
            self.root.destroy()
            return

        self.turn_label.config(text="🎮 Your Turn")
        self.dice_btn.config(state="normal")

# -----------------------------
# MAIN APP
# -----------------------------
root = tk.Tk()
SnakeLadderGame(root)
root.mainloop()