# ASCII File Encode/Decode

A lightweight Python utility designed to encode standard files into ASCII text representations and decode them back to their original file formats. 

This tool is useful for securely transferring or storing non-text files in text-only environments, understanding data serialization, or exploring how binary-to-text encoding works under the hood.

## 🚀 Features

* **File Encoding:** Convert binary or text files into an ASCII-encoded text format.
* **File Decoding:** Reconstruct original files accurately from their ASCII-encoded text.
* **Command-Line Interface:** Easy to use and interact with directly from your terminal.
* **Modular Design:** Separation of core logic (`main.py`) and user interface/output handling (`display.py`).

## 📂 Project Structure

* `main.py` - The entry point of the application. Contains the core logic for routing the user's encoding/decoding requests.
* `display.py` - Handles the presentation layer, such as printing the UI, progress bars, or console output.
* `.gitignore` - Specifies intentionally untracked files to ignore.

## 🛠️ Prerequisites

To run this tool, you need to have Python installed on your system.
* [Python 3.x](https://www.python.org/downloads/)

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/winth03/ASCII-File-Encode-Decode.git](https://github.com/winth03/ASCII-File-Encode-Decode.git)
   ```
2. **Navigate to the project directory:**
   ```bash
   cd ASCII-File-Encode-Decode
   ```

## 💻 Usage

Run the main script using Python. The application will guide you through prompts, or you can pass arguments directly (depending on your specific implementation).

```bash
python main.py
```

### Example Workflow
1. **To Encode a File:**
   * Select the "Encode" option when running the script.
   * Provide the path to the input file (e.g., `image.png` or `document.pdf`).
   * The program will output an encoded `.txt` file containing the ASCII representation.

2. **To Decode a File:**
   * Select the "Decode" option.
   * Provide the path to the encoded ASCII `.txt` file.
   * The program will process the text and restore the original file.
