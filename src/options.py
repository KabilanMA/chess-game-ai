import tkinter as tk

class PawnPromotionWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pawn Promotion")
        self.selected_piece = None

    def create_buttons(self, piece_options):
        for option in piece_options:
            button = tk.Button(self.root, text=option, width=10, height=2, command=lambda piece=option: self.select_piece(piece))
            button.pack(pady=5)

    def select_piece(self, piece):
        self.selected_piece = piece
        self.root.destroy()

    def display_window(self,piece_options = ["Queen", "Rook", "Bishop", "Knight"]):
        self.create_buttons(piece_options)
        self.root.mainloop()
        return self.selected_piece