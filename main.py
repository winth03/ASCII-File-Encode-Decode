from PIL import Image
import numpy as np
import os
import sys
from tkinter import filedialog
import tkinter as tk

GRID_RES = 1

class Img2Ascii:
    def __init__(self):
        self.char_map = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!l;:,\"^`'. "

    def write_ascii(self, image_path: str, ascii_path: str, message: str, inverted: bool, grid_res: int = GRID_RES) -> None:
        image = Image.open(image_path)
        # image = image.resize((image.width * 10, image.height * 10))
        img_width, img_height = image.size
        pixels = np.array(image.convert('L'))

        with open(message, 'rb') as file:
            file_data = file.read()
            for c in file_data:
                ("-debug" in sys.argv) and print(f"Debug: {format(c, '08b')} {c} {c.to_bytes(1, 'big')}")

        msg_size = len(file_data) + 40
        size_limit = (img_width // grid_res) * (img_height // grid_res)
        if msg_size > size_limit:
            raise ValueError(f"Error: Message Too Long ({msg_size} > {size_limit}") 

        message_length = len(file_data)
        extension = os.path.splitext(message)[1][1:]
        # print(f"Extension: {extension}")
        message = format(message_length, '016b') + ''.join(format(ord(c), '08b') for c in extension) + ''.join(format(c, '08b') for c in file_data)        

        message_index = 0
        char_h, char_w = img_height // grid_res, img_width // grid_res

        with open(ascii_path, 'w', encoding="utf-8-sig") as file:
            file.write("")
            file.flush()
            for y in range(char_h):
                for x in range(char_w):
                    y_start, y_end = y * grid_res, (y + 1) * grid_res
                    x_start, x_end = x * grid_res, (x + 1) * grid_res
                    intensity = np.mean(pixels[y_start:y_end, x_start:x_end])

                    map_value = (intensity / 256.0) * len(self.char_map)
                    offset_bias = round(map_value * 10) % 10
                    map_index = int(map_value)

                    if message_index < len(message):
                        map_index += 0 if message[message_index] == str(map_index % 2) else (1 if offset_bias > 4 else -1)
                        message_index += 1

                    if map_index < 0:
                        map_index = 1
                    elif map_index >= len(self.char_map):
                        map_index = len(self.char_map) - 2
                    curr_char = self.char_map[(len(self.char_map)-map_index-1) if inverted else map_index]
                    file.write(f"{curr_char} ")
                    file.flush()
                file.write('\n')
                file.flush()

    def read_ascii(self, ascii_path: str) -> tuple[bytes, str]:
        with open(ascii_path, 'r', encoding="ascii") as file:
            input_text = file.read()

        if not input_text:
            raise ValueError(f"Error: File Is Empty ({ascii_path})")

        message = ""

        for i in range(16):
            ch = input_text[i*2]
            message += str(self.char_map.index(ch) % 2)

        msg_length = (int(message, 2) + 5) * 8
        debug = message
        message = ""
        extension = ""

        for i in range(16, 40):
            ch = input_text[i*2]
            message += str(self.char_map.index(ch) % 2)
            if len(message) == 8:
                debug += message
                extension += chr(int(message, 2))
                message = ""

        message = bytearray()
        letter = ""
        offset = 0
        i = 40
        while i < msg_length:
            ch = input_text[i*2 + offset]
            if ch == '\n':
                offset += 1
                ("-debug" in sys.argv) and print(f"Debug: Skipping newline")
                continue
            letter += str(self.char_map.index(ch) % 2)
            if len(letter) == 8:
                debug += letter
                byte = int(letter, 2)
                ("-debug" in sys.argv) and print(f"Debug: {ch} {letter} {byte} {byte.to_bytes(1, 'big')}")
                message.append(byte)
                letter = ""
            i += 1
        
        return bytes(message), extension

def main():
    if len(sys.argv) == 2:
        ascii_path = sys.argv[1]
        obj = Img2Ascii()
        try:
            # print(obj.read_ascii(ascii_path))
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