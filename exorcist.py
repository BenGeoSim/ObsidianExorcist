# Requires the 'pillow' library for handling images
# Requires the 'pygame' library for playing MIDI files
# pip install pillow pygame

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pygame  # For playing the MIDI file

LAST_USED_FILE = "last_used_file.txt"  # File to store the path of the last markdown file
PLACEHOLDER_TEXT = "BEGONE, FOUL SPIRIT!"  # Placeholder text for the text field
INTERFACE_HEIGHT = 312
BUTTON_HEIGHT = 30
BUFFER = 20

# Initialize the Pygame mixer to handle sound
pygame.mixer.init()

# Track if the sound is currently muted
is_muted = True  # Start with the sound muted

# Track mouse position for dragging the window
x_offset = 0
y_offset = 0

def play_midi():
    """Play the 'halloween - the exorcist.mid' file located in the script folder."""
    midi_path = os.path.join(script_dir, "halloween - the exorcist.mid")
    if os.path.exists(midi_path):
        pygame.mixer.music.load(midi_path)
        pygame.mixer.music.play(-1)  # Loop the MIDI file indefinitely
        pygame.mixer.music.pause()  # Start the sound muted (paused)
    else:
        messagebox.showerror("MIDI Error", f"Could not find the MIDI file: {midi_path}")

def toggle_sound():
    """Toggle sound on and off, and update the mute button icon."""
    global is_muted
    if is_muted:
        pygame.mixer.music.unpause()
        mute_button.config(image=sound_on_icon)
    else:
        pygame.mixer.music.pause()
        mute_button.config(image=sound_off_icon)
    is_muted = not is_muted

def close_app():
    """Close the application."""
    root.quit()

def calculate_text_height():
    """Calculate the height of the text field based on the interface height, button height, and buffer."""
    available_height = INTERFACE_HEIGHT - BUTTON_HEIGHT - BUFFER
    line_height = 20
    return available_height // line_height

def load_last_file():
    """Load the path of the last used markdown file from a text file."""
    if os.path.exists(LAST_USED_FILE):
        with open(LAST_USED_FILE, "r") as file:
            path = file.read().strip()
            if os.path.exists(path):
                return path
    return None

def save_last_file(path):
    """Save the given markdown file path to the last used file."""
    with open(LAST_USED_FILE, "w") as file:
        file.write(path)

def select_markdown_file():
    """Opens a file dialog for the user to select a markdown file."""
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
    """Append the text from the text field to the markdown file."""
    global markdown_file
    if markdown_file is None:
        markdown_file = select_markdown_file()
    if markdown_file:
        text = text_field.get("1.0", "end-1c").strip() + "\n"
        if text.strip() != PLACEHOLDER_TEXT:  # Don't save the placeholder text
            with open(markdown_file, "a") as file:
                file.write(text)
        text_field.delete("1.0", tk.END)
        text_field.insert("1.0", PLACEHOLDER_TEXT)
        text_field.config(fg="gray")
    else:
        messagebox.showerror("File Error", "Unable to save, no file selected.")

def clear_placeholder(event):
    """Clear the placeholder text when the user starts typing."""
    if text_field.get("1.0", "end-1c") == PLACEHOLDER_TEXT:
        text_field.delete("1.0", tk.END)
        text_field.config(fg="white")

def on_mouse_press(event):
    """Record the offset when the mouse button is pressed."""
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

def on_mouse_drag(event):
    """Drag the window using the mouse."""
    x = event.x_root - x_offset
    y = event.y_root - y_offset
    root.geometry(f"+{x}+{y}")

# Create the main application window
root = tk.Tk()
root.title("BRAIN EXORCISM")

# Remove the title bar and make the window borderless
root.overrideredirect(True)
root.geometry("1000x312")

# Bind the mouse events to enable dragging
root.bind("<Button-1>", on_mouse_press)  # When left-click is pressed
root.bind("<B1-Motion>", on_mouse_drag)  # When the left-click is held and dragged

# Load the background image
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

    # Calculate text field height
    text_height = calculate_text_height()

    # Create a text field
    text_field = tk.Text(root, height=text_height, width=70, bg="black", fg="gray", insertbackground="white")
    text_field.insert("1.0", PLACEHOLDER_TEXT)
    text_field.bind("<FocusIn>", clear_placeholder)
    canvas.create_window(680, (INTERFACE_HEIGHT - BUTTON_HEIGHT) // 2, window=text_field, anchor="center")

    # Create a save button
    save_button = tk.Button(root, text="EXORCISE!!!", command=save_to_markdown, bg="black", fg="white", width=70)
    canvas.create_window(680, INTERFACE_HEIGHT - (BUTTON_HEIGHT // 2) - BUFFER, window=save_button, anchor="center")

    # Load the last used markdown file
    markdown_file = load_last_file()

    # Play the MIDI file
    play_midi()

    # Load the close button image and create the button
    close_icon_path = os.path.join(script_dir, "icon_close.png")
    close_icon = ImageTk.PhotoImage(Image.open(close_icon_path).resize((24, 24)))
    close_button = tk.Button(root, image=close_icon, command=close_app, bg="black", borderwidth=0)
    canvas.create_window(970, 4, window=close_button, anchor="ne")

    # Load the sound toggle button images and create the button
    sound_on_icon_path = os.path.join(script_dir, "icon_sound_on.png")
    sound_off_icon_path = os.path.join(script_dir, "icon_sound_off.png")
    sound_on_icon = ImageTk.PhotoImage(Image.open(sound_on_icon_path).resize((24, 24)))
    sound_off_icon = ImageTk.PhotoImage(Image.open(sound_off_icon_path).resize((24, 24)))

    # Set the initial state of the mute button to show sound as off (muted)
    mute_button = tk.Button(root, image=sound_off_icon, command=toggle_sound, bg="black", borderwidth=0)
    canvas.create_window(940, 4, window=mute_button, anchor="ne")

except FileNotFoundError:
    messagebox.showerror("File Error", f"Could not find the background image: {bg_image_path}")

# Run the Tkinter event loop
root.mainloop()
