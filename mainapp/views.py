from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import redirect
from .models import CustomUser

def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not password or not confirm_password:
            return redirect('register')

        if password != confirm_password:
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            return redirect('register')

        CustomUser.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'mainapp/register.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return redirect('login')

    return render(request, 'mainapp/login.html')

def logout_user(request):
    logout(request)
    print("Пользователь вышел из аккаунта")
    return redirect('login')

@login_required
def profile_user(request):
    return render(request, 'mainapp/profile.html', {'username': request.user.username})

@login_required
def change_password_user(request):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not old_password or not new_password or not confirm_password:
            return render(request, 'mainapp/change_password.html')

        if new_password != confirm_password:
            return render(request, 'mainapp/change_password.html')

        if not request.user.check_password(old_password):
            return render(request, 'mainapp/change_password.html')

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        return redirect('profile')

    return render(request, 'mainapp/change_password.html')

@login_required
def change_username_user(request):
    if request.method == "POST":
        new_username = request.POST.get('new_username')

        if not new_username:
            return render(request, 'mainapp/change_username.html')

        if CustomUser.objects.filter(username=new_username).exists():
            return render(request, 'mainapp/change_username.html')

        user = request.user
        user.username = new_username
        user.save()

        return redirect('profile')

    return render(request, 'mainapp/change_username.html')

@login_required
def delete_account_user(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        return redirect('login')

    return render(request, 'mainapp/delete_account.html')
