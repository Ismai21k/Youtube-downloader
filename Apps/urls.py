from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (PasswordResetConfirmView,PasswordResetCompleteView)

urlpatterns = [
               
               path('pass_reset/', views.password_reset_done, name='password_reset_done'),
               path('reset/', views.password_reset_request, name='password_request_reset'),
               path('delete/<int:video_id>/', views.delete_video, name='delete_video'),
               path('you/', views.youtube, name='youtube'),
               path('', views.user_registration, name='register'),
               path('login/', views.user_login, name='user_login'),
               path('logout/', views.user_logout, name='user_logout'),
               path('rest/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='Apps/password_reset_confirm.html'), name='password_reset_confirm'),
               path("reset/complete/", PasswordResetCompleteView.as_view(template_name="Apps/password_reset_complete.html"), name="password_reset_complete"),

               
               ] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)