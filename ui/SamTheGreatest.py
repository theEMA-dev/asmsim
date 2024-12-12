import tkinter as tk
from tkinter import filedialog, messagebox

def load_program():
    file_path = filedialog.askopenfilename(
        title="Select MIPS Assembly Program",
        filetypes=(("Assembly files", "*.asm"), ("All files", "*.*"))
    )
    if file_path:
        messagebox.showinfo("File Selected", f"Program file: {file_path}")
        print(f"Loaded program file: {file_path}")  # You can pass this to backend later.
    else:
        messagebox.showwarning("No File", "No program file was selected.")

def create_interface():
    # Create the main window
    root = tk.Tk()
    root.title("MIPS 32-bit Simulator Interface")
    root.geometry("400x200")

    # Add a button to load a program file
    load_button = tk.Button(
        root, text="Load MIPS Program", command=load_program, font=("Arial", 14)
    )
    load_button.pack(pady=20)

    # Add an exit button
    exit_button = tk.Button(
        root, text="Exit", command=root.quit, font=("Arial", 14)
    )
    exit_button.pack(pady=20)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    create_interface()

