from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from Librarian.models import Book
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Librarian.models import Book, BorrowRecord
from account.models import UserProfile
def catalog(request):
    # Nếu chưa đăng nhập, chuyển hướng về trang đăng nhập
    if not request.user.is_authenticated:
        return redirect("account:logout")

    # Lấy danh sách sách
    books = Book.objects.all().order_by("-book_id")
    paginator = Paginator(books, 8)  # 8 sách mỗi trang

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Lấy UserProfile theo user hiện tại
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect("account:logout")  # nếu không có hồ sơ thì về đăng nhập lại

    # Truyền dữ liệu ra template
    context = {
        "user_profile": user_profile,
        "max_days": getattr(user_profile, "max_days", 10),  # fallback mặc định
        "page_obj": page_obj,
    }
    return render(request, "library/catalog.html", context)


def home(request):
    # Nếu chưa đăng nhập, chuyển hướng về trang đăng nhập
    if not request.user.is_authenticated:
        return redirect("account:logout")

    # Lấy danh sách sách + tính điểm trung bình
    books_with_rating = Book.objects.annotate(
        avg_rating=Avg('reviews__rating')  # ✅ dùng đúng related_name của Review
    ).order_by("-book_id")

    # Phân trang
    paginator = Paginator(books_with_rating, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Lấy UserProfile
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect("login")

    # Truyền dữ liệu ra template
    context = {
        "user_profile": user_profile,
        "max_days": getattr(user_profile, "max_days", 10),
        "page_obj": page_obj,  # ✅ chứa cả avg_rating rồi
    }
    return render(request, "library/home.html", context)

def services(request):
    return render(request, 'library/services.html')

from django.conf import settings
def contact(request):
    latitude = 21.06147737140819
    longitude = 105.57668318886614
    context = {
        'google_maps_api_key':settings.GOOGLE_MAPS_API_KEY,
        'lat':latitude,
        'lng':longitude,
    }
    return render(request, 'library/contact.html',context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.membership_context import MembershipContext
from account.models import UserProfile

@login_required
def membership(request):
    profile = UserProfile.objects.get(user=request.user)
    current_rank = profile.membership_level
    membership_context = MembershipContext(current_rank)
    privileges = membership_context.get_info()
    context = {
        "profile": profile,
        "privileges": privileges,
        "current_rank": current_rank,
    }
    return render(request, 'library/membership.html', context)

@login_required
def upgrade_membership(request, level):
    profile = UserProfile.objects.get(user=request.user)

    if profile.upgrade_membership(level):
        messages.success(request, f"Bạn đã nâng cấp thành công lên {dict(UserProfile.MEMBERSHIP_CHOICES)[level]}")
    else:
        messages.warning(request, "Bạn không thể hạ cấp hoặc giữ nguyên cấp thành viên.")

    return redirect('account:profile')

@login_required
def payment(request):
    level = request.GET.get("level", "basic")
    level_map = {
        "basic":"Cơ bản",
        "standard":"Tiêu chuẩn",
        "premium":"Cao cấp",
    }
    profile, create = UserProfile.objects.get_or_create(user=request.user)
    user = request.user
    level_name = level_map.get(level, "Cơ bản")
    context = {
        "level": level,
        "level_name": level_name,
        "profile": profile,
        "user": user,
    }
    return render(request, 'library/payment.html', context)

from django.utils import timezone
from datetime import timedelta
@login_required
def process_payment(request):
    if request.method == "POST":
        level =request.POST.get("level", "basic")
        profile = request.user.userprofile
        if profile.membership_level != level:
            upgrade_time = timezone.now()
            profile.membership_level = level
            profile.membership_upgrade_date = upgrade_time
            profile.membership_expiry_date = upgrade_time + timedelta(days=30)
            profile.save()
            messages.success(request, f"Bạn đã nâng cấp thành công lên {dict(UserProfile.Membership_Choices)[level]}")
        else:
            messages.warning(request, "Bạn không thể hạ cấp hoặc giữ nguyên cấp thành viên.")
        return redirect("library:payment_done")
    return redirect("library:payment_done")

from account.forms import UserForm, ChangeUserProfileForm as UserProfileForm
@login_required
def payment_done(request):
    user = request.user
    profile, create = UserProfile.objects.get_or_create(user=user)
    
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Cập nhật thông tin thành công!")
            return redirect("account:profile") # Tên URL của chính view này
        else:
            messages.error(request, "Có lỗi xảy ra, vui lòng kiểm tra lại các trường thông tin.")
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    # Thêm user và date_joined vào context để hiển thị trong template
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "user": user, # Để tiện truy cập các thông tin như username, date_joined
    }
    return render(request, "library/payment_done.html",context)     

def digital(request):
    return render(request, 'library/digital.html')
from datetime import timedelta
from datetime import datetime


@login_required
def borrow_book(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        book_id = data.get("book_id")
        borrow_date = data.get("borrow_date")
        return_date = data.get("return_date")
        quantity = int(data.get("quantity", 1))

        try:
            book = Book.objects.get(pk=book_id)
            user_profile = UserProfile.objects.get(user=request.user)

            # 🧭 Lấy thông tin gói thành viên
            membership_state = user_profile.get_membership_state()

            # 🧮 1️⃣ Đếm số sách người này đang mượn (chưa trả)
            current_borrowed = BorrowRecord.objects.filter(
                user=user_profile,
                status__in=["borrowed", "overdue"]
            ).count()

            # Giới hạn số sách theo gói
            if current_borrowed + quantity > membership_state.max_books:
                return JsonResponse({
                    "success": False,
                    "message": f"Gói {membership_state.name} chỉ cho phép mượn tối đa {membership_state.max_books} cuốn sách. "
                               f"Hiện bạn đang mượn {current_borrowed} cuốn."
                })

            # 🕒 2️⃣ Kiểm tra số ngày không vượt quá giới hạn
            borrow_dt = datetime.strptime(borrow_date, "%Y-%m-%d").date()
            return_dt = datetime.strptime(return_date, "%Y-%m-%d").date()
            delta_days = (return_dt - borrow_dt).days

            if delta_days > membership_state.max_days:
                return JsonResponse({
                    "success": False,
                    "message": f"Gói {membership_state.name} chỉ được mượn tối đa {membership_state.max_days} ngày."
                })

            # 📚 3️⃣ Kiểm tra tồn kho
            if book.quantity < quantity:
                return JsonResponse({
                    "success": False,
                    "message": "Không đủ số lượng sách trong kho."
                })

            # 💾 4️⃣ Ghi vào bảng mượn
            BorrowRecord.objects.create(
                user=user_profile,
                book=book,
                borrow_date=borrow_date,
                due_date=return_date,
                status="borrowed"
            )

            # 🔄 5️⃣ Cập nhật số lượng sách
            book.quantity -= quantity
            if book.quantity <= 0:
                book.status = "unavailable"
            book.save()

            return JsonResponse({
                "success": True,
                "message": "Mượn sách thành công!"
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"Lỗi: {str(e)}"
            })

    return JsonResponse({
        "success": False,
        "message": "Phương thức không hợp lệ."
    })
from django.shortcuts import render, get_object_or_404
# library/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Avg # Cần thiết để tính điểm trung bình
from .models import Book, Review

def book_detail_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    # 1. Xử lý Form Đánh Giá
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # Chuyển hướng nếu người dùng chưa đăng nhập
            return redirect('account:login') 
            
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Tạo hoặc Cập nhật đánh giá
        Review.objects.update_or_create(
            book=book,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        messages.success(request, 'Cảm ơn bạn đã gửi đánh giá!')
        return redirect(reverse('library:book_detail_view', args=[book_id]))

    # 2. Truy vấn dữ liệu cho Template (GET)
    
    # Lấy tất cả đánh giá cho sách này
    reviews = book.reviews.all()
    
    # Tính điểm trung bình
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Kiểm tra xem người dùng hiện tại đã đánh giá chưa
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    context = {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'user_review': user_review, # Đánh giá của người dùng hiện tại
    }
    
    return render(request, 'library/book_detail.html', context)
from django.db.models import Avg
from .models import Review # Cần import Model Review

def about(request):
    return render(request, 'library/about.html')
@login_required
def borrowed_books(request):
    # Lấy user hiện tại
    user_profile = request.user.userprofile
    borrowed_books = BorrowRecord.objects.filter(user=user_profile).select_related('book')

    context = {
        'borrowed_books': borrowed_books,
    }
    return render(request, 'library/borrowed_books.html', context)
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from datetime import date

def renew_book(request, record_id):
    record = get_object_or_404(BorrowRecord, id=record_id, user=request.user.userprofile)
    if record.extend_due_date():
        messages.success(request, "📅 Gia hạn thành công thêm 7 ngày!")
    else:
        messages.error(request, "⚠️ Bạn đã hết lượt gia hạn miễn phí hoặc không đủ điều kiện.")
    return redirect('library:borrowed_books')

def extend_book(request, record_id):
    record = get_object_or_404(BorrowRecord, pk=record_id)
    user_profile = UserProfile.objects.get(user=request.user)

    # ❌ Nếu sách không ở trạng thái có thể gia hạn
    if record.status not in ['borrowed', 'overdue']:
        messages.error(request, "Sách này không thể gia hạn.")
        return redirect('library:borrowed_books')

    # ✅ Lấy giới hạn lượt gia hạn theo gói
    max_extend = user_profile.free_extend  
    total_renewed = user_profile.total_renew_used()

    if total_renewed >= max_extend:
        messages.error(
            request,
            f"⚠️ Bạn đã đạt giới hạn {max_extend} lần gia hạn cho gói {user_profile.membership_level.upper()}."
        )
        return redirect('library:borrowed_books')

    # ✅ Nếu chưa vượt giới hạn thì cho phép gọi hàm gia hạn
    if record.extend_due_date():
        messages.success(
            request,
            f"📘 Gia hạn thành công! Hạn mới: {record.due_date.strftime('%d/%m/%Y')}"
        )
    else:
        messages.error(request, "⚠️ Bạn đã hết lượt gia hạn miễn phí cho gói hiện tại.")

    return redirect('library:borrowed_books')
