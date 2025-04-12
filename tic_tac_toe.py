import tkinter as tk
import random

# Tema curentă
theme = "light"

# Culori inițiale - Tema light
BG_COLOR = "#f5f5f5"
X_COLOR = "#303F9F"
O_COLOR = "#37474F"
GRID_COLOR = "#B0BEC5"
WIN_COLOR = "#2ecc71"
BTN_COLOR = "#4a90e2"
BTN_HOVER = "#3a78c2"
TITLE_COLOR_1 = X_COLOR
TITLE_COLOR_2 = BTN_COLOR
TITLE_COLOR_3 = O_COLOR
FONT = ("Segoe UI", 20, "bold")
FONT_TITLE = ("Segoe UI", 26, "bold")

score_x = 0
score_o = 0
vs_ai = False

def check_winner():
    for row in range(3):
        if board[row][0]["text"] == board[row][1]["text"] == board[row][2]["text"] != "":
            highlight_winner([(row, 0), (row, 1), (row, 2)])
            return board[row][0]["text"]
    for col in range(3):
        if board[0][col]["text"] == board[1][col]["text"] == board[2][col]["text"] != "":
            highlight_winner([(0, col), (1, col), (2, col)])
            return board[0][col]["text"]
    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] != "":
        highlight_winner([(0, 0), (1, 1), (2, 2)])
        return board[0][0]["text"]
    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] != "":
        highlight_winner([(0, 2), (1, 1), (2, 0)])
        return board[0][2]["text"]
    return None

def highlight_winner(cells):
    for row, col in cells:
        board[row][col]["bg"] = WIN_COLOR

def show_winner_message(winner):
    if winner == "X":
        msg = "🎉 Player X wins!"
        color = X_COLOR
    elif winner == "O":
        msg = "🎉 Player O wins!"
        color = O_COLOR
    else:
        msg = "😐 It's a draw!"
        color = "black" if theme == "light" else "white"
    message_label.config(text=msg, fg=color)

def on_click(row, col):
    global current_player, score_x, score_o, game_over
    if board[row][col]["text"] == "" and not game_over:
        board[row][col]["text"] = current_player
        board[row][col]["fg"] = X_COLOR if current_player == "X" else O_COLOR
        winner = check_winner()
        if winner:
            game_over = True
            if winner == "X":
                score_x += 1
            else:
                score_o += 1
            update_score()
            show_winner_message(winner)
        elif all(board[i][j]["text"] != "" for i in range(3) for j in range(3)):
            game_over = True
            show_winner_message(None)
        else:
            current_player = "O" if current_player == "X" else "X"
            if vs_ai and current_player == "O" and not game_over:
                root.after(500, ai_move)

def ai_move():
    empty = [(i, j) for i in range(3) for j in range(3) if board[i][j]["text"] == ""]
    if empty:
        i, j = random.choice(empty)
        on_click(i, j)

def update_score():
    score_label.config(text=f"Jucatorul X: {score_x} | Jucatorul O: {score_o}")

def reset_game():
    global current_player, game_over
    current_player = "X"
    game_over = False
    for i in range(3):
        for j in range(3):
            board[i][j]["text"] = ""
            board[i][j]["fg"] = "white" if theme == "dark" else "black"
            board[i][j]["bg"] = BG_COLOR
    message_label.config(text="")

def restart_match():
    global score_x, score_o
    score_x = 0
    score_o = 0
    update_score()
    reset_game()

def toggle_theme():
    global BG_COLOR, X_COLOR, O_COLOR, GRID_COLOR, WIN_COLOR, BTN_COLOR, BTN_HOVER
    global TITLE_COLOR_1, TITLE_COLOR_2, TITLE_COLOR_3, theme

    if theme == "dark":
        theme = "light"
        BG_COLOR = "#f5f5f5"
        X_COLOR = "#303F9F"
        O_COLOR = "#37474F"
        GRID_COLOR = "#B0BEC5"
        WIN_COLOR = "#2ecc71"
        BTN_COLOR = "#4a90e2"
        BTN_HOVER = "#3a78c2"
    else:
        theme = "dark"
        BG_COLOR = "#1e1e1e"
        X_COLOR = "#00BCD4"
        O_COLOR = "#CFD8DC"
        GRID_COLOR = "#607D8B"
        WIN_COLOR = "#8BC34A"
        BTN_COLOR = "#4682B4"
        BTN_HOVER = "#37638a"

    TITLE_COLOR_1 = X_COLOR
    TITLE_COLOR_2 = GRID_COLOR
    TITLE_COLOR_3 = O_COLOR

    root.configure(bg=BG_COLOR)
    score_label.config(bg=BG_COLOR, fg=O_COLOR)
    message_label.config(bg=BG_COLOR)
    title_frame.config(bg=BG_COLOR)
    for widget, color in zip(title_frame.winfo_children(), [TITLE_COLOR_1, TITLE_COLOR_2, TITLE_COLOR_3]):
        widget.config(bg=BG_COLOR, fg=color)
    for i in range(3):
        for j in range(3):
            board[i][j].config(bg=BG_COLOR, highlightbackground=GRID_COLOR)
    btn_frame.config(bg=BG_COLOR)
    bottom_frame.config(bg=BG_COLOR)

def main():
    global root, board, score_label, message_label, title_frame, current_player, game_over, btn_frame, bottom_frame

    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.geometry("460x640")
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)
    current_player = "X"
    game_over = False
    board = [[None, None, None] for _ in range(3)]

    # Titlu
    title_frame = tk.Frame(root, bg=BG_COLOR)
    title_frame.pack(pady=(20, 5))
    tk.Label(title_frame, text="Tic", font=FONT_TITLE, fg=TITLE_COLOR_1, bg=BG_COLOR).pack(side="left")
    tk.Label(title_frame, text=" Tac ", font=FONT_TITLE, fg=TITLE_COLOR_2, bg=BG_COLOR).pack(side="left")
    tk.Label(title_frame, text="Toe", font=FONT_TITLE, fg=TITLE_COLOR_3, bg=BG_COLOR).pack(side="left")

    # Linie
    tk.Frame(root, bg=GRID_COLOR, height=2, width=250).pack(pady=5)

    # Scor
    score_label = tk.Label(root, text=f"Jucatorul X: {score_x} | Jucatorul O: {score_o}",
                           font=("Segoe UI", 14), fg=O_COLOR, bg=BG_COLOR)
    score_label.pack(pady=10)

    # Mesaj final
    message_label = tk.Label(root, text="", font=FONT, fg="black", bg=BG_COLOR)
    message_label.pack(pady=10)

    # Tabla
    frame = tk.Frame(root, bg=GRID_COLOR, padx=10, pady=10)
    frame.pack(pady=10)
    for i in range(3):
        for j in range(3):
            board[i][j] = tk.Button(frame, text="", font=FONT, width=6, height=2,
                                    fg="black", bg=BG_COLOR, activebackground=GRID_COLOR,
                                    highlightbackground=GRID_COLOR, borderwidth=0,
                                    command=lambda i=i, j=j: on_click(i, j))
            board[i][j].grid(row=i, column=j, padx=10, pady=6)

    # Butoane control
    btn_frame = tk.Frame(root, bg=BG_COLOR)
    btn_frame.pack(pady=10)

    reset_btn = tk.Button(btn_frame, text="Reset", font=("Segoe UI", 13, "bold"),
                          bg=BTN_COLOR, fg="white", activebackground=BTN_HOVER,
                          relief="flat", width=10, command=reset_game)
    reset_btn.pack(side="left", padx=10)

    restart_btn = tk.Button(btn_frame, text="Restart Match", font=("Segoe UI", 13, "bold"),
                            bg="#e63946", fg="white", activebackground="#b02e38",
                            relief="flat", width=14, command=restart_match)
    restart_btn.pack(side="left", padx=10)

    # Toggle Theme
    bottom_frame = tk.Frame(root, bg=BG_COLOR)
    bottom_frame.pack(pady=(10, 20))

    toggle_btn = tk.Button(bottom_frame, text="Toggle Theme", font=("Segoe UI", 11),
                           bg="#6c757d", fg="white", activebackground="#495057",
                           relief="flat", width=14, command=toggle_theme)
    toggle_btn.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
