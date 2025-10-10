from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=True)
    occupation = forms.CharField(max_length=100, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('male','Nam'), ('female','Nữ'), ('other','Khác')], required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                phone=self.cleaned_data.get('phone'),
                occupation=self.cleaned_data.get('occupation'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                gender=self.cleaned_data.get('gender'),
                address=self.cleaned_data.get('address'),
            )
        return user
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'profile-input w-full px-4 py-3 text-gray-900',
                'readonly': True
            }),
        }
class ChangeUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone', 'date_of_birth', 'gender', 'occupation', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'profile-input w-full px-4 py-3 text-gray-900', 'readonly': True}),
            'phone': forms.TextInput(attrs={'class': 'profile-input w-full px-4 py-3 text-gray-900', 'readonly': True}),
            'date_of_birth': forms.DateInput(attrs={'class': 'profile-input w-full px-4 py-3 text-gray-900', 'type': 'date', 'readonly': True}),
            'gender': forms.Select(
                choices=[('male', 'Nam'), ('female', 'Nữ'), ('other', 'Khác')],
                attrs={'class': 'profile-input w-full px-4 py-3 text-gray-900', 'disabled': True}
            ),
            'occupation': forms.TextInput(attrs={'class': 'profile-input w-full px-4 py-3 text-gray-900', 'readonly': True}),
            'address': forms.Textarea(attrs={'class': 'profile-input w-full px-4 py-3 text-gray-900', 'rows': 3, 'readonly': True}),
        }
class ChangePasswordForm(PasswordChangeForm):
    pass
