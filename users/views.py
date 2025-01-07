from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import secrets
from django.core.mail import send_mail
from django.urls import reverse
from datetime import timedelta
from .models import *
from .forms import *

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                existing_user = user_collection.find_one({
                    'email': form.cleaned_data['email']
                })
                
                if existing_user:
                    messages.error(request, 'Email already registered')
                    return render(request, 'users/registration.html', {'form': form})

                # Create new user document
                user = {
                    'user_name': form.cleaned_data['user_name'],
                    'email': form.cleaned_data['email'],
                    'password': make_password(form.cleaned_data['password']),
                    'created_at': now()
                }
                
                # Insert into MongoDB
                user_collection.insert_one(user)
                messages.success(request, 'Registration successful!')
                return redirect('login')
                
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                return render(request, 'users/registration.html', {'form': form})
    else:
        form = UserRegistrationForm()

    return render(request, 'users/registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = user_collection.find_one({'email': email})
            
            if user and check_password(password, user['password']):
                # Store user info in request.session
                request.session['user_info'] = {
                    'user_name': user['user_name'],
                    'email': user['email']
                }
                
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
                return render(request, 'users/login.html', {'form': form})
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout(request):
    # Clear only user info from session
    if 'user_info' in request.session:
        del request.session['user_info']
    messages.success(request, 'Logged out successfully')
    return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = user_collection.find_one({'email': email})
            
            if user:
                # Generate token
                token = secrets.token_urlsafe(32)
                expiry = now() + timedelta(hours=1) 
                
                # Store token in database
                reset_token_collection.insert_one({
                    'email': email,
                    'token': token,
                    'expiry': expiry
                })
                
                # In a real application, you would send this link via email
                reset_link = request.build_absolute_uri(
                    reverse('reset_password', args=[token])
                )

                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_link}',
                    'no-reply@yourdomain.com',
                    [email],
                )

                messages.success(
                    request, 'A password reset link has been sent to your email.'
                )
                
                return redirect('forgot_password')
            else:
                messages.error(request, 'Email not found')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'users/forgot_password.html', {'form': form})

def reset_password(request, token):
    # Verify token
    token_data = reset_token_collection.find_one({
        'token': token,
         'expiry': {'$gt': now()}
    })
    
    if not token_data:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return render(request, 'users/forgot_password.html', {'form': ForgotPasswordForm()})
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            # Update password
            new_password = make_password(form.cleaned_data['new_password'])
            user_collection.update_one(
                {'email': token_data['email']},
                {'$set': {'password': new_password}}
            )
            
            # Delete used token
            reset_token_collection.delete_one({'token': token})
            
            messages.success(request, 'Password successfully reset')
            return redirect('login')
    else:
        form = ResetPasswordForm()
    
    return render(request, 'users/reset_password.html', {'form': form})


def profile(request):
    if 'user_info' not in request.session:
        return redirect('login')
        
    user = user_collection.find_one({'email': request.session['user_info']['email']})
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, initial={
            'user_name': user['user_name'],
            'email': user['email']
        })
        
        if form.is_valid():
            # Update user info
            user_collection.update_one(
                {'email': user['email']},
                {'$set': {
                    'user_name': form.cleaned_data['user_name'],
                    'updated_at': now()
                }}
            )
            
            # Update session info
            request.session['user_info']['user_name'] = form.cleaned_data['user_name']
            request.session.modified = True
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(initial={
            'user_name': user['user_name'],
            'email': user['email']
        })
    
    return render(request, 'users/profile.html', {'form': form, 'user': user})

def settings(request):
    if 'user_info' not in request.session:
        return redirect('login')
        
    user = user_collection.find_one({'email': request.session['user_info']['email']})
    
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            
            # Verify current password
            if check_password(current_password, user['password']):
                # Update password
                user_collection.update_one(
                    {'email': user['email']},
                    {'$set': {
                        'password': make_password(new_password),
                        'updated_at': now()
                    }}
                )
                
                messages.success(request, 'Password changed successfully!')
                return redirect('settings')
            else:
                messages.error(request, 'Current password is incorrect!')
    else:
        form = ChangePasswordForm()
    
    return render(request, 'users/settings.html', {'form': form})
