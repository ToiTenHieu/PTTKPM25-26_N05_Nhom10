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

def login_view(request): # Đổi tên view để không trùng với hàm login
    if request.method == 'POST':
        # SỬA 6: Dùng AuthenticationForm để xử lý và xác thực an toàn hơn
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user) # Dùng auth_login đã import
            
            # Logic chuyển hướng vẫn giữ nguyên
            profile = UserProfile.objects.get(user=user)
            if profile.role == 'librarian' or user.is_superuser:
                # Có thể chuyển hướng tới trang admin/dashboard riêng
                return redirect('home')
            else:
                return redirect('home')
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
    else:
        form = AuthenticationForm()
        
    # SỬA 7: Luôn render template cho request GET hoặc khi form không hợp lệ
    return render(request, 'account/login.html', {'form': form})

def logout_view(request): # Đổi tên view
    auth_logout(request) # Dùng auth_logout đã import
    messages.info(request, "Bạn đã đăng xuất.")
    return redirect("login")

@login_required
@transaction.atomic
def profile(request):
    # SỬA 8: Phải gọi trên Model, không phải Form
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        changeprofile_form = ChangeUserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)
        if changeprofile_form.is_valid() and user_form.is_valid():
            changeprofile_form.save()
            user_form.save()
            messages.success(request, "Cập nhật thông tin thành công")
            return redirect('profile')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin")
    else:
        changeprofile_form = ChangeUserProfileForm(instance=profile)
        user_form = UserForm(instance=request.user)
        
    context = {
        'changeprofile_form': changeprofile_form,
        'user_form': user_form,
        'profile': profile,
    }
    return render(request, 'account/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Mật khẩu đã được thay đổi thành công.')
            return redirect('home')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'account/change_password.html', {'form': form})

def home(request):
    return render(request, 'account/home.html')
def regis_by_fb(request):
    return render(request, 'account/regis_by_fb.html')
def regis_by_gg(request):
    return render(request, 'account/regis_by_gg.html')