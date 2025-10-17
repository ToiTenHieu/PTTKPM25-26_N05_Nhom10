# ebook_reader/models.py
from django.db import models
from cloudinary.models import CloudinaryField

# Import model Book từ app thư viện chính của bạn
from Librarian.models import Book # <-- Thay 'library' bằng tên app chính của bạn

class Ebook(models.Model):
    # Mỗi Ebook sẽ được liên kết với một quyển sách
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='ebook')

    # Đây là trường lưu file PDF/EPUB lên Cloudinary
    # resource_type='raw' dùng cho các file không phải ảnh/video
    # 'auto' sẽ tự nhận diện, nhưng 'raw' rõ ràng hơn cho file PDF
    file = CloudinaryField(
        'ebooks',
        resource_type='raw',
    type='upload'   # ✅ Bắt buộc để public file PDF
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ebook for '{self.book.title}'"