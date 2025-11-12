from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index_view(request):
    """Landing page"""
    return render(request, 'index.html')


def login_view(request):
    """Login page"""
    return render(request, 'login.html')


def register_view(request):
    """Register page"""
    return render(request, 'register.html')


def dashboard_view(request):
    """Dashboard page"""
    return render(request, 'dashboard.html')


def profile_view(request):
    """Profile page"""
    return render(request, 'profile.html')