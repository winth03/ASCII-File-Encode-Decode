# ASCII Steganography Tool

This repository presents a Python project designed for converting images into ASCII art while simultaneously embedding hidden binary files within the generated text. It also aims to provide functionality for extracting these hidden files from the ASCII art.

## Features

*   **Image to ASCII Art Conversion:** Transforms various image formats into detailed ASCII text representations.
*   **Steganographic Embedding:** Conceals arbitrary binary files (such as documents, other images, or executables) directly within the ASCII art by subtly adjusting the chosen characters.
*   **Configurable Character Map:** Employs a comprehensive character set for ASCII rendering, offering flexibility in visual output.
*   **Inverted Output Option:** Supports generating ASCII art with inverted character brightness (e.g., light characters on a dark background or vice-versa).
*   **Binary File Reconstruction:** The project includes a mechanism to reconstruct the embedded binary file and its original extension from a specially encoded ASCII art file.
*   **Graphical User Interface (GUI):** Utilizes `tkinter` for an intuitive user interface, simplifying the encoding and decoding processes.

## Tech Stack

*   **Python:** The core programming language.
*   **Pillow (PIL Fork):** For image loading and manipulation.
*   **NumPy:** For efficient numerical operations, particularly array manipulation of image pixels.
*   **scikit-image:** Specifically `skimage.measure.block_reduce` for image downsampling.
*   **Tkinter:** Python's standard GUI toolkit, used for building the application's interface.

## Prerequisites

Before running this application, ensure you have Python 3.x installed on your system.
You will also need the following Python libraries:

```bash
pip install Pillow numpy scikit-image
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/winth03/ASCII-File-Encode-Decode.git
    cd ASCII-File-Encode-Decode
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt # (assuming requirements.txt would be generated from the above pip install command)
    ```
    *Note: A `requirements.txt` is not provided in the file tree, so the manual `pip install` command for dependencies is used above.*

## Usage

This project is primarily intended to be run via its graphical user interface, which will provide interactive ways to select image files, files to hide, and output locations.

The core logic resides in `main.py` within the `Img2Ascii` class.

### Running the Application (GUI)

While the `display.py` file is present (implying a GUI), a direct command to launch it is not provided. Assuming `display.py` is the entry point for the GUI, you would typically run:

```bash
python display.py
```

This should launch a Tkinter window allowing you to interact with the encoding and decoding functionalities.

### Encoding a File into ASCII Art

The `Img2Ascii.write_ascii` method handles the process of converting an image to ASCII art and embedding a message.

**Example (Illustrative - via GUI or custom script):**

```python
from main import Img2Ascii
import os

# Initialize the encoder/decoder
ascii_converter = Img2Ascii()

# Define paths
image_path = "path/to/your/input_image.jpg"  # e.g., "my_photo.jpg"
message_file_path = "path/to/your/secret_message.txt" # e.g., "hidden.zip"
output_ascii_path = "path/to/your/output_ascii_art.txt" # e.g., "encoded_art.txt"

# Ensure example files exist for demonstration
# You would replace these with your actual files
if not os.path.exists(image_path):
    print(f"Error: Input image not found at {image_path}")
    exit()
if not os.path.exists(message_file_path):
    print(f"Error: Message file not found at {message_file_path}")
    exit()

# Encode the message into ASCII art
# Parameters: input_image_path, output_ascii_path, file_to_hide_path, inverted_colors
ascii_converter.write_ascii(image_path, output_ascii_path, message_file_path, inverted=False)

print(f"Successfully encoded '{message_file_path}' into '{output_ascii_path}' from '{image_path}'")
```

### Decoding a File from ASCII Art

The `Img2Ascii.read_ascii` method is designed to extract the hidden message from an ASCII art file. *Note: The provided `main.py` snippet for `read_ascii` is incomplete, showing only the file reading operation. Full implementation details for message extraction are not available in the given code segment.*

**Example (Illustrative - intended use):**

```python
# from main import Img2Ascii
#
# # Initialize the decoder
# ascii_converter = Img2Ascii()
#
# # Define paths
# encoded_ascii_path = "path/to/your/output_ascii_art.txt" # e.g., "encoded_art.txt"
#
# # Attempt to read the hidden message
# # This method would typically return the decoded bytes and the original file extension
# try:
#     decoded_bytes, original_extension = ascii_converter.read_ascii(encoded_ascii_path)
#     print(f"Successfully decoded message with original extension: .{original_extension}")
#     # You would then write `decoded_bytes` to a file named e.g., "recovered_file.{original_extension}"
# except Exception as e:
#     print(f"Error during decoding: {e}")
```

## Project Structure

```
.
├── .gitignore          # Specifies intentionally untracked files to ignore
├── README.md           # This project's README file
├── display.py          # Likely contains the Tkinter-based graphical user interface
└── main.py             # Contains the core logic for ASCII conversion and steganography (Img2Ascii class)
```

## License

This project currently has no explicit license provided. For details on usage and distribution, please consult the repository owner.