from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import FileResponse
from PIL import Image
import pytesseract
from gtts import gTTS
import mimetypes
import os
from PyPDF2 import PdfReader
import yt_dlp
import mimetypes
from pathlib import Path



def home(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # Save the uploaded file to the root directory
        with open(uploaded_file.name, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        pdf_name = uploaded_file.name
        my_pdf = PdfReader(pdf_name)
 
        all_text = []
        for page_num, page in enumerate(my_pdf.pages):
            page_text = page.extract_text()
            all_text.append(page_text)

        pdf_text = '\n'.join(all_text)  # Concatenate text from all pages with newline

        tts = gTTS(pdf_text)
        # Save the synthesized speech to an audio file
        tts.save(   f"{pdf_name}.mp3")

        # Return PDF text as HTTP response
        return render(request, 'pdf_text.html', {'extracted_text': pdf_text})

    return render(request, 'home.html')


 

def image_to_text(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        # Save the uploaded file to the root directory
        with open(uploaded_file.name, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        uploaded_image = uploaded_file.name
 
        image = Image.open(uploaded_image)
        
 
        image_text =  pytesseract.image_to_string(image)

  
        # Return PDF text as HTTP response
        return render(request, 'pdf_text.html', {'extracted_text': image_text})

    return render(request, 'image_to_text.html')

 

def image_to_audio(request):
    if request.method == 'POST' and request.FILES.get('file'):
     

        uploaded_file = request.FILES['file']
        # Save the uploaded file to the root directory
        with open(uploaded_file.name, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        uploaded_image = uploaded_file.name
        image = Image.open(uploaded_image)
        
        image_text =  pytesseract.image_to_string(image)
        
        tts = gTTS(image_text)
        # Save the synthesized speech to an audio file
        mp3_file_path = f"{uploaded_image}.mp3"
        tts.save(mp3_file_path)


        started = True

        # Set the appropriate content type for the MP3 file
        content_type, _ = mimetypes.guess_type(mp3_file_path)
        response = FileResponse(open(mp3_file_path, 'rb'), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{uploaded_image}.mp3"'
        print('done converting ')

        return  response

    else :

        return render(request, 'image_to_audio.html' )




 

BASE_DIR = Path(__file__).resolve().parent.parent
output_path = BASE_DIR
def delete_file(the_file):
    if os.path.exists(the_file) :
        os.remove(the_file)
    else :
        pass 

def dow(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        download_format = request.POST.get('the_format')

        # Options for yt_dlp (YouTube Downloader)
        video = {
            'format': 'best',  # Select the best available format
            'outtmpl': str(output_path / '%(title)s.%(ext)s'),  # Output file template
            'quiet': True,  # Suppress output messages
        }

        audio = {
            'format': 'bestaudio/best',  # Select the best audio quality
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
                'preferredcodec': 'mp3',  # Convert to MP3 format
                'preferredquality': '192',  # Set audio quality
            }],
            'outtmpl': str(output_path / '%(title)s.%(ext)s'),  # Output file template
            'quiet': True,  # Suppress output messages
            'ffmpeg_location': "/usr/bin/ffmpeg",  # Replace with your location of FFmpeg executable
        }

        if download_format == "Audio":
            download_format = audio
            extension = "mp3"  # Set extension to MP3 for audio format
        elif download_format == "Video":
            download_format = video
            extension = "mp4"  # Set extension to MP4 for video format
 
        try:
            with yt_dlp.YoutubeDL(download_format) as ydl:
                ydl.download([url])  # Download the video/audio
                info = ydl.extract_info(url, download=False)
                title_with_extension = f"{info['title']}.{extension}"  # Use the specified extension
                file_path = output_path / title_with_extension
                print(f"File path: {file_path}")  # Debugging statement
                if os.path.exists(file_path):
                    content_type, _ = mimetypes.guess_type(file_path)
                    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
                    response['Content-Disposition'] = f'attachment; filename="{title_with_extension}"'
                    return response
                else:
                    print("File does not exist")  # Debugging statement
            if os.path.exists(the_file) :
                os.remove(the_file)
            print('the file is deleted ___________------><')
        except Exception as e:
            print(f"Failed to download {url}: {e}")

    return render(request, 'dow.html')
