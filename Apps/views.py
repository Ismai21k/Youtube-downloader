from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout, authenticate
from .forms import CustomUserCreationForm
import yt_dlp
import os

def test(request):
    return HttpResponse("Hello World! ")

def user_registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            messages.success(request, "Registration successfull")
            return redirect('youtube')
        
        else:    
            messages.error(request, 'Invalid credentials')
        
    else:
        form = CustomUserCreationForm() 
    return render(request, 'Apps/register.html',{'form':form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "login successful!")
                return redirect('youtube')
            else:
                messages.error(request,"Invalid Username or password")
        
        else:
            messages.error(request,"Invalid Username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'Apps/login.html',{'form':form})

def user_logout(request):
    logout(request)
    messages.success(request, "logged out successfully!")
    return redirect('user_login')

 
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