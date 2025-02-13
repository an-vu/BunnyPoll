import tkinter as tk
from tkinter import messagebox, ttk

class VoteApp:
    def __init__(self, root, voting_system):
        """
        Initialize the VoteApp class.

        Args:
        root (Tk): The Tkinter root window.
        voting_system (VotingSystem): An instance of the VotingSystem class.
        """
        self.root = root
        root.title("BunnyPoll")
        self.voting_system = voting_system
        self.setup_window()
        self.setup_frames()
        self.setup_buttons_style()

    def setup_window(self):
        """
        Set up the main window properties like size and resizability.
        """
        self.root.resizable(False, False)
        self.root.geometry("420x505")

    '''FRAME SET UP'''
    def setup_frames(self):
        """
        Set up the top, middle, and bottom frames of the application.
        """
        self.setup_top_frame() 
        self.setup_middle_frame()
        self.setup_bottom_frame()

    def setup_top_frame(self):
        """
        Set up the top frame of the application, including the logo, title, and poll grid.
        """
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X)
        self.setup_logo_and_title(top_frame)
        self.setup_polls_grid(top_frame)

    def setup_middle_frame(self):
        """
        Set up the middle frame of the application. This is used for dynamic content like switching screens.
        """
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(expand=True, fill=tk.BOTH)

    def setup_bottom_frame(self):
        """
        Set up the bottom frame of the application, including the button frame and credit label.
        """
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side="bottom", fill=tk.X)
        self.button_frame = tk.Frame(self.bottom_frame)
        self.button_frame.pack(pady=(10, 20))
        self.setup_credit_label(self.bottom_frame)

    def setup_buttons_style(self):
        """
        Configure the styles for various types of buttons used in the application.
        """
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("Danger.TButton", foreground="white", background="#ff3b30")
        style.configure("Primary.TButton", foreground="white", background="#007aff")
        style.map("TButton", foreground=[('disabled', 'grey')])
        style.configure("Post.TButton", foreground="#007aff", padding=3)
        style.configure("Remove.TButton", foreground="#ff3b30", padding=3)

    def clear_button_frame(self):
        """
        Clear all widgets from the button frame to refresh the button area.
        """
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    '''HOME SCREEN'''
    def setup_logo_and_title(self, parent):
        """
        Sets up the logo and title on the provided parent frame.

        Args:
        parent (tk.Frame): The parent frame where the logo and title will be placed.
        """
        emoji_label = tk.Label(parent, text="🐰", font=("Helvetica", 50))
        emoji_label.pack(pady=20)
        tk.Label(parent, text="Welcome to BunnyPoll! 🥕", font=("Helvetica", 24)).pack()

    def create_polls_grid(self):
        """
        Creates or refreshes the grid of poll buttons. Existing buttons are cleared and new buttons are created 
        based on the current list of polls. 
        """
        # Clear existing poll buttons if any
        for button in self.poll_buttons:
            if button is not None:
                button.destroy()

        # Set up or refresh poll buttons
        existing_polls = self.voting_system.list_polls()
        for i in range(4):
            if i < len(existing_polls):
                poll_name = existing_polls[i].split(": ")[1] if ':' in existing_polls[i] else existing_polls[i]
                button_text = poll_name
                command = lambda name=poll_name: self.show_poll(name)
            else:
                button_text = "Create a new poll"
                command = self.show_create_poll_screen

            self.poll_buttons[i] = tk.Button(self.polls_frame, text=button_text, command=command, width=10, height=5)
            row, col = divmod(i, 2)
            self.poll_buttons[i].grid(row=row, column=col, padx=10, pady=10, ipadx=10, ipady=10)
    
    def setup_polls_grid(self, parent):
        """
        Sets up the main polls grid on the provided parent widget. If the polls frame already exists, it is reset.

        Args:
        parent (tk.Widget): The parent widget where the polls grid will be set up.
        """
        # Check if polls_frame already exists and is packed
        if hasattr(self, 'polls_frame') and self.polls_frame.winfo_ismapped():
            self.polls_frame.pack_forget()

        self.polls_frame = tk.Frame(parent)
        self.polls_frame.pack(pady=30)
        self.poll_buttons = [None] * 4
        self.create_polls_grid()

    def setup_credit_label(self, parent):
        """
        Sets up a credit label on the provided parent frame.

        Args:
        parent (tk.Frame): The parent frame where the credit label will be placed.
        """
        credit_frame = tk.Frame(parent)
        credit_frame.pack(side="bottom", fill=tk.X, pady=(5, 10))
        tk.Label(credit_frame, text="Developed by An Vu - December 2023", font=("Helvetica", 10), fg="grey").pack()

    '''CREATE POLL SCREEN'''
    def show_create_poll_screen(self):
        """
        Displays the screen for creating a new poll. It includes input fields for the poll name,
        description, and choices. Also sets up buttons specific to this screen.
        """
        self.polls_frame.pack_forget()
        self.create_poll_frame = tk.Frame(self.middle_frame)
        self.create_poll_frame.pack(expand=True, fill=tk.BOTH)

        # Set a uniform width for all entry widgets
        uniform_font_size = 14
        uniform_width = 45

        # Name and Description Input Fields
        self.poll_name_entry = self.create_entry_with_placeholder("Name*", uniform_font_size, uniform_width, pady=(10, 0))
        self.poll_description_entry = self.create_entry_with_placeholder("Enter a description/question", uniform_font_size, uniform_width, pady=(5, 20))

        # Frame for Choice Entries
        self.choice_frame = tk.Frame(self.create_poll_frame)
        self.choice_frame.pack(pady=(0, 10))
        self.choice_entries = []
        for i in range(2):
            self.add_choice()

        # Setup buttons specific to this screen
        self.setup_poll_buttons()

        self.root.update()
        self.poll_name_entry.focus_set()

    def create_entry_with_placeholder(self, placeholder, font_size, width, pady, default_text=''):
        """
        Creates an entry widget with a placeholder text.

        Args:
        placeholder (str): The placeholder text for the entry widget.
        font_size (int): The font size for the text in the entry.
        width (int): The width of the entry widget.
        pady (int): The vertical padding around the entry widget.
        default_text (str, optional): Default text to display in the entry. Defaults to an empty string.

        Returns:
        tk.Entry: The created entry widget.
        """        
        entry = tk.Entry(self.create_poll_frame, width=width, font=("Helvetica", font_size), fg='grey')
        if default_text:
            entry.insert(0, default_text)
            entry.config(fg='black')
        else:
            entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda args: self.on_entry_click(entry, placeholder))
        entry.bind("<FocusOut>", lambda args: self.on_focusout(entry, placeholder))
        entry.pack(pady=pady)
        return entry

    def setup_poll_buttons(self):
        """
        Sets up the buttons for the create poll screen including 'Add choice', 'Remove Poll', and 'Post'.
        """
        self.clear_button_frame()

        # Add buttons for 'Create Poll' screen
        self.add_button = ttk.Button(self.button_frame, text="Add choice", style="Small.TButton", command=self.add_choice)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(self.button_frame, text="Remove Poll", style="Remove.TButton", command=self.show_home_screen).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(self.button_frame, text="Post", style="Post.TButton", command=self.post_poll).pack(side=tk.LEFT, padx=5, pady=5)

    def on_entry_click(self, entry, placeholder):
        """
        Event handler for when an entry widget is clicked. Removes placeholder text and changes text color.

        Args:
        entry (tk.Entry): The entry widget that is clicked.
        placeholder (str): The placeholder text of the entry widget.
        """
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focusout(self, entry, placeholder):
        """
        Event handler for when an entry widget loses focus. Restores placeholder text if the entry is empty.

        Args:
        entry (tk.Entry): The entry widget that lost focus.
        placeholder (str): The placeholder text for the entry widget.
        """
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    def add_choice(self, default_text=''):
        """
        Adds a new choice entry to the create poll screen.

        Args:
        default_text (str, optional): Default text for the new choice entry. Defaults to an empty string.
        """
        choice_number = len(self.choice_entries) + 1
        placeholder = f"Choice {choice_number}" + ("*" if choice_number <= 2 else " (Optional)")
        new_choice = self.create_entry_with_placeholder(placeholder, 14, 45, pady=(0, 5), default_text=default_text)
        self.choice_entries.append(new_choice)
        new_choice.pack(in_=self.choice_frame)
        if len(self.choice_entries) >= 4:
            self.add_button.configure(state='disabled')

    def post_poll(self):
        """
        Handles the posting of a new poll. Retrieves data from entry widgets, validates them,
        and creates a new poll in the voting system.
        """
        poll_name = self.poll_name_entry.get().strip()
        description = self.poll_description_entry.get().strip()

        # Replace placeholder text with a blank string if description is not entered
        if description == "Enter a description/question":
            description = ""

        # Retrieve choices from choice_entries
        choices = [entry.get().strip() for entry in self.choice_entries if entry.get().strip()]

        placeholders = ["Name*", "Choice 1*", "Choice 2*", "Choice 3 (Optional)", "Choice 4 (Optional)"]
        valid_choices = [choice for choice, placeholder in zip(choices, placeholders[1:]) if choice != placeholder]

        if not poll_name or poll_name == placeholders[0] or len(valid_choices) < 2:
            messagebox.showwarning("Warning", "Please complete the required field(s)*.")
            return

        self.voting_system.create_poll(poll_name, description, valid_choices)
        self.update_poll_button(poll_name)
        self.create_poll_frame.pack_forget()
        self.polls_frame.pack()

        # Update CSV file
        self.voting_system.save_polls_to_csv()

    def update_poll_button(self, poll_name):
        """
        Updates the poll button on the home screen after a new poll is created or an existing one is edited.

        Args:
        poll_name (str): The name of the poll to update on the home screen.
        """
        for button in self.poll_buttons:
            if button["text"] == "Create a new poll":
                button.config(text=poll_name, command=lambda: self.show_poll(poll_name))
                break
    
    '''VOTE SCREEN'''
    def show_poll(self, poll_name):
        """
        Displays the voting screen for a selected poll. It shows the poll name, description, 
        and buttons for each choice, allowing users to cast their votes.

        Args:
        poll_name (str): The name of the poll to display.
        """
        self.current_poll_name = poll_name  # Store the current poll name
        self.voting_system.reload_polls_from_csv()  # Refresh the poll data

        if hasattr(self, 'create_poll_frame'):
            self.create_poll_frame.pack_forget()

        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.polls_frame.pack_forget()
        self.voting_frame = tk.Frame(self.middle_frame)
        self.voting_frame.pack(expand=True, fill=tk.BOTH, pady=20)

        tk.Label(self.voting_frame, text=poll_name, font=("Helvetica", 18)).pack(pady=(10, 10))

        poll_data = self.voting_system.get_poll_data(poll_name)

        if poll_data and poll_data.get('description'):
            tk.Label(self.voting_frame, text=poll_data['description'], font=("Helvetica", 14)).pack(pady=(0, 20))

        choices = list(poll_data['candidates'].keys()) if 'candidates' in poll_data else []

        # Store vote labels for updating
        self.vote_labels = {}

        for choice in choices:
            if not choice.isdigit():
                choice_frame = tk.Frame(self.voting_frame)
                choice_frame.pack(fill=tk.X, pady=5, padx=20)

                tk.Button(choice_frame, text=choice, command=lambda c=choice: self.vote(c)).pack(side=tk.LEFT, padx=10)

                vote_label = tk.Label(choice_frame, text=str(poll_data['candidates'][choice]))
                vote_label.pack(side=tk.RIGHT, padx=10)
                self.vote_labels[choice] = vote_label

        self.setup_vote_screen_buttons()

    def setup_vote_screen_buttons(self):
        """
        Sets up the buttons for the voting screen, including 'Back', 'Edit', and 'Export'.
        """
        self.clear_button_frame()

        # Add buttons for 'Vote' screen
        ttk.Button(self.button_frame, text="Back", style="Small.TButton", command=self.show_home_screen).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(self.button_frame, text="Edit", style="Small.TButton", command=lambda: self.edit_poll(self.current_poll_name)).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(self.button_frame, text="Export", style="Small.TButton", command=self.export_poll).pack(side=tk.LEFT, padx=5, pady=5)

    def vote(self, choice):
        """
        Casts a vote for a given choice in the current poll and updates the vote count.

        Args:
        choice (str): The choice for which the vote is cast.
        """
        voted = self.voting_system.cast_vote(self.current_poll_name, choice)

        # Update the vote count labels and CSV file if the vote was successful
        if voted:
            self.voting_system.save_polls_to_csv()
            poll_data = self.voting_system.get_poll_data(self.current_poll_name)
            new_vote_count = poll_data['candidates'][choice]
            self.vote_labels[choice].config(text=str(new_vote_count))

    def show_home_screen(self):
        """
        Returns to the home screen, hiding any other screens and refreshing the poll grid.
        """
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # Hide the current frame and show the polls frame
        if hasattr(self, 'create_poll_frame') and self.create_poll_frame.winfo_ismapped():
            self.create_poll_frame.pack_forget()
        if hasattr(self, 'edit_poll_frame') and self.edit_poll_frame.winfo_ismapped():
            self.edit_poll_frame.pack_forget()
        if hasattr(self, 'voting_frame') and self.voting_frame.winfo_ismapped():
            self.voting_frame.pack_forget()

        # Ensure consistent geometry management for polls_frame
        self.polls_frame.pack(pady=30)

        # Refresh the polls grid
        self.create_polls_grid()

    def edit_poll(self, poll_name):
        """
        Displays the edit poll screen for modifying an existing poll.

        Args:
        poll_name (str): The name of the poll to edit.
        """
        self.polls_frame.pack_forget()
        if hasattr(self, 'voting_frame'):
            self.voting_frame.pack_forget()

        # Show the edit poll screen
        self.show_edit_poll_screen(poll_name)

        # Set up buttons specific to the edit poll screen
        self.setup_edit_poll_buttons(poll_name)

    def export_poll(self):
        """
        Exports the data of the currently viewed poll to a .txt file and displays a success or failure message.
        """
        success = self.voting_system.export_poll_to_txt(self.current_poll_name)
        if success:
            messagebox.showinfo("Export Successful!", f"Poll exported as '{self.current_poll_name}.txt'.")
        else:
            messagebox.showerror("Export Failed", "Failed to export the poll.")

    '''EDIT POLL SCREEN'''
    def show_edit_poll_screen(self, poll_name):
        """
        Displays the edit poll screen for a specific poll, allowing the user to modify its details.

        Args:
            poll_name (str): The name of the poll to be edited.
        """
        self.current_poll_name = poll_name  # Store the current poll name
        poll_data = self.voting_system.get_poll_data(poll_name)
        choices = list(poll_data['candidates'].keys()) if 'candidates' in poll_data else []

        self.show_create_poll_screen()

        # Populate the poll name and description fields
        self.poll_name_entry.delete(0, tk.END)
        self.poll_name_entry.insert(0, poll_data['name'])
        self.poll_name_entry.config(fg='black')

        self.poll_description_entry.delete(0, tk.END)
        description_text = poll_data['description'] if poll_data['description'] else "Enter a description/question"
        self.poll_description_entry.insert(0, description_text)
        self.poll_description_entry.config(fg='black' if poll_data['description'] else 'grey')

        # Clear existing choice entries and add entries for existing choices
        for choice_entry in self.choice_entries:
            choice_entry.destroy()
        self.choice_entries.clear()

        for i, choice in enumerate(choices, start=1):
            choice_text = f"Choice {i}" if i <= 2 else f"Choice {i} (Optional)"
            new_choice_entry = self.create_entry_with_placeholder(choice_text, 14, 45, pady=(0, 5))
            new_choice_entry.delete(0, tk.END)
            new_choice_entry.insert(0, choice)
            new_choice_entry.config(fg='black')
            new_choice_entry.pack(in_=self.choice_frame)
            self.choice_entries.append(new_choice_entry)

        # Adjust the state of the 'Add choice' button
        self.add_button.configure(state='normal' if len(self.choice_entries) < 4 else 'disabled')

    def setup_edit_poll_buttons(self, poll_name):
        """
        Sets up the buttons for the edit poll screen, including buttons for adding choices, 
        saving changes, deleting the poll, and canceling the edit.

        Args:
            poll_name (str): The name of the poll being edited.
        """
        self.clear_button_frame()

        # Configure the style for the edit screen buttons
        style = ttk.Style()
        style.configure("Edit.TButton", padding=3, font=('Helvetica', 12))
        style.configure("SaveEdit.TButton", padding=3, font=('Helvetica', 12), foreground="#007aff")  # Blue text for Save
        style.configure("DeleteEdit.TButton", padding=3, font=('Helvetica', 12), foreground="#ff3b30")  # Red text for Delete

        # Add the buttons with consistent style and reduced horizontal padding
        self.add_button = ttk.Button(self.button_frame, text="Add choice", style="Edit.TButton", command=self.add_choice)
        self.add_button.pack(side=tk.LEFT, padx=2, pady=2)
        
        ttk.Button(self.button_frame, text="Delete Poll", style="DeleteEdit.TButton", command=lambda: self.delete_poll(poll_name)).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(self.button_frame, text="Save", style="SaveEdit.TButton", command=lambda: self.save_edited_poll(poll_name)).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(self.button_frame, text="Cancel", style="Edit.TButton", command=self.show_home_screen).pack(side=tk.LEFT, padx=2, pady=2)

        # Check if the 'Add choice' button should be disabled initially
        if len(self.choice_entries) >= 4:
            self.add_button.configure(state='disabled')

    def save_edited_poll(self, original_poll_name):
        """
        Saves the edited poll with the new details entered by the user.

        Args:
            original_poll_name (str): The original name of the poll before editing.
        """
        poll_name = self.poll_name_entry.get().strip()
        description = self.poll_description_entry.get().strip()

        # Replace placeholder text with a blank string if description is not entered
        if description == "Enter a description/question":
            description = ""

        # Define placeholders for easier comparison
        placeholders = ["Name*", "Choice 1*", "Choice 2*", "Choice 3 (Optional)", "Choice 4 (Optional)"]

        # Only consider input valid if it's not equal to the placeholder
        valid_choices = [entry.get().strip() for entry, placeholder in zip(self.choice_entries, placeholders[1:]) if entry.get().strip() and entry.get().strip() != placeholder]
        
        if not poll_name or poll_name == placeholders[0] or len(valid_choices) < 2:
            messagebox.showwarning("Warning", "Please complete the required field(s)*.")
            return

        # Update the poll with the new details
        self.voting_system.modify_poll(original_poll_name, poll_name, description, valid_choices)
        self.update_poll_button(poll_name)
        self.create_poll_frame.pack_forget()
        self.polls_frame.pack()

        # Update CSV file
        self.voting_system.save_polls_to_csv()

        # Refresh the polls grid and return to the home screen
        self.create_polls_grid()
        self.create_poll_frame.pack_forget()
        self.polls_frame.pack()

    def delete_poll(self, poll_name):
        """
        Deletes the specified poll from the voting system and updates the Home Screen.

        Args:
            poll_name (str): The name of the poll to delete.
        """
        deleted = self.voting_system.delete_poll(poll_name)

        # Show user feedback
        if deleted:
            messagebox.showinfo("Poll Deleted", f"'{poll_name}' is removed.")
        else:
            messagebox.showerror("Error", "Failed to delete the poll.")

        # Go back to the Home Screen and refresh
        self.show_home_screen()

