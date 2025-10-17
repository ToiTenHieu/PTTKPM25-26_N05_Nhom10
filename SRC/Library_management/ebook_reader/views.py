# ebook_reader/views.py
from django.shortcuts import render, get_object_or_404
from .models import Ebook

def read_ebook_view(request, ebook_id):
    # Lấy đối tượng Ebook từ DB dựa trên id
    ebook = get_object_or_404(Ebook, id=ebook_id)

    # Lấy URL công khai của file từ Cloudinary
    # Thư viện đã tự động xử lý việc này cho bạn
    ebook_url = ebook.file.url

    context = {
        'ebook_url': ebook_url,
        'book_title': ebook.book.title,
    }
    return render(request, 'ebook_reader/read_ebook.html', context)