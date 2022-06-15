from django.shortcuts import render,redirect

# Create your views here.
from .models import reader
from .forms import ReaderRegisterForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from reader.serializer import UserSerializer
from books.models import book,shells,reading_record

def ReaderRegister(request):
    if request.method == "POST":
        reader_obj = ReaderRegisterForm(request.POST)
     
        if reader_obj.is_valid():
            reader_obj.save()
            messages.info(request,"reader created")
            return redirect("login")

        else:
            err = reader_obj.errors
            messages.info(request,str(err))
            return redirect("register")
    else:
        content = {"form":ReaderRegisterForm()}
        return render(request,'reader/register.html',content)

def ReaderLogin(request):
    if request.method == "POST":
        pass
    else:
        return render(request,'reader/login.html')
@login_required
def user_settings(request):
    if request.method == "POST":
        user_obj = request.user
        s = UserSerializer(user_obj,request.POST)
        if s.is_valid():
            s.save();
            messages.info(request,"Settings Update")
        else:
            messages.info(request,"Sorry setting not update "+str(s.errors))

    return render(request,"reader/usersettings.html")

@login_required
def profile(request):
    user_obj = request.user
    reader_obj = reader.objects.get(user = user_obj)
    content = {}
    content['books'] = len(book.objects.filter(upload_by=reader_obj))
    content['shell'] = len(shells.objects.filter(upload_by=reader_obj))
    content['followers'] = 0 
    content['reading'] = reading_record.objects.filter(reader =reader_obj)
    readed = 0
    reading_book =[]
    for i in content['reading']:
        reading_book.append(book.objects.get(id=i.book_id))
        if i.progress() >= 98:
            readed = readed+1
    content['red_len'] = len(content['reading'])
    content['readed'] =readed
    content['reading_books'] = reading_book
    print(content)
    return render(request,"reader/profile.html",content)
