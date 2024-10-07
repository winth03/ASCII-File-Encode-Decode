import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from main import Img2Ascii, GRID_RES
import time
import threading

def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]+'B'}"

class Img2AsciiGUI:
	def __init__(self, master):
		self.master = master
		self.master.title("Image to ASCII Converter")
		self.master.geometry("1200x800")
		self.master.configure(bg="#f0f0f0")

		self.img2ascii = Img2Ascii()
		self.image_path = ""
		self.file_to_hide = ""

		self.size_limit = -1
		
		self.create_widgets()

	def create_widgets(self):
		# สร้าง style สำหรับปุ่ม
		style = ttk.Style()
		style.theme_use('clam')
		style.configure('TButton', font=('Arial', 12, 'bold'), padding=10, width=15)
		style.map('TButton',
					foreground=[('pressed', 'white'), ('active', 'blue')],
					background=[('pressed', '!disabled', 'black'), ('active', 'white')])

		# Frame สำหรับปุ่มด้านบน
		top_frame = tk.Frame(self.master, bg="#f0f0f0")
		top_frame.pack(pady=20)

		# ปุ่มเพิ่มรูปภาพ
		self.add_image_btn = ttk.Button(top_frame, text="Add Image", command=self.add_image, style='TButton')
		self.add_image_btn.pack(side=tk.LEFT, padx=10)

		# ปุ่มเพิ่มไฟล์ที่จะซ่อน
		self.add_file_btn = ttk.Button(top_frame, text="Add File to Hide", command=self.add_file, style='TButton')
		self.add_file_btn.pack(side=tk.LEFT, padx=10)

		# ปุ่ม Encode
		self.encode_btn = ttk.Button(top_frame, text="Encode", command=self.encode, style='TButton')
		self.encode_btn.pack(side=tk.LEFT, padx=10)

		# ปุ่ม Decode
		self.decode_btn = ttk.Button(top_frame, text="Decode", command=self.decode, style='TButton')
		self.decode_btn.pack(side=tk.LEFT, padx=10)

		# สร้าง Tooltip สำหรับปุ่ม
		self.create_tooltip(self.add_image_btn, "Select an image to convert")
		self.create_tooltip(self.add_file_btn, "Select a file to hide in the image")
		self.create_tooltip(self.encode_btn, "Convert image to ASCII and hide file")
		self.create_tooltip(self.decode_btn, "Extract hidden file from ASCII")

		# Frame สำหรับแสดงรูปภาพ
		image_frame = tk.Frame(self.master)
		image_frame.pack(pady=20, padx=5, expand=True, fill=tk.BOTH)

		# Frame สำหรับ ASCII preview และ Original image
		ascii_container = tk.Frame(image_frame)
		ascii_container.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

		# Frame สำหรับรูปภาพต้นฉบับ
		self.original_frame = tk.Frame(ascii_container, bg="white", width=550, height=400, bd=2, relief=tk.SOLID)
		self.original_frame.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.BOTH, anchor=tk.SW)

		# Label สำหรับแสดงรูปภาพต้นฉบับ
		self.original_label = tk.Label(self.original_frame, bg="white")
		self.original_label.pack(expand=True, fill=tk.BOTH)

		# Label สำหรับ size limit
		self.size_limit_label = tk.Label(image_frame, text=f"File to hide size limit: {format_bytes(self.size_limit) if self.size_limit >= 0 else "-"}")
		self.size_limit_label.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)

      	# ปุ่ม Copy
		self.copy_btn = ttk.Button(image_frame, text="Copy", command=self.copy_ascii, width=5)
		self.copy_btn.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NE)

		# Frame สำหรับ ASCII preview
		self.ascii_frame = tk.Frame(ascii_container, bg="white", width=550, height=400, bd=2, relief=tk.SOLID)
		self.ascii_frame.pack(side=tk.RIGHT, padx=5, expand=True, fill=tk.BOTH, anchor=tk.SE)

		# Text widget สำหรับแสดง ASCII preview
		self.ascii_text = tk.Text(self.ascii_frame, wrap=tk.NONE, font=("Courier", 4))
		self.ascii_text.grid(row=0, column=0, sticky="nsew")

		# Scrollbar สำหรับ ASCII preview
		x_scrollbar = ttk.Scrollbar(self.ascii_frame, orient=tk.HORIZONTAL, command=self.ascii_text.xview)
		x_scrollbar.grid(row=1, column=0, sticky="ew")
		y_scrollbar = ttk.Scrollbar(self.ascii_frame, orient=tk.VERTICAL, command=self.ascii_text.yview)
		y_scrollbar.grid(row=0, column=1, sticky="ns")

		self.ascii_text.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

		# ทำให้ grid ขยายตัวได้
		self.ascii_frame.grid_rowconfigure(0, weight=1)
		self.ascii_frame.grid_columnconfigure(0, weight=1)

		# Frame สำหรับแสดงผลลัพธ์
		self.result_frame = tk.Frame(self.master, bg="#f0f0f0", bd=0, relief=tk.SOLID)
		self.result_frame.pack(pady=20, padx=10, fill=tk.X)

		# Text widget สำหรับแสดงผลลัพธ์
		self.result_text = tk.Text(self.result_frame, height=10, width=120, bg="#f0f0f0")
		self.result_text.pack(pady=5, padx=5)
	
	def copy_ascii(self):
		ascii_content = self.ascii_text.get("1.0", tk.END)
		self.master.clipboard_clear()
		self.master.clipboard_append(ascii_content)
		messagebox.showinfo("Copied", "ASCII content has been copied to clipboard.")
      
	def create_tooltip(self, widget, text):
		def enter(event):
			self.tooltip = tk.Toplevel(widget)
			self.tooltip.overrideredirect(True)
			self.tooltip.geometry(f"+{event.x_root+15}+{event.y_root+10}")
			label = tk.Label(self.tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
			label.pack()

		def leave(event):
			if hasattr(self, 'tooltip'):
				self.tooltip.destroy()

		widget.bind("<Enter>", enter)
		widget.bind("<Leave>", leave)


	def add_image(self):
		self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
		if self.image_path:
			self.display_image(self.image_path, self.original_label)
			self.result_text.insert(tk.END, f"Image added: {self.image_path}\n")

			img_width, img_height = Image.open(self.image_path).size
			self.size_limit = (img_width // GRID_RES) * (img_height // GRID_RES) - 40
			self.size_limit_label.configure(text=f"File to hide size limit: {format_bytes(self.size_limit) if self.size_limit >= 0 else "-"}")

	def add_file(self):
		self.file_to_hide = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
		if self.file_to_hide:
			# Check if file is too big
			with open(self.file_to_hide, "rb") as file:
				file_data = file.read()
			if len(file_data) > self.size_limit:
				self.result_text.insert(tk.END, f"File need to be less than: {format_bytes(self.size_limit)}\n")
				messagebox.showerror("Error", f"Please select file with size less than {format_bytes(self.size_limit)}")
				return
			
			self.result_text.insert(tk.END, f"File to hide: {self.file_to_hide}\n")

	def encode(self):
		if not self.image_path or not self.file_to_hide:
			messagebox.showerror("Error", "Please select both an image and a file to hide.")
			return

		try:
			ascii_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
			if ascii_path:
				start_time = time.time_ns()
				self.img2ascii.write_ascii(self.image_path, ascii_path, self.file_to_hide, False)
				stop_time = time.time_ns()
				self.result_text.insert(tk.END, f"Encoded successfully in {stop_time - start_time} ns. Output saved to: {ascii_path}\n")
				with open(ascii_path, 'r', encoding='utf-8') as file:
					ascii_content = file.read()		
				self.ascii_text.delete(1.0, tk.END)
				self.ascii_text.insert(tk.END, ascii_content)	
		except Exception as e:
			messagebox.showerror("Error", str(e))

	def decode(self):
		ascii_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
		if ascii_path:
			try:
				start_time = time.time_ns()
				data, extension = self.img2ascii.read_ascii(ascii_path)
				stop_time = time.time_ns()
				save_path = filedialog.asksaveasfilename(defaultextension=f".{extension}", filetypes=[(f"{extension.upper()} files", f"*.{extension}")])
				if save_path:
					with open(save_path, 'wb') as file:
						file.write(data)
					self.result_text.insert(tk.END, f"Decoded successfully in {stop_time - start_time} ns. File saved to: {save_path}\n")
			except Exception as e:
				messagebox.showerror("Error", str(e))

	def display_image(self, path, label):
		image = Image.open(path)
		image.thumbnail((550, 400))  # Resize image to fit the frame
		photo = ImageTk.PhotoImage(image)
		label.config(image=photo)
		label.image = photo  # Keep a reference

def main():
  root = tk.Tk()
  app = Img2AsciiGUI(root)
  root.mainloop()

if __name__ == "__main__":
  main()