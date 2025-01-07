from django import forms

class UserRegistrationForm(forms.Form):  
    user_name = forms.CharField(
        max_length=150,
        label="User Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your username", "class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email", "class": "form-control"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password", "class": "form-control"}),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Re-enter your password", "class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please try again.")

        return cleaned_data


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email",
            "class": "user-details",
            "id": "user-name",
            "required": True
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "class": "user-details",
            "id": "user-password",
            "required": True
        })
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'user-details',
            'id': 'email',
            'placeholder': 'Enter your email'
        })
    )

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'user-details',
            'id': 'new-password',
            'placeholder': 'Enter new password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'user-details',
            'id': 'confirm-password',
            'placeholder': 'Confirm new password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Passwords do not match!")
        return cleaned_data
    

# forms.py
class ProfileUpdateForm(forms.Form):
    user_name = forms.CharField(
        max_length=150,
        label="User Name",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your username",
            "class": "form-control"
        })
    )
    email = forms.EmailField(
        label="Email",
        disabled=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control"
        })
    )

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter current password",
            "class": "form-control"
        })
    )
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter new password",
            "class": "form-control"
        })
    )
    confirm_password = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm new password",
            "class": "form-control"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("New passwords do not match!")
        return cleaned_data