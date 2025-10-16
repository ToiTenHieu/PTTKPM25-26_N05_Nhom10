from django.shortcuts import render
from django.core.paginator import Paginator
from Librarian.models import Book

def catalog(request):
    books = Book.objects.all().order_by("-book_id")   # lấy danh sách sách
    paginator = Paginator(books, 8)  # 8 sách / trang

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "accounts/catalog.html", {"page_obj": page_obj})
def home(request):
    return render(request, 'library/home.html')
def services(request):
    return render(request, 'library/services.html')
def contact(request):
    return render(request, 'library/contact.html')
def membership(request):
    return render(request, 'library/membership.html')
def payment(request):
    return render(request, 'library/payment.html')
def process_payment(request):
    # Xử lý thanh toán ở đây (giả sử thanh toán thành công)
    return render(request, 'library/process_payment.html')
def payment_done(request):
    return render(request, 'library/payment_done.html')

# Create your views here.
