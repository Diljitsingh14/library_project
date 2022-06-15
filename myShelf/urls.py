"""myShelf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from books import views as bv
from django.conf import settings
from django.conf.urls.static import static
from reader import views as reader_view
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', bv.index,name = 'library'),
    path('library/addshell/',bv.addshell,name='add_shell'),
    path('library/get_shell_detail/',bv.getShellDetail,name='get_shell'),
    path('library/addbook/',bv.addbook,name='insert_book'),
    path('library/bookview/<int:id>',bv.pdf_view,name='book_view'),
    path('library/shell/update/',bv.shellupdate,name='shell_update'),
    path('contact_us/',bv.contact_us,name='contact'),
    
    #reader module
    path('reader/register/',reader_view.ReaderRegister,name = 'register'),
    path('reader/login/',views.LoginView.as_view(template_name="reader/login.html"),name = 'login'),
    path('accounts/login/',views.LoginView.as_view(template_name="reader/login.html"),name = 'login'),
    path('reader/logout/',views.LogoutView.as_view(next_page="library"),name = 'logout'),
    path('reader/settings/change_password/',views.PasswordChangeView.as_view(template_name="reader/usersettings.html",success_url="/"),name = 'change_password'),
    path('reader/library/',bv.library,name = 'reader_library'),
    path('reader/settings/',reader_view.user_settings,name = 'user_settings'),
    path('reader/profile/',reader_view.profile,name = 'user_profile'),


    path('book/remember/',bv.remember,name="remember"),
    path('book/like/',bv.book_like,name="book_like"),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
