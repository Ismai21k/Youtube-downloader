from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path('', views.test, name='test'),
               path('you/', views.youtube, name='youtube'),
               path('reg/', views.user_registration, name='register'),
               path('login/', views.user_login, name='user_login'),
               path('logout/', views.user_logout, name='user_logout'),
               
               
               ] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)