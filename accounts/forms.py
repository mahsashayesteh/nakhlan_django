from django import forms
from .models import Account, UserProfile


class RegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'رمز عبور را وارد کنید',
        'class': 'form-control'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'رمز عبور را مجددا وارد کنید',
        'class': 'form-control'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegisterationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'نام را وارد کنید'
        self.fields['last_name'].widget.attrs['placeholder'] = 'نام خانوادگی را وارد کنید'
        self.fields['email'].widget.attrs['placeholder'] = 'ایمیل را وارد کنید'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'شماره تلفن را وارد کنید'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'border-color:#6f7172'

    def clean(self):
        cleaned_data = super(RegisterationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email_input = cleaned_data.get('email')
        emails = Account.objects.filter(email=email_input).exists()
        if emails:
            raise forms.ValidationError(
                'حساب کاربری با این ایمیل از قبل وجود دارد'
            )
        if len(password) < 8:
            raise forms.ValidationError("رمز عبور باید 8 کاراکتر یا بیشتر باشد")
        if password != confirm_password:
            raise forms.ValidationError(
                "!رمز عبور مطابقت ندارد"
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'نامعتبر': 'فقط فایل عکس'}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'full_address')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
