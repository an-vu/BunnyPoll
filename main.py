"""
BunnyPoll

Features:
- Allows users to create and participate in polls with a graphical interface. 
- Create polls with custom names, descriptions, and multiple choices.
- Vote on existing polls and see real-time updates on vote counts.
- Edit or delete existing polls.
- Export poll results to a text file.

To use the app, simply follow the on-screen instructions to create, edit, vote, or delete polls.

"""

import tkinter as tk
from vote import VotingSystem
from gui import VoteApp

def main():
    """
    Initializes and runs the BunnyPoll voting application.

    This function sets up the main window, centers it on the screen,
    initializes the voting system, and starts the application loop.
    """
    root = tk.Tk()
    root.withdraw()  # Initially hide the window

    voting_system = VotingSystem()
    app = VoteApp(root, voting_system)

    # Centering the window on the screen
    root.update()
    window_width, window_height = root.winfo_width(), root.winfo_height()
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    center_x, center_y = int(screen_width/2 - window_width / 2), int(screen_height/2 - window_height / 2)
    root.geometry(f'+{center_x}+{center_y}')

    root.deiconify()  # Show the window after centering

    root.mainloop()

if __name__ == "__main__":
    main()
