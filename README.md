# MetadataRemover
A simple Python GUI application to remove metadata from image files using ExifTool.

## Overview

This application provides a user-friendly interface to easily strip metadata from image files. It utilizes the `tkinter` library for the GUI and `ExifTool` for the actual metadata removal.  An image preview is provided to ensure the correct file is being processed.

## Features

- **GUI Interface:** Intuitive and easy-to-use graphical interface.
- **File Selection:** Allows browsing and selection of image files.
- **Image Preview:** Displays a preview of the selected image.
- **Metadata Removal:** Removes all metadata from the selected image file using ExifTool.
- **Status Updates:** Provides real-time status updates on the operation's progress.
- **Error Handling:** Gracefully handles common errors, such as ExifTool not being found or issues with image loading.
- **Cross-Platform Compatibility:**  Written in Python and can be run on any platform with Python and tkinter support.  Packaging as an executable for Windows is described below.

## Prerequisites

Before using this application, ensure you have the following installed:

- **Python:** (version 3.6 or higher)
- **ExifTool:** Download and install ExifTool from [https://exiftool.org/](https://exiftool.org/). Ensure the installation directory is added to your system's PATH environment variable *or* specify the path explicitly in the script (default is `C:\Program Files\ExifTool\exiftool.exe`).
- **Pillow (PIL):** Install the Python Imaging Library (Pillow) using pip:

  ```bash
  pip install Pillow
  ```

## Installation

1. **Download the script:** directly download the `metadata_remover.py` file.

2. **Install Dependencies:** `pip install Pillow`

## Usage

1. **Run the script:**
   ```bash
   python metadata_remover.py
   ```

2. **Select an Image:** Click the "Browse Image" button to select an image file from your computer.

3. **Remove Meta** Once an image is selected, the "Remove Metadata" button will be enabled. Click it to remove all metadata from the image.

4. **View Status:** The application will display a status message indicating whether the metadata removal was successful or if any errors occurred. The image preview will also refresh.

## Code Structure

- `metadata_remover.py`: The main Python script containing the GUI application.

## Explanation of Key Code Sections

### Initialization and GUI Setup

```python
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import os

class MetadataRemoverGUI:
    def __init__(self, root):
        # ... (GUI setup and widget creation) ...
```

This section initializes the `tkinter` window and sets up the GUI elements, including buttons, labels, and the image preview area.

### Image Loading and Preview

```python
def load_and_resize_image(self, image_path):
    """Load and resize image to fit the preview frame"""
    try:
        image = Image.open(image_path)
        # ... (resize logic) ...
        return ImageTk.PhotoImage(image)
    except Exception as e:
        # ... (error handling) ...
        return None
```

This function loads an image using the `PIL` library, resizes it while preserving aspect ratio, and returns a `PhotoImage` object for displaying in the GUI.  Error handling is included to catch potential issues when opening or processing the image file.

### Metadata Removal

```python
def remove_metadata(self):
    """Remove metadata from the selected image"""
    try:
        command = [
            self.exiftool_path,
            '-all=',  # Remove all metadata
            '-overwrite_original',  # Overwrite the original file
            self.current_file
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        # ... (status update logic) ...
    except Exception as e:
        # ... (error handling) ...
```

This function removes metadata using `ExifTool`. It constructs the command, executes it via `subprocess`, and updates the GUI with the operation's result.  The `-overwrite_original` option will directly modify the original file. If you don't want this behavior, remove the option.

## Configuration

- **ExifTool Path:**  The default path to ExifTool is set to `C:\Program Files\ExifTool\exiftool.exe`. If you installed ExifTool in a different location, modify the `exiftool_path` variable in the script.
   ```python
   self.exiftool_path = r"C:\Program Files\ExifTool\exiftool.exe"
   ```

## Creating an Executable (Windows)

You can create a standalone executable for Windows using PyInstaller. This allows you to run the application without needing Python installed.

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Create the executable:**
   ```bash
   pyinstaller --onefile --windowed --hidden-import='PIL._tkinter_finder' metadata_remover.py
   ```
   * `--onefile`: Creates a single executable file.
   * `--windowed`: Creates a windowed application (no console window).
   * `--hidden-import='PIL._tkinter_finder'`:  This is crucial for Pillow/PIL to work correctly within the bundled executable.

3. **Find the executable:** The executable will be created in the `dist` folder.
