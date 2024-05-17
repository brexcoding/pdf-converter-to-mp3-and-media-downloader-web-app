import os
import PyPDF2
from PyPDF2 import PdfReader
from pathlib import Path
 # pdf_to_audio()
from gtts import gTTS

 
import pytesseract
from PIL import Image

# Open the image file
image = Image.open('pic.png')

# Use pytesseract to extract text
extracted_text = pytesseract.image_to_string(image)

# Print the extracted text
print(extracted_text)

# my_pdf = PdfReader("djangoapibook.pdf")
# print(type(my_pdf))

# number_of_pages = len(my_pdf.pages)
 
# def pdf_to_audio():
     
#     all_text = []
#     for page_num, page in enumerate(my_pdf.pages):
#         page_text = page.extract_text()
#         all_text.append(page_text)

#     pdf_text = str(all_text)
 
#     engine = pyttsx3.init()
#     engine.say(pdf_text)
#     engine.runAndWait()

# # Text to be converted to speech
# text = "Hello, this is the audio file sir , should be a bit short but thats waht we need ot test ?"

# # Create a gTTS instance with the text
# tts = gTTS(text)

# # Save the synthesized speech to an audio file
# tts.save("output.mp3")
