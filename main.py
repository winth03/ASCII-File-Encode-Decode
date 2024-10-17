from PIL import Image
import numpy as np
import os
import sys
from tkinter import filedialog
import tkinter as tk
from skimage.measure import block_reduce

GRID_RES = 1

class Img2Ascii:
    def __init__(self):
        self.char_map = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!l;:,\"^`'. "

    def write_ascii(self, image_path: str, ascii_path: str, message: str, inverted: bool, grid_res: int = GRID_RES) -> None:
        # Load and prepare image
        image = Image.open(image_path)
        pixels = np.array(image.convert('L'))
        reduced = block_reduce(pixels, grid_res, np.mean)
        
        # Read message file and prepare binary message
        with open(message, 'rb') as file:
            file_data = file.read()
        
        # Prepare the binary message (same as original)
        extension = os.path.splitext(message)[1][1:]
        b_message = ''.join(format(c, '08b') for c in file_data)
        b_extension = ''.join(format(ord(c), '08b') for c in extension)
        
        extension_length = len(b_extension)
        message_length = len(b_message) + 32 + 8 + extension_length
        
        full_message = format(message_length, '032b') + format(extension_length, '08b') + b_extension + b_message
        print(message_length, len(full_message))
        
        # Vectorized mapping
        char_h, char_w = reduced.shape
        
        # Step 1: Calculate base mapping values
        map_values = (reduced / 256.0) * len(self.char_map)
        offset_bias = np.round(map_values * 10) % 10
        map_indices = map_values.astype(int)
        
        # Step 2: Prepare message array
        msg_array = np.pad(np.array([int(bit) for bit in full_message], dtype=int), (0, char_h * char_w - len(full_message)), 'constant', constant_values=0)
        msg_array = msg_array.reshape(char_h, char_w)
        
        # Step 3: Create a mask for pixels that need modification
        need_modification = (msg_array != (map_indices % 2)).astype(bool)
        
        # Step 4: Apply modifications
        adjustments = np.where(offset_bias > 4, 1, -1)
        map_indices = np.where(need_modification, map_indices + adjustments, map_indices)
        
        # Step 5: Clip values
        map_indices[map_indices < 0] = 1
        map_indices[map_indices >= len(self.char_map)] = len(self.char_map) - 2
        
        # Step 6: Handle inversion
        if inverted:
            map_indices = len(self.char_map) - map_indices - 1
        
        # Step 7: Convert to characters and write to file
        with open(ascii_path, 'w', encoding="utf-8-sig") as file:
            for y in range(char_h):
                line = ""
                for x in range(char_w):
                    line += f"{self.char_map[map_indices[y, x]]} "
                file.write(line + '\n')

    def read_ascii(self, ascii_path: str) -> tuple[bytes, str]:
        with open(ascii_path, 'r', encoding="utf-8-sig") as file:
            input_text = file.read()

        if not input_text:
            raise ValueError(f"Error: File Is Empty ({ascii_path})")

        message = ""

        for i in range(32):
            ch = input_text[i*2]
            message += str(self.char_map.index(ch) % 2)

        msg_length = int(message, 2)
        message = ""

        for i in range(32, 40):
            ch = input_text[i*2]
            message += str(self.char_map.index(ch) % 2)

        ext_length = int(message, 2)
        message = ""
        extension = ""

        for i in range(40, 40 + ext_length):
            ch = input_text[i*2]
            message += str(self.char_map.index(ch) % 2)
            if len(message) == 8:
                extension += chr(int(message, 2))
                message = ""

        message = bytearray()
        letter = ""
        offset = 0
        i = 40 + ext_length
        while i < msg_length:
            ch = input_text[i*2 + offset]
            if ch == '\n':
                offset += 1
                continue
            letter += str(self.char_map.index(ch) % 2)
            if len(letter) == 8:
                byte = int(letter, 2)
                message.append(byte)
                letter = ""
            i += 1
        
        return bytes(message), extension

def main():
    if len(sys.argv) == 2:
        ascii_path = sys.argv[1]
        obj = Img2Ascii()
        try:
            data, extension = obj.read_ascii(ascii_path)
            file_name = filedialog.asksaveasfilename(title="Save File", filetypes=[("Files", f"*.{extension}")], initialfile=f"decoded.{extension}", defaultextension=extension)
            with open(file_name, 'wb') as file:
                file.write(data)
                print(f"Success! : Output saved to ({os.path.abspath(file.name)})")
        except Exception as e:
            print(f"Error: {e}")
    elif len(sys.argv) == 4:
        inverted = int(sys.argv[1]) == 1
        image_path = sys.argv[2]
        message = sys.argv[3]
        ascii_path = filedialog.asksaveasfilename(title="Save File", filetypes=[("Text Files", "*.txt")], defaultextension=".txt")
        # ascii_path = "output.txt"
        obj = Img2Ascii()
        try:
            obj.write_ascii(image_path, ascii_path, message, inverted)
            print(f"Success! : Output saved to ({os.path.abspath(ascii_path)})")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Usage -")
        print("Encode: python img2ascii.py [Inverted(0/1)] [ImageFilePath] [MESSAGE]")
        print("        Example - python img2ascii.py 0 \"./sampleImageFile.png\" \"Hello, World!\"")
        print("Decode: python img2ascii.py [TextFilePath]")
        print("        Example - python img2ascii.py \"./outputTextFile.txt\"")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    mode = input("Encode or Decode? (e/d): ").lower()

    if mode == "e":
        image_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        # message = input("Enter message to hide: ")
        message = filedialog.askopenfilename(title="Select File to encode", filetypes=[("Files", "*.png *.jpg *.txt")])
        # inverted = input("Invert image? (y/n): ").lower() == "y"
        inverted = False

        sys.argv = [sys.argv[0], int(inverted), image_path, message]

    elif mode == "d":
        ascii_path = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text Files", "*.txt")])
        sys.argv = [sys.argv[0], ascii_path]

    main()