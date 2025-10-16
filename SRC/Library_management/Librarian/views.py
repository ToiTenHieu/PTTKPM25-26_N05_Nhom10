from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .models import Book
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Book
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User

from django.core.paginator import Paginator
from django.urls import reverse

@login_required
def librarian_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.role != 'librarian':
        return redirect('library:home')

    # 👉 Nếu nhấn nút Thêm Người Dùng
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        name = request.POST.get("name")
        occupation = request.POST.get("occupation")
        address = request.POST.get("address")
        date_of_birth = request.POST.get("date_of_birth")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")

        # 1. Tạo User
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # 2. Tạo UserProfile
        UserProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            occupation=occupation,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            role='user'
        )

        return redirect(reverse("librarian:managebook") + "?section=quanLyNguoiDung")


    # 👉 Nếu GET: load dữ liệu
    users_only = UserProfile.objects.filter(role='user').order_by("id")

    # --- Thêm phân trang ---
    paginator = Paginator(users_only, 5)  # 5 user mỗi trang
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    books = Book.objects.all()
    categories = Book.objects.values_list('category', flat=True).distinct()
    librarian_name = profile.name or profile.user.username

    # =========================
    # 👉 Query BorrowRecord để hiển thị trong manageBorrow.html
    from django.utils.timezone import now
    records = BorrowRecord.objects.select_related("user", "book").filter(
        status__in=['borrowed', 'overdue']
    )

    # 👉 Auto update: nếu quá hạn thì chuyển thành "overdue"
    today = now().date()
    for record in records:
        if record.due_date and record.due_date < today and record.status == 'borrowed':
            record.status = 'overdue'
            record.save()

    total = records.count()
    # =========================

    context = {
        'users': page_obj.object_list,   # user của trang hiện tại
        'page_obj': page_obj,            # để làm thanh phân trang
        'books': books,
        'categories': categories,
        'librarian_name': librarian_name,
        'profile': profile,
        # 👉 Thêm vào context cho manageBorrow.html
        'records': records,
        'total': total,
    }

    return render(request, 'managebook.html', context)


from django.contrib.auth.models import Group


def user_logout(request):
    logout(request)
    return redirect("login")


def home(request):
    return render(request, "accounts/home.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


# views.py
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import UserProfile


def danh_sach_nguoi_dung(request):
    users = UserProfile.objects.select_related('user').all()  # lấy tất cả UserProfile kèm User
    return render(request, 'users_list.html', {'users': users})


from django.core.paginator import Paginator

def catalog(request):
    books = Book.objects.all().order_by("-book_id")   # lấy danh sách sách
    paginator = Paginator(books, 8)  # 8 sách / trang

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "accounts/catalog.html", {"page_obj": page_obj})
@login_required
def payment_done(request):
    return render(request, "accounts/payment_done.html")  
from django.shortcuts import get_object_or_404, render, redirect
from .models import UserProfile  # model chứa phone, address, gender,...

def edit_user(request, user_id):
    profile = get_object_or_404(UserProfile, pk=user_id)
    if request.method == "POST":
        profile.name = request.POST.get('name')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.date_of_birth = request.POST.get('date_of_birth')
        profile.gender = request.POST.get('gender')
        profile.save()
        return redirect(reverse("librarian:managebook") + "?section=quanLyNguoiDung")
    return render(request, 'edit_user.html', {'user': profile})
@csrf_exempt  # hoặc dùng csrf token header trong fetch
def delete_user_api(request, user_id):
    if request.method == "DELETE":
        user_profile = get_object_or_404(UserProfile, pk=user_id)
        user_profile.delete()
        return JsonResponse({"message": "Người dùng đã được xóa thành công."})
    
    return JsonResponse({"error": "Phương thức không hợp lệ."}, status=400)
from django.template.defaultfilters import slugify

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book

@csrf_exempt
def add_book(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        author = data.get("author")
        category = data.get("category")
        quantity = data.get("quantity")
        publish_year = data.get("publishYear")
        description = data.get("description")

        # Lưu vào DB
        book = Book.objects.create(
            title=name,
            author=author,
            category=category,
            quantity=quantity,
            year=publish_year,
            description=description
        )

        return JsonResponse({"message": "Thêm sách thành công", "id": book.book_id}, status=201)
    return JsonResponse({"error": "Phương thức không hợp lệ"}, status=400)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book

@csrf_exempt
def update_book(request, book_id):
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"error": "Book not found"}, status=404)

    if request.method == "GET":
        # Trả về dữ liệu sách để load vào form
        return JsonResponse({
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "category": book.category,
            "quantity": book.quantity,
            "description": book.description,
            "status": book.status,
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            book.title = data.get("title", book.title)
            book.author = data.get("author", book.author)
            book.year = data.get("year", book.year)
            book.category = data.get("category", book.category)
            book.quantity = data.get("quantity", book.quantity)
            book.description = data.get("description", book.description)
            book.status = data.get("status", book.status)
            book.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Book
import json

# accounts/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Book
import json

# GET all books
def book_list(request):
    if request.method == "GET":
        books = Book.objects.all().values()
        return JsonResponse(list(books), safe=False)

# GET or PUT a single book
@csrf_exempt
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == "GET":
        return JsonResponse({
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "category": book.category,
            "quantity": book.quantity,
            "status": book.status,
            "description": book.description,
        })

    elif request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))

        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        book.year = data.get("year", book.year)
        book.category = data.get("category", book.category)
        book.quantity = data.get("quantity", book.quantity)
        book.status = data.get("status", book.status)
        book.description = data.get("description", book.description)
        book.save()

        return JsonResponse({"message": "Book updated successfully"})

    elif request.method == "DELETE":
        book.delete()
        return JsonResponse({"message": "Book deleted successfully"}, status=200)

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
from django.shortcuts import render
from .models import BorrowRecord

from django.shortcuts import render
from .models import BorrowRecord

