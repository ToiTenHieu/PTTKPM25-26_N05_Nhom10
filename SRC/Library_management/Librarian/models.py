from django.db import models
from django.contrib.auth.models import User
from account.models import UserProfile
# Create your models here.
class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]

    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.title} - {self.author}"
class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Đang mượn'),
        ('returned', 'Đã trả'),
        ('overdue', 'Quá hạn'),
    ]

    record_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="borrow_records")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_records")

    borrow_date = models.DateField()   # ngày mượn
    due_date = models.DateField()      # hạn trả
    return_date = models.DateField(blank=True, null=True)  # ngày trả
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrowed')

    def __str__(self):
        return f"Record {self.record_id} - {self.user} - {self.book}"
