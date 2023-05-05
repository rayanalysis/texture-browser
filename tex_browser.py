# Description: A minimal texture browser built to recognize images in immediate subfolders with
# "*PREVIEW*" in their names. Swap pages with forward and backward mouse buttons.
# Click on an image to open its asset folder.

import os
import glob
import subprocess
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


def get_preview_images(path):
    preview_images = []
    for f in os.listdir(path):
        subfolder_path = os.path.join(path, f)
        for p in os.listdir(subfolder_path):
            if "PREVIEW" in str(p):
                preview_images.append(os.path.join(subfolder_path, p))
    # print(preview_images)
    return preview_images

def on_image_click(event, img_path):
    print("Image clicked:", img_path)
    if os.name == 'nt':  # Windows
        os.startfile(os.path.dirname(img_path))
    elif os.name == 'posix':  # macOS and Linux
        subprocess.Popen(['open', os.path.dirname(img_path)])

def on_mouse_click(event, root, preview_images, page_var, texture_path):
    if event.num == 4:
        page_var.set(page_var.get() - 1)
    elif event.num == 5:
        page_var.set(page_var.get() + 1)

    update_grid(root, preview_images, page_var, texture_path)

def update_grid(root, preview_images, page_var, texture_path):
    for widget in root.grid_slaves():
        widget.grid_forget()

    page = page_var.get()
    start_index = page * 150
    print(preview_images)

    for i in range(150):
        if start_index + i >= len(preview_images):
            break

        img_path = preview_images[start_index + i]
        img = Image.open(img_path)
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        img_thumbnail = ImageTk.PhotoImage(img)

        label = tk.Label(root, image=img_thumbnail)
        label.image = img_thumbnail
        label.grid(row=i // 15, column=i % 10)

        label.bind("<Button-1>", lambda event, img_path=img_path: on_image_click(event, img_path))

def main():
    root = tk.Tk()
    root.title("Texture Browser")

    texture_path = filedialog.askdirectory(title="Select Texture Folder")
    preview_images = get_preview_images(texture_path)
    page_var = tk.IntVar(value=0)

    update_grid(root, preview_images, page_var, texture_path)
    root.bind("<Button-4>", lambda event, root=root, preview_images=preview_images, page_var=page_var, texture_path=texture_path: on_mouse_click(event, root, preview_images, page_var, texture_path))
    root.bind("<Button-5>", lambda event, root=root, preview_images=preview_images, page_var=page_var, texture_path=texture_path: on_mouse_click(event, root, preview_images, page_var, texture_path))
    root.focus_set()
    root.mainloop()

if __name__ == "__main__":
    main()
