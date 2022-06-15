from django import template
from books.models import reading_record,reader,book
register = template.Library()

def reading_progress(user,book):
    if user.id == None:
        return 0
    else:
        reader_obj = reader.objects.get(user = user)
        rid = reading_record.objects.filter(reader =reader_obj).filter(book=book)
        if not rid:
            return 0
        else:
            return int(rid[0].progress())


def last_page(user,book):
    if user.id == None:
        return 1
    else:
        reader_obj = reader.objects.get(user = user)
        rid = reading_record.objects.filter(reader =reader_obj).filter(book=book)
        if not rid:
            return 1
        else:
            return int(rid[0].last_read_page)

def no_of_books(shell):
    no_books = len(book.objects.filter(shell = shell))
    return no_books

def is_liked(user,book):
    if user.id == None:
        return False
    else:
        return book.is_liked(user.id)
        
    
    

register.filter("progress",reading_progress)
register.filter("last_page",last_page)
register.filter("is_liked",is_liked)
register.filter("no_of_books",no_of_books)