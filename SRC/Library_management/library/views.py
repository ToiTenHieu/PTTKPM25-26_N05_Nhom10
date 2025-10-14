from django.shortcuts import render

def catalog(request):
    return render(request, 'library/catalog.html')
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
