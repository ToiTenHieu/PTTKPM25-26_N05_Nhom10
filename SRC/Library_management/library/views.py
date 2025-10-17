from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from Librarian.models import Book
from django.contrib import messages

def catalog(request):
    books = Book.objects.all().order_by("-book_id")   # lấy danh sách sách
    paginator = Paginator(books, 8)  # 8 sách / trang

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "library/catalog.html", {"page_obj": page_obj})

def home(request):
    return render(request, 'library/home.html')

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



def about(request):
    return render(request, 'library/about.html')