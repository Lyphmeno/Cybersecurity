import tkinter as tk
from tkinter import ttk, scrolledtext
import piexif
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS

class ImageViewer:
    def __init__(self, root, image_files):
        self.root = root
        self.root.title("SCORPION")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.geometry("1080x720")

        self.image_frame = tk.Frame(root)
        self.image_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.image_label = tk.Label(self.image_frame, bg='#181818', borderwidth=1)
        self.image_label.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        self.metadata_label = tk.Label(self.image_frame, bg="#2C2C2C",  justify="left", bd=0)
        self.metadata_label.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)
        self.metadata_frame = tk.Frame(self.image_frame, bg="#2C2C2C", borderwidth=1)
        self.metadata_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        self.metadata_text = scrolledtext.ScrolledText(self.metadata_frame, wrap=tk.WORD, width=60, height=50)
        self.metadata_text.pack(pady=10)

        self.image_index = 0
        self.images = image_files
        self.update_viewer()
        
        self.root.bind("<Left>", self.prev_image)
        self.root.bind("<Right>", self.next_image)
        self.root.bind("<KeyPress>", self.on_key_press)

    def on_key_press(self, event):
        if event.keysym == 'Escape':
            self.on_close()

    def on_close(self):
        self.root.destroy()

    def update_viewer(self):
        if self.images:
            image_file = self.images[self.image_index]
            image = Image.open(image_file)
            width, height = self.get_dim(image)
            image = image.resize((width, height), Image.LANCZOS)
            border_size = 2
            bordered_image = Image.new('RGB', (width + 2 * border_size, height + 2 * border_size), '#2C2C2C')
            bordered_image.paste(image, (border_size, border_size))
            photo = ImageTk.PhotoImage(bordered_image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

            metadata = self.get_metadata(image_file)
            self.metadata_text.delete(1.0, tk.END)

            if isinstance(metadata, dict):
                for tag, value in metadata.items():
                    self.metadata_text.insert(tk.END, f"{tag}: {value}\n\n")
            else:
                self.metadata_text.insert(tk.END, str(metadata))

    def get_metadata(self, image_file):
        try:
            with Image.open(image_file) as img:
                exif_data = img._getexif()
                if exif_data:
                    standard_exif_data = {TAGS[tag]: value for tag, value in exif_data.items() if tag in TAGS}
                    return standard_exif_data
                else:
                    return {}
        except Exception as e:
            return f"Error reading Exif data: {e}"

    def prev_image(self, event):
        self.image_index = (self.image_index - 1) % len(self.images)
        self.update_viewer()

    def next_image(self, event):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.update_viewer()

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
