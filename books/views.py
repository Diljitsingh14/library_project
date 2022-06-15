from django.shortcuts import render,redirect,HttpResponse,Http404
from books.forms import shell_form
from django.contrib import messages
from books.models import shells,book,reading_record
from django.views.decorators.clickjacking import xframe_options_sameorigin
from PyPDF2 import PdfFileWriter, PdfFileReader
from reader.models import reader
from .serializer import shellSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import json
from django.contrib.auth.decorators import login_required
from reader.forms import ContactForm
from django.http import JsonResponse

def contact_us(request):
    if request.method == "POST":
        CF = ContactForm(request.POST)
        if CF.is_valid():
            CF.save()
            messages.info(request,"Thank you , Your request is submit...")
        else:
            messages.info(request,"sorry your request is not submit due to "+str(CF.errors))
        CF = ContactForm()
        return render(request,"contact.html",{"form":CF})
    else:
        CF = ContactForm()
        return render(request,"contact.html",{"form":CF})


def create_thumbnail(file):
    file = "media/"+file
    inputpdf = PdfFileReader(open(file, "rb"))
    file = file[:-4]+"front.pdf"
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(0))
    with open(file, "wb") as outputStream:
        output.write(outputStream)

# Create your views here.
@xframe_options_sameorigin
def index(request):
    all_shell = shells.objects.all().filter(privacy=False)
    compress =[]
    for shell in all_shell:
        compress.append(book.objects.filter(shell_id = shell.id))
    sz = zip(all_shell,compress)    
    content = {
        'sz':sz

    }
    return render(request,'books/index.html',content)

@login_required
def library(request):
    reader_obj = reader.objects.get(user=request.user.id)
    all_shell = shells.objects.filter(upload_by=reader_obj.id)
    compress =[]
    for shell in all_shell:
        compress.append(book.objects.filter(shell_id = shell.id))
    if len(compress) == 0:
        content ={}
    else:
        sz = zip(all_shell,compress)    
        content = {
            'sz':sz

        }
    return render(request,'reader/library.html',content)

def pdf_view(request,id):
    pdf_loc = book.objects.filter(id = id)
    if pdf_loc:
        pdf_loc = pdf_loc[0].file_book
        with open("media/"+str(pdf_loc), 'r',encoding="utf8") as pdf:
            response = HttpResponse(pdf.read(), mimetype='application/pdf')
            response['Content-Disposition'] = 'inline;filename=some_file.pdf'
            return response
        pdf.closed
    else:
        return Http404()

@login_required
def addshell(request):
    if request.method == 'POST':
        name = request.POST.get('shell_name','')
        reader_obj = reader.objects.get(user = request.user.id)

        shell = shell_form({'name':name,'upload_by':reader_obj})
        if shell.is_valid():
            shell.save()
            messages.success(request,name+" shell is Add ")
        else:
            shell = shell_form()
            messages.warning(request,name+" Shell is note created")
        return redirect('library')

@login_required
def addbook(request):
    if request.method == "POST":
        name = request.POST.get('b_name')
        shellname = request.POST.get('shellName')
        auther = request.POST.get('auther')
        file_book = request.FILES['myfile']
        upload_by = reader.objects.get(user = request.user.id)
        shell = shells.objects.get(name = shellname)
        b1 = book(name = name ,file_book=file_book,shell = shell,auther=auther,upload_by=upload_by)
        b1.save()
        file = str(b1.file_book)
        thumbnail = "media/"+file[:-4]+"front.pdf"
        create_thumbnail(file)
        b1.thumbnail = thumbnail
        b1.save()
        messages.success(request,name+" is Add to your shell "+shellname)

    return redirect('library')

@login_required
def remember(request):
    user = request.user
    if user.id == None:
        return HttpResponse("failure")
    else:
        data = request.GET.get("data","")
        data = json.loads(data)
        book_obj = book.objects.get(id= data["bookid"])
        reader_obj = reader.objects.get(user = user)
        book_rem = reading_record.objects.filter(reader =reader_obj).filter(book=book_obj)
        if not book_rem:
            rem = reading_record(book=book_obj,reader=reader_obj,last_read_page=data["last_page"],total_page = data['total_pages'])
            rem.save()
            return HttpResponse("save")
        else:
            book_rem[0].last_read_page = data['last_page']
            book_rem[0].total_page = data['total_pages']
            book_rem[0].save()
            return HttpResponse("save")

@api_view(['GET'])
def getShellDetail(request):
    if request.method == "GET":
        sid = request.GET.get('id',0)
        if sid:
            shell_object = shells.objects.get(id=sid)
            no_books = len(book.objects.filter(shell = shell_object))
            print(no_books)
            s = {'id':shell_object.id,'name':shell_object.name,'privacy':shell_object.privacy,"no_of_books":no_books,'contrib':shell_object.contrib,'create_by':str(shell_object.upload_by.user.first_name)+" "+str(shell_object.upload_by.user.last_name),'create_on':shell_object.create_on}
            # s = shellSerializer(shell_object)
            # print(s.data)
            return Response(s,status = status.HTTP_200_OK)
        else:
            return HttpResponse("Fail to get detail")
    else:
        return HttpResponse("not a valid request")


@api_view(['PUT','POST','GET'])
def shellupdate(request):
    id = request.POST.get('sid',0)
    s_obj = shells.objects.filter(id=int(id))
    if not s_obj:
        messages.info(request,"in valid shell request")
    else:
         
        s = shellSerializer(s_obj[0],request.data)
        if s.is_valid():
            s.save()
            messages.info(request,"Shell updated")
        else:
            messages.info(request,"Shell not updated "+str(s.errors))
         
    return redirect('library')

@login_required
def book_like(request):
    if request.method == "POST":
        id = request.POST.get("id",'')
        book_obj = book.objects.filter(id= id)
        if not book_obj:
            return JsonResponse({'status':"invalid"})
        else:
            resp = {}
            if book_obj[0].is_liked(request.user.id):
                book_obj[0].likes.remove(request.user)
                resp["status"] = "disliked"

            else:        
                book_obj[0].likes.add(request.user)
                resp["status"] = "liked"
            resp['likes'] = book_obj[0].likes_count()
            return JsonResponse(resp)

    else:
        return JsonResponse({'status':"invalid"})


            
            


 
        
    




