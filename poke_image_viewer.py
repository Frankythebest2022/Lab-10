"""
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokemon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""
from tkinter import *
from tkinter import ttk
import os
from poke_api import get_pokemon_names, get_pokemon_info, download_image
import ctypes

# Get the script and images directory
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')

# Create the images directory if it does not exist
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

def set_desktop_image(image_path):
    # Set the provided image as the desktop background
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

def update_image(event):
    selected_pokemon = cbox_pokemon.get()
    if selected_pokemon:
        pokemon_info = get_pokemon_info(selected_pokemon)
        if pokemon_info:
            image_url = pokemon_info['sprites']['other']['official-artwork']['front_default']
            image_filename = f"{selected_pokemon}.png"
            image_path = os.path.join(images_dir, image_filename)

            if not os.path.exists(image_path):
                download_image(image_url, image_path)

            img = PhotoImage(file=image_path)
            lbl_image.config(image=img)
            lbl_image.image = img
            btn_set_desktop.config(state='normal')
        else:
            lbl_image.config(image='')
            lbl_image.image = None
            btn_set_desktop.config(state='disabled')

# Create the main window
root = Tk()
root.title("Pokemon Viewer")

#Set the icon 
root.iconbitmap(os.path.join(script_dir, 'pokemon.ico'))

# Create frames
frm_select = ttk.Frame(root)
frm_select.grid(row=30, padx=10, pady=10, sticky=W)

frm_image = ttk.Frame(root)
frm_image.grid(row=1, padx=70, pady=70, sticky=W)

# Populate frames with widgets and define event handler functions
lbl_select = ttk.Label(frm_select, text="Select Pokemon:")
lbl_select.grid(row=0, column=0, padx=(0, 5))

pokemon_names = get_pokemon_names()
cbox_pokemon = ttk.Combobox(frm_select, state='readonly', values=pokemon_names)
cbox_pokemon.grid(row=0, column=2)
cbox_pokemon.bind('<<ComboboxSelected>>', update_image)

btn_set_desktop = ttk.Button(frm_select, text="Set as Desktop Image", state='disabled')
btn_set_desktop.grid(row=0, column=3)
btn_set_desktop['command'] = lambda: set_desktop_image(os.path.join(images_dir, f"{cbox_pokemon.get()}.png"))

lbl_image = ttk.Label(frm_image)
lbl_image.grid(row=0, column=0)

# Create the default image
default_image_path = os.path.join(script_dir, 'pokemon.png')
default_img = PhotoImage(file=default_image_path)
lbl_image.config(image=default_img)
lbl_image.image = default_img
btn_set_desktop.config(state='disabled')

root.mainloop()
