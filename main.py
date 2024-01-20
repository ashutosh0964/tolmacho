from tkinter import *
from tkinter import ttk, filedialog
import googletrans
import textblob
import pyttsx3
import PyPDF2
import tkinter.messagebox

def translate_it():
    # Delete Any Previous Translations
    translated_text.delete(1.0, END)

    try:
        # Get Languages From Dictionary Keys
        # Get the From Language Key
        for key, value in languages.items():
            if value == original_combo.get():
                from_language_key = key

        # Get the To Language Key
        for key, value in languages.items():
            if value == translated_combo.get():
                to_language_key = key

        # Turn Original Text into a TextBlob
        words = textblob.TextBlob(original_text.get(1.0, END))

        # Translate Text
        words = words.translate(from_lang=from_language_key, to=to_language_key)

        # Output translated text to screen
        translated_text.insert(1.0, words)

        # Initialize the speech engine
        engine = pyttsx3.init()

        # Set the language for Text-to-Speech (replace 'hi' with the appropriate language code for Hindi)
        engine.setProperty('voice', f'{to_language_key}-utf8')
        engine.setProperty('rate', 150)  # Adjust the speed of speech if needed

        # Pass text to speech engine
        engine.say(words)

        # Run to the engine
        engine.runAndWait()

    except Exception as e:
        tkinter.messagebox.showerror("Translator", e)

def clear():
    # Clear the text boxes
    original_text.delete(1.0, END)
    translated_text.delete(1.0, END)

def open_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            pdf_text = ""
            for page_num in range(len(pdf_reader.pages)):
                pdf_text += pdf_reader.pages[page_num].extract_text()

        # Insert PDF text into the original_text Text widget
        original_text.delete(1.0, END)
        original_text.insert(1.0, pdf_text)

# Grab Language List From GoogleTrans
languages = googletrans.LANGUAGES
language_list = list(languages.values())

# GUI Setup
root = Tk()
root.title('Translator')
root.geometry("880x300")

# Text Boxes
original_text = Text(root, height=10, width=40)
original_text.grid(row=0, column=0, pady=20, padx=10)

translate_button = Button(root, text="Translate!", font=("Helvetica", 24), command=translate_it)
translate_button.grid(row=0, column=1, padx=10)

translated_text = Text(root, height=10, width=40)
translated_text.grid(row=0, column=2, pady=20, padx=10)

# Combo boxes
original_combo = ttk.Combobox(root, width=50, value=language_list)
original_combo.current(21)
original_combo.grid(row=1, column=0)

translated_combo = ttk.Combobox(root, width=50, value=language_list)
translated_combo.current(38)
translated_combo.grid(row=1, column=2)

# Clear button
clear_button = Button(root, text="Clear", command=clear)
clear_button.grid(row=2, column=1)

# PDF button
pdf_button = Button(root, text="Open PDF", command=open_pdf)
pdf_button.grid(row=3, column=1)

root.mainloop()