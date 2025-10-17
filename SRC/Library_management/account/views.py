from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout # SỬA 1: Dùng alias
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm # SỬA 2: Dùng form đăng nhập có sẵn
from django.db import transaction
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserForm, ChangeUserProfileForm
from .models import UserProfile


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        occupation = request.POST.get("occupation")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        address = request.POST.get("address")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Mật khẩu nhập lại không khớp!")
            return redirect("/account/register/")
        # Kiểm tra username đã tồn tại
        if User.objects.filter(username=username).exists():
            messages.error(request, "Tên đăng nhập đã tồn tại!")
            return redirect("/account/register/")
        # Tạo User
        user = User.objects.create_user(username=username, email=email, password=password)
        # Tạo UserProfile với tất cả các trường
        UserProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            occupation=occupation,
            gender=gender ,
            date_of_birth=date_of_birth or None,
            address=address
        )
        messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
        return redirect("/account/login/")
    else:
        # GET → render template form đăng ký
        return render(request, "account/register.html")

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile  # đảm bảo đã import đúng model

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
<<<<<<< Updated upstream
            auth_login(request, user)

            # 🔑 Lấy role từ UserProfile
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                messages.error(request, "Không tìm thấy thông tin người dùng.")
                return redirect('login')

            # 🔁 Chuyển hướng theo vai trò
            if profile.role == 'librarian':
                return redirect('Librarian:managebook')  # giao diện thủ thư
            elif user.is_superuser:
                return redirect('/admin/')               # admin
            else:
                return redirect('library:home')          # người dùng thường

=======
            auth_login(request, user) # Dùng auth_login đã import
            
            # Logic chuyển hướng vẫn giữ nguyên
            profile = UserProfile.objects.get(user=user)
            if profile.role == 'librarian' or user.is_superuser:
                # Có thể chuyển hướng tới trang admin/dashboard riêng
                return redirect('library:home')
            else:
                return redirect('library:home')
>>>>>>> Stashed changes
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
    else:
        form = AuthenticationForm()

    # Luôn render lại form khi GET hoặc form không hợp lệ
    return render(request, 'account/login.html', {'form': form})


def logout_view(request): 
    auth_logout(request) 
    messages.info(request, "Bạn đã đăng xuất.")
    return redirect("account:login")

@login_required
@transaction.atomic
def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ChangeUserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Cập nhật thông tin thành công!")
            return redirect("account:profile") 
        else:
            messages.error(request, "Có lỗi xảy ra, vui lòng kiểm tra lại các trường thông tin.")
    else:
        user_form = UserForm(instance=user)
        profile_form = ChangeUserProfileForm(instance=profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "user": user,
    }
    return render(request, "account/profile.html", context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Mật khẩu đã được thay đổi thành công.')
            return redirect('library:home')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'account/change-password.html', {'form': form})
def regis_by_fb(request):
    return render(request, 'account/regis_by_fb.html')
def regis_by_gg(request):
    return render(request, 'account/regis_by_gg.html')