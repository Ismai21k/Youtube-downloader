from django.shortcuts import render
from django.http import HttpResponse
import yt_dlp
import os

def test(request):
    return HttpResponse("Hello World! ")

from django.shortcuts import render
from django.http import HttpResponse
import yt_dlp
import os

def youtube(request):
    video_url = None
    error_message = None

    if request.method == "POST":
        link = request.POST.get('link')

        try:
            download_folder = 'Apps/downloads'
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)

            # Force yt-dlp to find FFmpeg
            os.environ["PATH"] += os.pathsep + "C:\\Users\\excit\\Downloads\\bin"

            ydl_opts = {
                'format': 'b',  # Select the best quality format that contains both video and audio. Equivalent to best*[vcodec!=none][acodec!=none]
                'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',          # Ensure final output is MP4
                'postprocessor_args': ['-c:a', 'aac'],  # Re-encode audio to AAC for compatibility
                
                'verbose': True, 
                #'--no-part': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=True)
                video_path = info_dict["requested_downloads"][0]["filepath"]
                video_url = f"/media/{os.path.basename(video_path)}"

        except Exception as e:
            error_message = f"Error: {str(e)}"

    return render(request, 'Apps/youtube.html', {
        'video_url': video_url,
        'error_message': error_message
    })