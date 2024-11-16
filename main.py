'''
This program make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 2023/08/08
Ending 2024//

'''
# Installing the necessary libraries
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox, Radiobutton, Progressbar
import pytesseract
import easyocr
import cv2
import numpy as np
from PIL import Image, ImageTk


class TextRecognitionEngine:
    """AI is creating summary for
    """
    def __init__(self):
        self.language = 'eng'

    def set_language(self, language):
        """AI is creating summary for set_language

        Args:
            language ([type]): [description]
        """
        self.language = language

    def extract_text(self, image_path):
        """AI is creating summary for extract_text

        Args:
            image_path ([type]): [description]

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError("Метод extract_text должен быть переопределен в дочернем классе.")


class TesseractEngine(TextRecognitionEngine):
    """AI is creating summary for TesseractEngine

    Args:
        TextRecognitionEngine ([type]): [description]
    """
    def __init__(self):
        super().__init__()
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    def extract_text(self, image_path):
        """AI is creating summary for extract_text

        Args:
            image_path ([type]): [description]

        Returns:
            [type]: [description]
        """
        image = Image.open(image_path).convert("RGB")
        image_cv = np.array(image)
        gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)
        return pytesseract.image_to_string(gray, lang=self.language)


class EasyOCREngine(TextRecognitionEngine):
    """AI is creating summary for EasyOCREngine

    Args:
        TextRecognitionEngine ([type]): [description]
    """
    def __init__(self):
        super().__init__()
        self.reader = easyocr.Reader(['en', 'ru'])

    def extract_text(self, image_path):
        """AI is creating summary for extract_text

        Args:
            image_path ([type]): [description]

        Returns:
            [type]: [description]
        """
        image = Image.open(image_path)
        results = self.reader.readtext(np.array(image))
        return ' '.join([res[1] for res in results])


class TextRecognitionApp:
    """AI is creating summary for
    """
    def __init__(self, root):
        # Initialization of the main application frame
        self.root = root
        self.root.title("Распознавание текста")
        self.root.geometry("800x600")

        # Default engine initialization (Tesseract)
        self.engine = TesseractEngine()

        # Create GUI components
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        """AI is creating summary for create_widgets
        """
        # Image display field
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Text field
        self.text_box = tk.Text(self.root, height=30, width=80)
        self.text_box.pack()

        # Language selection Combobox
        self.language_combobox = Combobox(self.root, values=['eng', 'rus'])
        self.language_combobox.set('eng')
        self.language_combobox.pack()

        # Engine selection Radiobuttons
        self.engine_var = tk.StringVar(value="Tesseract")
        self.engine_frame = tk.Frame(self.root)
        self.engine_frame.pack()
        tk.Label(self.engine_frame, text="Выберите библиотеку распознавания:").pack()
        Radiobutton(self.engine_frame, text="Tesseract", variable=self.engine_var, value="Tesseract", command=self.set_engine).pack()
        Radiobutton(self.engine_frame, text="EasyOCR", variable=self.engine_var, value="EasyOCR", command=self.set_engine).pack()

        # Buttons
        tk.Button(self.root, text="Открыть файл", command=self.open_file).pack()
        tk.Button(self.root, text="Извлечь текст", command=self.extract_text).pack()
        tk.Button(self.root, text="Сохранить файл", command=self.save_file).pack()
        tk.Button(self.root, text="Очистить текст", command=self.clear_text).pack()
        tk.Button(self.root, text="Копировать текст", command=self.copy_text).pack()

        # Progressbar
        self.progress_bar = Progressbar(self.root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress_bar.pack()

        # Binding a text field resizing event
        self.text_box.bind('<KeyRelease>', self.resize_textbox)

    def create_menu(self):
        """AI is creating summary for create_menu
        """
        main_menu = tk.Menu()

        file_menu = tk.Menu(main_menu, tearoff=0)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        main_menu.add_cascade(label="Файл", menu=file_menu)

        edit_menu = tk.Menu(main_menu, tearoff=0)
        edit_menu.add_command(label="Очистить", command=self.clear_text)
        edit_menu.add_command(label="Копировать", command=self.copy_text)
        main_menu.add_cascade(label="Редактировать", menu=edit_menu)

        help_menu = tk.Menu(main_menu, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_info)
        main_menu.add_cascade(label="Справка", menu=help_menu)

        self.root.config(menu=main_menu)

    def display_image(self, file_path):
        """AI is creating summary for display_image

        Args:
            file_path ([type]): [description]
        """
        image = Image.open(file_path).resize((400, 400))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def open_file(self):
        """AI is creating summary for open_file
        """
        file_path = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                text = file.read()
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, text)

    def extract_text(self):
        """AI is creating summary for extract_text
        """
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.jpeg;*.jpg;*.png")])
        if file_path:
            self.display_image(file_path)
            self.engine.set_language(self.language_combobox.get())
            text = self.engine.extract_text(file_path)

            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, text)
            self.progress_bar.step(100)
            messagebox.showinfo("Распознавание завершено", "Текст успешно извлечен из изображения.")

    def save_file(self):
        """AI is creating summary for save_file
        """
        text = self.text_box.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Текстовые файлы", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(text)

    def clear_text(self):
        """AI is creating summary for clear_text
        """
        self.text_box.delete("1.0", tk.END)

    def copy_text(self):
        """AI is creating summary for copy_text
        """
        text = self.text_box.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def resize_textbox(self, event):
        """AI is creating summary for resize_textbox

        Args:
            event ([type]): [description]
        """
        self.text_box.config(height=self.text_box.index('end-1c').split('.')[0])

    def show_info(self):
        """AI is creating summary for show_info
        """
        messagebox.showinfo("О программе", "Распознавание текста v1.0\nАвтор: Феткулин Григорий")

    def set_engine(self):
        """AI is creating summary for set_engine
        """
        engine_name = self.engine_var.get()
        if engine_name == "Tesseract":
            self.engine = TesseractEngine()
        elif engine_name == "EasyOCR":
            self.engine = EasyOCREngine()


if __name__ == "__main__":
    root = tk.Tk()
    app = TextRecognitionApp(root)
    root.mainloop()
