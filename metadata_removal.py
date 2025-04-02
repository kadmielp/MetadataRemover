import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import os

class MetadataRemoverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Metadata Remover")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # ExifTool path
        self.exiftool_path = r"C:\Program Files\ExifTool\exiftool.exe"
        
        # Check if ExifTool exists
        if not os.path.exists(self.exiftool_path):
            messagebox.showerror("Error", 
                "ExifTool not found!\nPlease install ExifTool from:\nhttps://exiftool.org/\n" +
                "And ensure it's installed in: " + self.exiftool_path)
            root.quit()
            return

        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Left frame for controls
        self.left_frame = tk.Frame(self.root, width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Right frame for image preview
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # File path label
        self.path_label = tk.Label(self.left_frame, text="No file selected", 
                                 wraplength=280)
        self.path_label.pack(pady=10)

        # Browse button
        self.browse_button = tk.Button(self.left_frame, text="Browse Image", 
                                     command=self.browse_file, pady=5)
        self.browse_button.pack()

        # Remove metadata button
        self.remove_button = tk.Button(self.left_frame, text="Remove Metadata", 
                                     command=self.remove_metadata, 
                                     state='disabled', pady=5)
        self.remove_button.pack(pady=10)

        # Status label
        self.status_label = tk.Label(self.left_frame, text="", fg="black", wraplength=280)
        self.status_label.pack(pady=10)

        # Image preview label
        self.preview_frame = tk.Frame(self.right_frame, 
                                    width=450, height=450, 
                                    relief=tk.SUNKEN, bd=2)
        self.preview_frame.pack(padx=10, pady=10)
        self.preview_frame.pack_propagate(False)  # Prevent frame from shrinking

        self.preview_label = tk.Label(self.preview_frame, text="Image Preview")
        self.preview_label.pack(expand=True)

        # Store the reference to the photo
        self.photo = None

    def load_and_resize_image(self, image_path):
        """Load and resize image to fit the preview frame"""
        try:
            # Open image with PIL
            image = Image.open(image_path)
            
            # Calculate aspect ratio
            aspect_ratio = image.width / image.height
            
            # Define maximum dimensions
            max_width = 450
            max_height = 450
            
            # Calculate new dimensions maintaining aspect ratio
            if aspect_ratio > 1:
                # Width is greater than height
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:
                # Height is greater than width
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
            
            # Resize image
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            return ImageTk.PhotoImage(image)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            return None

    def browse_file(self):
        """Open file dialog to select an image"""
        filetypes = (
            ('Image files', '*.jpg *.jpeg *.png *.gif *.bmp *.tiff'),
            ('All files', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='Select an image',
            filetypes=filetypes
        )
        
        if filename:
            self.current_file = filename
            self.path_label.config(text=filename)
            self.remove_button.config(state='normal')
            self.status_label.config(text="", fg="black")
            
            # Update image preview
            self.photo = self.load_and_resize_image(filename)
            if self.photo:
                self.preview_label.config(image=self.photo, text="")
            else:
                self.preview_label.config(text="Failed to load image", image="")

    def remove_metadata(self):
        """Remove metadata from the selected image"""
        try:
            # Run ExifTool command
            command = [
                self.exiftool_path,
                '-all=',  # Remove all metadata
                '-overwrite_original',  # Overwrite the original file
                self.current_file
            ]
            
            # Execute the command
            result = subprocess.run(command, 
                                 capture_output=True, 
                                 text=True)
            
            # Check if the command was successful
            if result.returncode == 0:
                self.status_label.config(
                    text="Metadata successfully removed!",
                    fg="green"
                )
                # Refresh the image preview
                self.photo = self.load_and_resize_image(self.current_file)
                if self.photo:
                    self.preview_label.config(image=self.photo)
            else:
                self.status_label.config(
                    text=f"Error: {result.stderr}",
                    fg="red"
                )
                
        except Exception as e:
            self.status_label.config(
                text=f"Error: {str(e)}",
                fg="red"
            )

def main():
    root = tk.Tk()
    app = MetadataRemoverGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
