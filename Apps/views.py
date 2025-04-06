from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm,AuthenticationForm
from django.contrib.auth import login,logout, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.files import File
from .models import Video
import yt_dlp
import os



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


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            associate_user = User.objects.filter(email=email)
            if associate_user.exists():
                for user in associate_user:
                    subject = "Password Reset Request"
                    email_template_name = 'Apps/password_reset_email.html'
                    context = {
                        'email':user.email,
                        'domain':'youtube-downloader-2-z4bz.onrender.com',
                        'site_name':'your website',
                        'uidb64':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':default_token_generator.make_token(user),
                        'protocol':'http',

                    }
                    email_content = render_to_string(email_template_name,context)
                    send_mail(subject, email_content, 'admin@example.com',[user.email],fail_silently=False)
                messages.success(request,'A password resent link has been sent to you')
                return redirect('password_reset_done')
            else:
                messages.error(request,"No user is associated with this  email")
    else:
        form = PasswordResetForm()

    return render(request, "Apps/password_reset_form.html",{'form':form})    

def password_reset_done(request):
    return render(request, 'Apps/password_reset_done.html')


def youtube(request):
    error_message = None

    if request.method == "POST":
        link = request.POST.get('link')

        try:
            download_folder = os.path.join('media', 'videos')  # Use correct path format
            os.makedirs(download_folder, exist_ok=True)  # Ensure the folder exists

            os.environ["PATH"] += os.pathsep + os.path.abspath("Apps/ffmpeg")  # Correct FFmpeg path

            ydl_opts = {
                'format': 'b',  
                'outtmpl': os.path.join(download_folder, '%(id)s.%(ext)s'),  # Use video ID for consistency
                'merge_output_format': 'mp4',
                'postprocessor_args': ['-c:a', 'aac'],
                'verbose': True, 
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=True)
                video_id = info_dict.get('id', 'unknown_id')  # Get video ID
                video_title = info_dict.get('title', 'Unknown Title')

                file_name = f"{video_id}.mp4"
                file_path = os.path.join(download_folder, file_name)

                if not os.path.exists(file_path):  # Check if file exists before opening
                    raise FileNotFoundError(f"Downloaded file not found: {file_path}")

                with open(file_path, 'rb') as f:
                    video_file = File(f)
                    video = Video(user=request.user, title=video_title)
                    video.file.save(file_name, video_file)
                    video.save()

                video_url = video.file.url  # Get stored file URL
                
                

        except Exception as e:
            error_message = f"Error: {str(e)}"

    videos = Video.objects.filter(user=request.user)

    return render(request, 'Apps/youtube.html', {
        'videos': videos,
        'error_message': error_message
    })

def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)


    if video.file:
        if os.path.exists(video.file.path):
            os.remove(video.file.path)
    
    video.delete()
    return redirect('youtube')