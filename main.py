'''
This program make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 2023/08/08
Ending 2024//

'''
# Installing the necessary libraries
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Combobox, Radiobutton, Progressbar
import pytesseract
import easyocr
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo
from tkinter import messagebox
# Setting the path to the Tesseract OCR executable (if not installed on the system)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Creating a graphical interface
root = tk.Tk()
root.title("Распознавание текста")
root.geometry("800x600")
# Creating an image display field
image_label = tk.Label(root)
image_label.pack()
# Creating a text field
text_box = tk.Text(root, height=30, width=80)
text_box.pack()

# Function for image display
def display_image(file_path):
    image = Image.open(file_path)
    image = image.resize((400, 400))  # Изменение размера изображения для отображения
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo
# Function for opening a text file
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text = file.read()
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, text)

# Function for extracting text from an image
def extract_text():
    file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.jpeg;*.jpg;*.png")])
    if file_path:
        display_image(file_path)

        selected_engine = engine_var.get()
        if selected_engine == "Tesseract":
            image = Image.open(file_path)
            image = image.convert("RGB")
            image_cv = np.array(image)
            gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)
            text = pytesseract.image_to_string(gray, lang=language_combobox.get())
        elif selected_engine == "EasyOCR":
            reader = easyocr.Reader(['en', 'ru'])
            image = Image.open(file_path)
            text = reader.readtext(np.array(image))

        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, text)
# Updating the Progressbar and displaying a completion message
        progress_bar.step(100)
        showinfo("Распознавание завершено", "Текст успешно извлечен из изображения.")

# Function for saving text to a file
def save_file():
    text = text_box.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Текстовые файлы", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text)
# Function to clear the text field
def clear_text():
    text_box.delete("1.0", tk.END)
# Function for copying text to clipboard
def copy_text():
    text = text_box.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(text)

# Resizing the text field based on the content
def resize_textbox(event):
    text_box.config(height=text_box.index('end - 1 line').split('.')[0])
text_box.bind('<KeyRelease>', resize_textbox)
# Создание Combobox для выбора языка
language_combobox = Combobox(root, values=['eng', 'rus'])
language_combobox.set('eng')
language_combobox.pack()
# Creating a Radiobutton to select the recognition library
engine_var = tk.StringVar()
engine_var.set("Tesseract")
engine_frame = tk.Frame(root)
engine_frame.pack()
engine_label = tk.Label(engine_frame, text="Выберите библиотеку распознавания:")
engine_label.pack()
tesseract_button = Radiobutton(engine_frame, text="Tesseract", variable=engine_var, value="Tesseract")
tesseract_button.pack()
easyocr_button = Radiobutton(engine_frame, text="EasyOCR", variable=engine_var, value="EasyOCR")
easyocr_button.pack()
# Creating buttons
open_button = tk.Button(root, text="Открыть файл", command=open_file)
open_button.pack()
extract_button = tk.Button(root, text="Извлечь текст", command=extract_text)
extract_button.pack()
save_button = tk.Button(root, text="Сохранить файл", command=save_file)
save_button.pack()
clear_button = tk.Button(root, text="Очистить текст", command=clear_text)
clear_button.pack()
copy_button = tk.Button(root, text="Копировать текст", command=copy_text)
copy_button.pack()
# Creating a Progressbar
progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=400, mode='determinate')
progress_bar.pack()


# Program information display function
def show_info():
    messagebox.showinfo("О программе", "Распознавание текста v1.0\nАвтор: Феткулин Григорий")
# Создание главного меню
main_menu = tk.Menu()
file_menu = tk.Menu()
file_menu.add_command(label="Открыть", command=open_file)
file_menu.add_command(label="Сохранить", command=save_file)
main_menu.add_cascade(label="Файл", menu=file_menu)
edit_menu = tk.Menu()
edit_menu.add_command(label="Очистить", command=clear_text)
edit_menu.add_command(label="Копировать", command=copy_text)
main_menu.add_cascade(label="Редактировать", menu=edit_menu)
help_menu = tk.Menu()
help_menu.add_command(label="О программе", command=show_info)
main_menu.add_cascade(label="Справка", menu=help_menu)
root.config(menu=main_menu)
# Starting the main cycle
root.mainloop()
