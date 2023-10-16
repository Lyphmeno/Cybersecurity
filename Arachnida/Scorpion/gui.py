import tkinter as tk
from PIL import Image, ImageTk
import imghdr
import struct

class ImageViewer:
    def __init__(self, root, image_files):
        self.root = root
        self.root.title("Image Viewer")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.geometry("800x600") 
        self.image_label = tk.Label(root)
        self.image_label.pack(side="left")
        self.metadata_label = tk.Label(root, justify="left")
        self.metadata_label.pack(side="right", fill="both", expand=True)
        self.image_index = 0
        self.images = image_files
        self.update_image()
        self.root.bind("<Left>", self.prev_image)
        self.root.bind("<Right>", self.next_image)

    def on_close(self):
        self.root.destroy()

    def update_image(self):
        if self.images:
            image_file = self.images[self.image_index]
            image = Image.open(image_file)
            width, height = self.get_dim(image)
            image = image.resize((width, height), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

    def prev_image(self, event):
        self.image_index = (self.image_index - 1) % len(self.images)
        self.update_image()

    def next_image(self, event):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.update_image()

    def get_dim(self, image, size=400):
        width, height = image.size
        if width > size or height > size:
            if width > height:
                new_width = size
                new_height = int(height * size / width)
            else:
                new_height = size
                new_width = int(width * size / height)
        else:
            new_width = width
            new_height = height
        return new_width, new_height
