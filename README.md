# Bunny Poll 🐰

## Description

Bunny Poll is a simple, interactive polling application with a graphical user interface (GUI). It allows users to create, vote, edit, and manage polls in real-time. The app provides a user-friendly experience with live vote updates and data persistence through CSV files.

## Features

- **Create Polls:**  
    - Users can define custom poll names, descriptions, and multiple-choice options.
    - Polls are saved and can be accessed later.

- **Vote on Polls:**  
    - Select a poll and cast votes.
    - Live updates show the current vote count.

- **Edit & Delete Polls:**  
    - Modify poll details, including choices and descriptions.
    - Remove polls from the system.

- **Export Results:**  
    - Save poll results as a `.txt` file.

## Technologies Used

- **Backend:**
    - Python
    - CSV file handling for data storage
    - Object-Oriented Programming (OOP)

- **Frontend:**
    - `Tkinter` for GUI components
    - `ttk` for styled buttons and labels

## Installation

- Clone the repository:

```bash
git clone https://github.com/an-vu/bunnypoll.git
cd bunnypoll
```

## How to Use

1. **Run the Application:**

   ```bash
   python main.py
   ```

2. **Manage Polls:**
    - Create a new poll by entering a name, description, and options.
    - View available polls and select one to vote.
    - Edit or delete polls as needed.
    - Export poll results to a `.txt` file.
