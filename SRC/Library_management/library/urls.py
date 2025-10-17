from django.urls import path
from . import views

app_name='library'

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('home/', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('membership/', views.membership, name='membership'),
    path('', views.home, name='home'),  # Đường dẫn gốc dẫn đến trang chủ
    path('payment/', views.payment, name='payment'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('digital/', views.digital, name='digital'),
    path("borrow/", views.borrow_book, name="borrow_book"),
    path('book-detail/<int:book_id>/', views.book_detail_view, name='book_detail_view'),
]