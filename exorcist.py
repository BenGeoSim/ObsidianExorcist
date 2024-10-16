# Requires the 'pillow' library for handling images
# pip install pillow

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

LAST_USED_FILE = "last_used_file.txt"  # File to store the path of the last markdown file

PLACEHOLDER_TEXT = "Enter your markdown content here..."

# Set the overall interface height and button height
INTERFACE_HEIGHT = 312
BUTTON_HEIGHT = 30
BUFFER = 20

def calculate_text_height():
    """
    Calculate the height of the text field based on the interface height, button height, and buffer.
    """
    available_height = INTERFACE_HEIGHT - BUTTON_HEIGHT - BUFFER
    # Approximate line height for text widget (varies with font size, let's assume ~20 pixels per line)
    line_height = 20
    return available_height // line_height

def load_last_file():
    """
    Load the path of the last used markdown file from a text file.
    If the file or path doesn't exist, return None.
    """
    if os.path.exists(LAST_USED_FILE):
        with open(LAST_USED_FILE, "r") as file:
            path = file.read().strip()
            if os.path.exists(path):
                return path
    return None

def save_last_file(path):
    """
    Save the given markdown file path to the last used file.
    """
    with open(LAST_USED_FILE, "w") as file:
        file.write(path)

def select_markdown_file():
    """
    Opens a file dialog for the user to select a markdown file.
    """
    file_path = filedialog.askopenfilename(
        title="Select Markdown File", 
        filetypes=(("Markdown Files", "*.md"), ("All Files", "*.*"))
    )
    if file_path:
        save_last_file(file_path)
        return file_path
    else:
        messagebox.showerror("File Error", "No file selected.")
        return None

def save_to_markdown():
    """
    Append the text from the text field to the markdown file.
    """
    global markdown_file
    if markdown_file is None:
        markdown_file = select_markdown_file()
    if markdown_file:
        text = text_field.get("1.0", "end-1c").strip() + "\n"  # Add a newline at the end
        if text.strip() != PLACEHOLDER_TEXT:  # Don't save the placeholder text
            with open(markdown_file, "a") as file:  # Use "a" mode to append
                file.write(text)
        
        # Clear the text field after saving
        text_field.delete("1.0", tk.END)
        text_field.insert("1.0", PLACEHOLDER_TEXT)
        text_field.config(fg="gray")  # Reset placeholder color
    else:
        messagebox.showerror("File Error", "Unable to save, no file selected.")

def clear_placeholder(event):
    """
    Clear the placeholder text when the user starts typing.
    """
    if text_field.get("1.0", "end-1c") == PLACEHOLDER_TEXT:
        text_field.delete("1.0", tk.END)
        text_field.config(fg="white")  # Change to white font color when user types

# Create the main application window
root = tk.Tk()
root.title("Markdown Saver")

# Set the window resolution to 1000x312 pixels
root.geometry("1000x312")

# Load the background image using the absolute path
script_dir = os.path.dirname(os.path.abspath(__file__))
bg_image_path = os.path.join(script_dir, "bg.png")

try:
    bg_image = Image.open(bg_image_path)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a canvas to display the background image
    canvas = tk.Canvas(root, width=1000, height=312)
    canvas.pack(fill="both", expand=True)

    # Display the background image on the canvas
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Calculate text field height based on available space
    text_height = calculate_text_height()

    # Create a text field on the canvas (Text widget) for typing
    text_field = tk.Text(root, height=text_height, width=70, bg="black", fg="gray", insertbackground="white")  # Adjust width
    text_field.insert("1.0", PLACEHOLDER_TEXT)  # Insert placeholder text
    text_field.bind("<FocusIn>", clear_placeholder)  # Bind to focus event for clearing placeholder

    # Set the text box starting at exactly 380px on the x-axis
    canvas.create_window(680, (INTERFACE_HEIGHT - BUTTON_HEIGHT) // 2, window=text_field, anchor="center")  # Centered at 380px, width roughly 600px

    # Create a save button on the canvas to save the text into the markdown file
    save_button = tk.Button(root, text="Save to Markdown", command=save_to_markdown, bg="black", fg="white", width=70)
    # Set the y value to 295
    canvas.create_window(680, INTERFACE_HEIGHT - (BUTTON_HEIGHT // 2) - BUFFER, window=save_button, anchor="center")  # Align it with the text field

    # Load the last used markdown file
    markdown_file = load_last_file()

except FileNotFoundError:
    messagebox.showerror("File Error", f"Could not find the background image: {bg_image_path}")

# Run the Tkinter event loop
root.mainloop()
